pragma solidity ^0.8.7;

contract SpectramaInu is IBEP20, Auth {
    using SafeMath for uint256;

    address private WETH;
    address private DEAD = 0x000000000000000000000000000000000000dEaD;
    address private ZERO = 0x0000000000000000000000000000000000000000;

    string private constant  _name = "Spectrama Inu";
    string private constant _symbol = "SPC";
    uint8 private constant _decimals = 9;

    uint256 private _totalSupply = 1000000000000 * (10 ** _decimals);
    uint256 private _maxTxAmountBuy = _totalSupply;
    

    mapping (address => uint256) private _balances;
    mapping (address => mapping (address => uint256)) private _allowances;

    mapping (address => bool) private isFeeExempt;
    mapping (address => bool) private isDividendExempt;
    mapping (address => bool) private isBot;
    
    uint256 private totalFee = 14;
    uint256 private feeDenominator = 100;

    address payable public marketingWallet = payable(0x2B15978b360b6c0d8356a5B564ABdaFFD1c4188A);
    address payable public treasury = payable(0x2B15978b360b6c0d8356a5B564ABdaFFD1c4188A);

    IDEXRouter public router;
    address public pair;

    uint256 public launchedAt;
    bool private tradingOpen;
    bool private buyLimit = true;
    uint256 private maxBuy = 10000000000 * (10 ** _decimals);
    
    bool private inSwap;

    constructor() {
        address _owner = 0x8A6844F2EB6AB1c1Eb31795EBf908739771Fbc8c;
        router = IDEXRouter(0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D);
            
        WETH = router.WETH();
        
        pair = IDEXFactory(router.factory()).createPair(WETH, address(this));
        
        _allowances[address(this)][address(router)] = type(uint256).max;

        distributor = new DividendDistributor(_owner, treasury);

        isFeeExempt[_owner] = true;
        isFeeExempt[marketingWallet] = true;
        isFeeExempt[treasury] = true;        
              
        isDividendExempt[pair] = true;
        isDividendExempt[address(this)] = true;
        isDividendExempt[DEAD] = true;        

        _balances[_owner] = _totalSupply;
    
        emit Transfer(address(0), _owner, _totalSupply);
    }

    receive() external payable { }

    function approve(address spender, uint256 amount) public {
        _allowances[msg.sender][spender] = amount;
        emit Approval(msg.sender, spender, amount);
        return true;
    }

    function approveMax(address spender) external {
        return approve(spender, type(uint256).max);
    }

    function transfer(address recipient, uint256 amount) external {
        return _transferFrom(msg.sender, recipient, amount);
    }

    function transferFrom(address sender, address recipient, uint256 amount) external {
        if(_allowances[sender][msg.sender] != type(uint256).max){
            _allowances[sender][msg.sender] = _allowances[sender][msg.sender].sub(amount, "Insufficient Allowance");
        }

        return _transferFrom(sender, recipient, amount);
    }

    function _transferFrom(address sender, address recipient, uint256 amount) internal {
        if (sender!= owner && recipient!= owner) require(tradingOpen, "Trading not yet enabled."); 
        require (!isBot[sender] && !isBot[recipient], "Nice try");
        if (buyLimit) { 
            if (sender!=owner && recipient!= owner) require (amount<=maxBuy, "Too much sir");        
        }
        if (block.number <= (launchedAt + 1)) { 
            isBot[recipient] = true;
            isDividendExempt[recipient] = false; 
        }
       
        if(inSwap){ return _basicTransfer(sender, recipient, amount); }      
    
        bool shouldSwapBack = /*!inSwap &&*/ (recipient==pair && balanceOf(address(this)) > 0);
        if(shouldSwapBack){ swapBack(); }

        _balances[sender] = _balances[sender].sub(amount, "Insufficient Balance");

        uint256 amountReceived = shouldTakeFee(sender, recipient) ? takeFee(sender, amount) : amount;
        
        _balances[recipient] = _balances[recipient].add(amountReceived);

        if(sender != pair && !isDividendExempt[sender]){ try distributor.setShare(sender, _balances[sender]) {} catch {} }
        if(recipient != pair && !isDividendExempt[recipient]){ try distributor.setShare(recipient, _balances[recipient]) {} catch {} }

        emit Transfer(sender, recipient, amountReceived);
        return true;
    }
    
    function _basicTransfer(address sender, address recipient, uint256 amount) internal {
        _balances[sender] = _balances[sender].sub(amount, "Insufficient Balance");
        _balances[recipient] = _balances[recipient].add(amount);
        emit Transfer(sender, recipient, amount);
        return true;
    }

 
    function shouldTakeFee(address sender, address recipient) internal {
        return ( !(isFeeExempt[sender] || isFeeExempt[recipient]) &&  (sender == pair || recipient == pair) );
   }

    function takeFee(address sender, uint256 amount) internal {
        uint256 feeAmount;
        feeAmount = amount.mul(totalFee).div(feeDenominator);
        _balances[address(this)] = _balances[address(this)].add(feeAmount);
        emit Transfer(sender, address(this), feeAmount);   

        return amount.sub(feeAmount);
    }

   
    function swapBack() internal {
        uint256 amountToSwap = balanceOf(address(this));

        address[] memory path = new address[](2);
        path[0] = address(this);
        path[1] = WETH;

        
        router.swapExactTokensForETHSupportingFeeOnTransferTokens(
            amountToSwap,
            0,
            path,
            address(this),
            block.timestamp
        );
        
        uint256 amountTreasury = (address(this).balance).div(2);
        uint256 amountMarketing = (address(this).balance).div(2);

             
        payable(marketingWallet).transfer(amountMarketing);
        payable(treasury).transfer(amountTreasury);
    }

    
    function openTrading() external onlyOwner {
        launchedAt = block.number;
        tradingOpen = true;
    }    
  
    
    function setBot(address _address) external onlyOwner {
        isBot[_address] = true;
        _setIsDividendExempt(_address, true);
    }
    
    function setBulkBots(address[] memory bots_) external onlyOwner {
        for (uint i = 0; i < bots_.length; i++) {
        isBot[bots_[i]] = true;
        _setIsDividendExempt(bots_[i], true);

        }
    }

    function delBulkBots(address[] memory bots_) external onlyOwner {
        for (uint i = 0; i < bots_.length; i++) {
        isBot[bots_[i]] = false;
        _setIsDividendExempt(bots_[i], false);

        }
    }

    function isInBot(address _address) external onlyOwner {
        return isBot[_address];
    }
    
    function _setIsDividendExempt(address holder, bool exempt) internal {
        require(holder != address(this) && holder != pair);
        isDividendExempt[holder] = exempt;
        if(exempt){
            distributor.setShare(holder, 0);
        }else{
            distributor.setShare(holder, _balances[holder]);
        }
    }

    function setFee (uint256 _fee) external onlyOwner {
        require (_fee <= 14, "Fee can't exceed 14%");
        totalFee = _fee;
    }
  
    function manualSend() external onlyOwner {
        uint256 contractETHBalance = address(this).balance;
        payable(marketingWallet).transfer(contractETHBalance);
    }

}