pragma solidity ^0.5.0;

contract  TruckersInu is ERC20 {

    using SafeMath for uint256;

    string public symbol = " TruckersInu";
    string public name = " TRUCKERS";
    uint8 public decimals = 18;
    uint256 private _totalSupply = 1000000000000000000000000000;
    uint256 oneHundredPercent = 100;

    mapping(address => uint256) balances;
    mapping(address => mapping(address => uint256)) allowed;

    constructor() public {
        balances[msg.sender] = _totalSupply;
        emit Transfer(address(0), msg.sender, _totalSupply);
    }

    function findOnePercent(uint256 amount) private {
        uint256 roundAmount = amount.ceil(oneHundredPercent);
        uint256 fivePercent = roundAmount.mul(oneHundredPercent).div(1000);
        return fivePercent;
    }

    function transfer(address to, uint256 amount) public {
      require(amount <= balances[msg.sender]);
      require(to != address(0));

      uint256 tokensToBurn = findOnePercent(amount);
      uint256 tokensToTransfer = amount.sub(tokensToBurn);

      balances[msg.sender] = balances[msg.sender].sub(amount);
      balances[to] = balances[to].add(tokensToTransfer);

      _totalSupply = _totalSupply.sub(tokensToBurn);

      emit Transfer(msg.sender, to, tokensToTransfer);
      emit Transfer(msg.sender, address(0), tokensToBurn);
      return true;
    }

    function approve(address spender, uint256 amount) public {
        allowed[msg.sender][spender] = amount;
        emit Approval(msg.sender, spender, amount);
        return true;
    }

    function transferFrom(address from, address to, uint256 amount) public {
      require(amount <= balances[from]);
      require(amount <= allowed[from][msg.sender]);
      require(to != address(0));

      balances[from] = balances[from].sub(amount);

      uint256 tokensToBurn = findOnePercent(amount);
      uint256 tokensToTransfer = amount.sub(tokensToBurn);

      balances[to] = balances[to].add(tokensToTransfer);
      _totalSupply = _totalSupply.sub(tokensToBurn);

      allowed[from][msg.sender] = allowed[from][msg.sender].sub(amount);

      emit Transfer(from, to, tokensToTransfer);
      emit Transfer(from, address(0), tokensToBurn);

      return true;
    }
}