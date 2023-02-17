pragma solidity ^0.8;

contract StakingRewards {
    IERC20 public rewardsToken;
    IERC20 public stakingToken;

    uint public rewardRate;
    uint public lastUpdateTime;
    uint public rewardPerTokenStored;
    address public owner;

    mapping(address => uint) public userRewardPerTokenPaid;
    mapping(address => uint) public rewards;

    uint private _totalSupply;
    mapping(address => uint) private _balances;

    constructor(address _token,uint _rewardrate) {
        stakingToken = IERC20(_token);
        rewardsToken = IERC20(_token);
        rewardRate=_rewardrate;
        owner=(msg.sender);
    }

    function setRewardRate(uint _rate) public {
        require(owner==msg.sender,"Owner Only accesable");
        rewardRate=_rate;
    }

    function AddRewards(uint _amount) public {
        require(owner==msg.sender,"Owner Only accesable");
         rewardsToken.transfer(msg.sender, _amount);
    }

    function rewardPerToken() public view returns (uint) {
        if (_totalSupply == 0) {
            return 0;
        }
        return
            rewardPerTokenStored +
            (((block.timestamp - lastUpdateTime) * rewardRate * 1e18) / _totalSupply);
    }

    function earned(address account) public {
        return
            ((_balances[account] *
                (rewardPerToken() - userRewardPerTokenPaid[account])) / 1e18) +
            rewards[account];
    }

    modifier updateReward(address account) {
        rewardPerTokenStored = rewardPerToken();
        lastUpdateTime = block.timestamp;

        rewards[account] = earned(account);
        userRewardPerTokenPaid[account] = rewardPerTokenStored;
        _;
    }

    function stake(uint _amount) external {
        _totalSupply += _amount;
        _balances[msg.sender] += _amount;
        stakingToken.transferFrom(msg.sender, address(this), _amount);
    }

    function withdraw() external {
        uint _amount = _balances[msg.sender];
        _totalSupply -= _amount;
         _balances[msg.sender] =0;
        stakingToken.transfer(msg.sender, _amount);

        uint reward = rewards[msg.sender];
        rewards[msg.sender] = 0;
        rewardsToken.transfer(msg.sender, reward);
       
    }

    function getReward() external {
        uint reward = rewards[msg.sender];
        rewards[msg.sender] = 0;
        rewardsToken.transfer(msg.sender, reward);
    }
}