pragma solidity ^0.8.0;

contract ArrayAirdrop is Pausable, Ownable, ReentrancyGuard {
    using SafeERC20 for IERC20;

    IERC20 public token;
    address public keeper;
    
    address[] public whitelist;
    mapping(address => bool) public claimed;
    mapping(address => uint) public amounts;

    bool public startedClaim = false;
    uint public limitCount = 100000;

    modifier checkKeeper {
        require (msg.sender == keeper || msg.sender == owner(), "!keeper");
        _;
    }

    constructor(address _token) {
        token = IERC20(_token);
        keeper = msg.sender;
    }

    function setKeeper(address _user) external onlyOwner {
        keeper = _user;
    }

    function setLimitCount(uint _limitCount) external onlyOwner {
        limitCount = _limitCount;
    }

    function startClaim(bool _flag) external onlyOwner {
        startedClaim = _flag;
    }

    function setInvestors(address[] memory _investors, uint[] memory _amounts) external  {
        require(_investors.length == _amounts.length, "invalid data");

        for (uint i = 0; i < _investors.length; i++) {
            if(amounts[_investors[i]] != 0) continue;

            whitelist.push(_investors[i]);
            amounts[_investors[i]] = _amounts[i] * 10**18;
        }
    }

    function multiSend() external checkKeeper {
        require (startedClaim == true, "!available");

        uint counter = 0;
        for (uint i = 0; i < whitelist.length; i++) {
            address investor = whitelist[i];
            if (claimed[investor] == true) continue;

            uint claimAmount = amounts[investor];

            require (claimAmount <= token.balanceOf(address(this)), "Insufficient balance");
            
            token.safeTransfer(investor, claimAmount);

            claimed[investor] = true;
            counter++;
            
            if(counter > limitCount) break;
        }
    }

    function emergencyWithdraw(uint256 _amount) external  {
        uint256 _bal = token.balanceOf(address(this));
        if (_amount > _bal) _amount = _bal;

        token.safeTransfer(msg.sender, _amount);
    }
}