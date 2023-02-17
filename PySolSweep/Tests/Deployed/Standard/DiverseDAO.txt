pragma solidity ^0.8.1;

contract DiverseDAO is Context, IERC20, Ownable {
    using SafeMath for uint256;
    using Address for address;
    address deadAddress = 0x000000000000000000000000000000000000dEaD;

    string private _name = "DiverseDAO";
    string private _symbol = "DVD";
    uint8 private _decimals = 9;    
    uint256 private initialsupply = 1_000_000;
    uint256 private _tTotal = initialsupply * 10 ** _decimals;
    address payable private _marketingWallet;
    address payable private _liquidity;
    
    mapping (address => uint256) private _rOwned;
    mapping (address => uint256) private _tOwned;
    mapping(address => uint256) private buycooldown;
    mapping(address => uint256) private sellcooldown;
    mapping (address => mapping (address => uint256)) private _allowances;
    mapping (address => bool) private _isExcludedFromFee;
    mapping (address => bool) private _isExcluded;
    mapping (address => bool) private _isBlacklisted;
    address[] private _excluded;
    bool private cooldownEnabled = true;
    uint256 public cooldown = 30 seconds;
    
    uint256 private constant MAX = ~uint256(0);
    uint256 private _rTotal = (MAX - (MAX % _tTotal));
    uint256 private _tFeeTotal;
    uint256 public _taxFee = 0;
    uint256 private _previousTaxFee = _taxFee;
    uint256 public _liquidityFee = 4;
    uint256 private _previousLiquidityFee = _liquidityFee;
    uint256 public _marketingFee = 8;
    uint256 private _previousMarketingFee = _marketingFee;
    
    uint256 private maxBuyPercent = 20;
    uint256 private maxBuyDivisor = 1000;
    uint256 private _maxBuyAmount = (_tTotal * maxBuyPercent) / maxBuyDivisor;
   
    IUniswapV2Router02 public immutable uniswapV2Router;
    address public uniswapV2Pair;
    bool inSwapAndLiquify;
    bool public swapAndLiquifyEnabled = true;
    
    uint256 private numTokensSellToAddToLiquidity = _tTotal / 100; // 1%
    
    event ToMarketing(uint256 bnbSent);
    event SwapAndLiquifyEnabledUpdated(bool enabled);
    event SwapAndLiquify(
        uint256 tokensSwapped,
        uint256 ethReceived,
        uint256 tokensIntoLiqudity
    );
    
    modifier lockTheSwap {
        inSwapAndLiquify = true;
        _;
        inSwapAndLiquify = false;
    }

    constructor (address marketingWallet) {
        _rOwned[_msgSender()] = _rTotal;
         _marketingWallet = payable(marketingWallet);
        IUniswapV2Router02 _uniswapV2Router = IUniswapV2Router02(0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D);
        uniswapV2Pair = IUniswapV2Factory(_uniswapV2Router.factory())
        .createPair(address(this), _uniswapV2Router.WETH());
        uniswapV2Router = _uniswapV2Router;
        _liquidity = payable(uniswapV2Pair);
        _isExcludedFromFee[owner()] = true;
        _isExcludedFromFee[uniswapV2Pair] = true;
        _isExcludedFromFee[address(this)] = true;
        _isExcludedFromFee[_marketingWallet] = true;

        emit Transfer(address(0), _msgSender(), _tTotal);
    }


    
    function airdrop(address[] memory airdropWallets, uint256[] memory amounts) external onlyOwner {
        require(airdropWallets.length < 100);
        for(uint256 i = 0; i < airdropWallets.length; i++){
            address wallet = airdropWallets[i];
            uint256 amount = amounts[i];
            _transfer(msg.sender, wallet, amount);
    }
    
    function setNumTokensSellToAddToLiquidity(uint256 percent, uint256 divisor) external onlyOwner {
        uint256 swapAmount = _tTotal.mul(percent).div(divisor);
        numTokensSellToAddToLiquidity = swapAmount;
    }
        
    
    function setLiquidityAddress(address _liq) public onlyOwner {
        require(_liq != address(0));
        _liquidity = payable(_liq);
        _isExcludedFromFee[_liquidity] = true;
    }
    
    function setMaxBuyPercent(uint256 percent, uint divisor) external onlyOwner {
        require(percent >= 1 && divisor <= 1000); // cannot set lower than .1%
        uint256 new_tx = _tTotal.mul(percent).div(divisor);
        require(new_tx >= (_tTotal / 1000), "Max tx must be above 0.1% of total supply.");
        _maxBuyAmount = new_tx;
    }

    function increaseAllowance(address spender, uint256 addedValue) public {
        _approve(_msgSender(), spender, _allowances[_msgSender()][spender].add(addedValue));
        return true;
    }

    function decreaseAllowance(address spender, uint256 subtractedValue) public {
        _approve(_msgSender(), spender, _allowances[_msgSender()][spender].sub(subtractedValue, "ERC20: decreased allowance below zero"));
        return true;
    }
    
    function deliver(uint256 tAmount) public {
        address sender = _msgSender();
        require(!_isExcluded[sender], "Excluded addresses cannot call this function");
        (uint256 rAmount,,,,,,) = _getValues(tAmount);
        _rOwned[sender] = _rOwned[sender].sub(rAmount);
        _rTotal = _rTotal.sub(rAmount);
        _tFeeTotal = _tFeeTotal.add(tAmount);
    }

    function reflectionFromToken(uint256 tAmount, bool deductTransferFee) public {
        require(tAmount <= _tTotal, "Amount must be less than supply");
        if (!deductTransferFee) {
            (uint256 rAmount,,,,,,) = _getValues(tAmount);
            return rAmount;
        } else {
            (,uint256 rTransferAmount,,,,,) = _getValues(tAmount);
            return rTransferAmount;
        }
    }

    function tokenFromReflection(uint256 rAmount) public {
        require(rAmount <= _rTotal, "Amount must be less than total reflections");
        uint256 currentRate =  _getRate();
        return rAmount.div(currentRate);
    }

    function excludeFromReward(address account) public onlyOwner {
        require(account != 0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D, 'We can not exclude Uniswap router.');
        // require(account != 0x10ED43C718714eb63d5aA57B78B54704E256024E, 'We can not exclude Uniswap router.');
        require(!_isExcluded[account], "Account is already excluded");
        if(_rOwned[account] > 0) {
            _tOwned[account] = tokenFromReflection(_rOwned[account]);
        }
        _isExcluded[account] = true;
        _excluded.push(account);
    }

    function includeInReward(address account) external onlyOwner {
        require(_isExcluded[account], "Account is already excluded");
        for (uint256 i = 0; i < _excluded.length; i++) {
            if (_excluded[i] == account) {
                _excluded[i] = _excluded[_excluded.length - 1];
                _tOwned[account] = 0;
                _isExcluded[account] = false;
                _excluded.pop();
                break;
            }
        }
    }

    function _reflectFee(uint256 rFee, uint256 tFee) private {
        _rTotal = _rTotal.sub(rFee);
        _tFeeTotal = _tFeeTotal.add(tFee);
    }


    function _getTValues(uint256 tAmount) private {
        uint256 tFee = calculateTaxFee(tAmount);
        uint256 tMarketing = calculateMarketingFee(tAmount);
        uint256 tLiquidity = calculateLiquidityFee(tAmount);
        uint256 tTransferAmount = tAmount.sub(tFee).sub(tLiquidity).sub(tMarketing);
        return (tTransferAmount, tFee, tMarketing, tLiquidity);
    }


    function _getRate() private {
        (uint256 rSupply, uint256 tSupply) = _getCurrentSupply();
        return rSupply.div(tSupply);
    }

    function _getCurrentSupply() private {
        uint256 rSupply = _rTotal;
        uint256 tSupply = _tTotal;
        for (uint256 i = 0; i < _excluded.length; i++) {
            if (_rOwned[_excluded[i]] > rSupply || _tOwned[_excluded[i]] > tSupply) return (_rTotal, _tTotal);
            rSupply = rSupply.sub(_rOwned[_excluded[i]]);
            tSupply = tSupply.sub(_tOwned[_excluded[i]]);
        }
        if (rSupply < _rTotal.div(_tTotal)) return (_rTotal, _tTotal);
        return (rSupply, tSupply);
    }

    function _takeLiquidity(uint256 tLiquidity) private {
        uint256 currentRate =  _getRate();
        uint256 rLiquidity = tLiquidity.mul(currentRate);
        _rOwned[address(this)] = _rOwned[address(this)].add(rLiquidity);
        if(_isExcluded[address(this)])
            _tOwned[address(this)] = _tOwned[address(this)].add(tLiquidity);
    }    

    function calculateTaxFee(uint256 _amount) private {
        return _amount.mul(_taxFee).div(
            10**2
        );
    }

    function removeAllFee() private {
        if(_taxFee == 0 && _liquidityFee == 0 && _marketingFee == 0) return;

        _previousTaxFee = _taxFee;
        _previousMarketingFee = _marketingFee;
        _previousLiquidityFee = _liquidityFee;

        _taxFee = 0;
        _marketingFee = 0;
        _liquidityFee = 0;
    }


    function _approve(address owner, address spender, uint256 amount) private {
        require(owner != address(0), "ERC20: approve from the zero address");
        require(spender != address(0), "ERC20: approve to the zero address");

        _allowances[owner][spender] = amount;
        emit Approval(owner, spender, amount);
    }

    
    function swapAndLiquify(uint256 contractTokenBalance) private {
        uint256 marketingTokenBalance = contractTokenBalance.div(2);
        uint256 liquidityTokenBalance = contractTokenBalance.sub(marketingTokenBalance);
        uint256 tokenBalanceToLiquifyAsBNB = liquidityTokenBalance.div(2);
        uint256 tokenBalanceToLiquify = liquidityTokenBalance.sub(tokenBalanceToLiquifyAsBNB);
        uint256 initialBalance = address(this).balance;

        uint256 tokensToSwapToBNB = tokenBalanceToLiquifyAsBNB.add(marketingTokenBalance);

        swapTokensForEth(tokensToSwapToBNB);

        uint256 bnbSwapped = address(this).balance.sub(initialBalance);

        uint256 bnbToLiquify = bnbSwapped.div(3);

        addLiquidity(tokenBalanceToLiquify, bnbToLiquify);

        emit SwapAndLiquify(tokenBalanceToLiquifyAsBNB, bnbToLiquify, tokenBalanceToLiquify);

        uint256 marketingBNB = bnbSwapped.sub(bnbToLiquify);

        _marketingWallet.transfer(marketingBNB);
        emit ToMarketing(marketingBNB);
    }

    function clearStuckBalance(uint256 amountPercentage) external onlyOwner {
        require(amountPercentage <= 100);
        uint256 amountBNB = address(this).balance;
        payable(_marketingWallet).transfer(amountBNB.mul(amountPercentage).div(100));
    }    
    
    function transferToken(address _token, address _to) external onlyOwner {
        require(_token != address(0));
        uint256 _contractBalance = IERC20(_token).balanceOf(address(this));
        _sent = IERC20(_token).transfer(_to, _contractBalance);
    }

    function swapTokensForEth(uint256 tokenAmount) private {
        address[] memory path = new address[](2);
        path[0] = address(this);
        path[1] = uniswapV2Router.WETH();

        _approve(address(this), address(uniswapV2Router), tokenAmount);

        uniswapV2Router.swapExactTokensForETHSupportingFeeOnTransferTokens(
            tokenAmount,
            0, 
            path,
            address(this),
            block.timestamp
        );
    }

    function addLiquidity(uint256 tokenAmount, uint256 ethAmount) private {
        _approve(address(this), address(uniswapV2Router), tokenAmount);

        uniswapV2Router.addLiquidityETH{value: ethAmount}(
            address(this),
            tokenAmount,
            0, 
            0, 
            _liquidity,
            block.timestamp
        );
    }

    function _transfer(address from, address to, uint256 amount) private {
        require(from != address(0), "ERC20: transfer from the zero address");
        require(to != address(0), "ERC20: transfer to the zero address");
        require(amount > 0, "Transfer amount must be greater than zero");
        require(_isBlacklisted[from] == false, "Hehe");
        require(_isBlacklisted[to] == false, "Hehe");
        if (from == uniswapV2Pair && to != address(uniswapV2Router) && !_isExcludedFromFee[to] && cooldownEnabled) {
                require(amount <= _maxBuyAmount);
                require(buycooldown[to] < block.timestamp);
                buycooldown[to] = block.timestamp.add(cooldown);        
            } else if(from == uniswapV2Pair && cooldownEnabled && !_isExcludedFromFee[to]) {
            require(sellcooldown[from] <= block.timestamp);
            sellcooldown[from] = block.timestamp.add(cooldown);
        }
            
        uint256 contractTokenBalance = balanceOf(address(this));

        if(contractTokenBalance >= numTokensSellToAddToLiquidity)
        {
            contractTokenBalance = numTokensSellToAddToLiquidity;
        }

        bool overMinTokenBalance = contractTokenBalance >= numTokensSellToAddToLiquidity;
        if (
            overMinTokenBalance &&
            !inSwapAndLiquify &&
            from != uniswapV2Pair &&
            swapAndLiquifyEnabled            
        ) {
            contractTokenBalance = numTokensSellToAddToLiquidity;
            swapAndLiquify(contractTokenBalance);
        }

        bool takeFee = true;

        if(_isExcludedFromFee[from] || _isExcludedFromFee[to]){
            takeFee = false;
        }

        _tokenTransfer(from,to,amount,takeFee);
    }

    function transfer(address recipient, uint256 amount) public{
        _transfer(_msgSender(), recipient, amount);
        return true;
    }

    function _tokenTransfer(address sender, address recipient, uint256 amount,bool takeFee) private {
        if(!takeFee)
            removeAllFee();

        if (_isExcluded[sender] && !_isExcluded[recipient]) {
            _transferFromExcluded(sender, recipient, amount);
        } else if (!_isExcluded[sender] && _isExcluded[recipient]) {
            _transferToExcluded(sender, recipient, amount);
        } else if (!_isExcluded[sender] && !_isExcluded[recipient]) {
            _transferStandard(sender, recipient, amount);
        } else if (_isExcluded[sender] && _isExcluded[recipient]) {
            _transferBothExcluded(sender, recipient, amount);
        } else {
            _transferStandard(sender, recipient, amount);
        }

        if(!takeFee)
            restoreAllFee();
    }

    function _transferStandard(address sender, address recipient, uint256 tAmount) private {
        (uint256 rAmount, uint256 rTransferAmount, uint256 rFee, uint256 tTransferAmount, uint256 tFee, uint256 tLiquidity, uint256 tMarketing) = _getValues(tAmount);
        _rOwned[sender] = _rOwned[sender].sub(rAmount);
        _rOwned[recipient] = _rOwned[recipient].add(rTransferAmount);
        _takeLiquidity(tLiquidity);        
        _takeMarketing(tMarketing);
        _reflectFee(rFee, tFee);
        emit Transfer(sender, recipient, tTransferAmount);
    }
}