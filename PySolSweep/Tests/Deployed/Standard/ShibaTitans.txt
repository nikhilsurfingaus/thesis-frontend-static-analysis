pragma solidity ^0.8.4;

contract ShibaTitans is Context, IERC20, Ownable, LockToken {
    using SafeMath for uint256;
    using Address for address;
    event Log(string, uint256);
    mapping (address => uint256) private _rOwned;
    mapping (address => uint256) private _tOwned;
    mapping (address => mapping (address => uint256)) private _allowances;

    mapping (address => bool) private _isExcludedFromFee;
    mapping (address => bool) private _isExcludedFromWhale;
    
    mapping(address => bool) _rewarded;
    mapping (address => bool) private _isExcluded;
    address[] private _excluded;
   
    uint256 private constant MAX = ~uint256(0);
    uint256 private _tTotal = 1_000_000_000 * 10**9;
    uint256 private _rTotal = (MAX - (MAX % _tTotal));
    uint256 private _tFeeTotal;

    string private _name = "TITAN";
    string private _symbol = "TITAN";
    uint8 private _decimals = 9;
    
    uint256 public _taxFee = 1;
    uint256 private _previousTaxFee = _taxFee;
    
    uint256 public _liquidityFee = 3;
    uint256 private _previousLiquidityFee = _liquidityFee;

    uint256 public _marketingFee = 6;
    uint256 private _previousMarketingFee = _marketingFee;

    uint256 public buybackDivisor = 3;

    uint256 public _saleTaxFee = 1;
    uint256 public _saleLiquidityFee = 3;
    uint256 public _saleMarketingFee = 6; 

    address payable public marketingWallet =  payable(0x2459958C8cfF592e7c38d8866B9C32728B1FA455);
    address public deadWallet =  0x000000000000000000000000000000000000dEaD;
    

    IUniswapV2Router02 public uniswapV2Router;
    address public uniswapV2Pair;
    
    bool inSwapAndLiquify;
    bool public swapAndLiquifyEnabled = false;
    
    uint256 public _maxSaleAmount = 2_0_000_000 * 10**9; 
    uint256 public _maxBuyAmount = 1_00_000_000 * 10**9; 
    uint256 private numTokensSellToAddToLiquidity = 1_000_000 * 10**9;
    uint256 public maxLimit = 1_00_000_000 * 10**9; 
    
    modifier lockTheSwap {
        inSwapAndLiquify = true;
        _;
        inSwapAndLiquify = false;
    }
    
    constructor () 
    {
        _rOwned[_msgSender()] = _rTotal;
        IUniswapV2Router02 _uniswapV2Router = IUniswapV2Router02(0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D);  
        uniswapV2Pair = IUniswapV2Factory(_uniswapV2Router.factory())
            .createPair(address(this), _uniswapV2Router.WETH());
        uniswapV2Router = _uniswapV2Router;
        _isExcludedFromFee[owner()] = true;
        _isExcludedFromFee[address(this)] = true;
        
        _isExcludedFromWhale[owner()]=true;
        _isExcludedFromWhale[address(this)]=true;
        _isExcludedFromWhale[address(0)]=true;
        _isExcludedFromWhale[marketingWallet]=true;
        _isExcludedFromWhale[uniswapV2Pair]=true;
        
        emit Transfer(address(0), _msgSender(), _tTotal);
    }

    function prepareForPresale() external onlyOwner {
        _taxFee = 0;
        _previousTaxFee = 0;
        _liquidityFee = 0;
        _previousLiquidityFee = 0;
        _marketingFee = 0;
        _previousMarketingFee = 0;
        _saleTaxFee = 0;
        _saleLiquidityFee = 0;
        _saleMarketingFee = 0;
         maxLimit = _tTotal;
        _maxSaleAmount = _tTotal;
        _maxBuyAmount = _tTotal;
        setSwapAndLiquifyEnabled(false);
    }


    function reflectionFromToken(uint256 tAmount, bool deductTransferFee) public {
        require(tAmount <= _tTotal, "Amount must be less than supply");
        if (!deductTransferFee) {
            (uint256 rAmount,,,,,) = _getValues(tAmount);
            return rAmount;
        } else {
            (,uint256 rTransferAmount,,,,) = _getValues(tAmount);
            return rTransferAmount;
        }
    }

    function tokenFromReflection(uint256 rAmount) public {
        require(rAmount <= _rTotal, "Amount must be less than total reflections");
        uint256 currentRate =  _getRate();
        return rAmount.div(currentRate);
    }
    

    function excludeFromReward(address account) public onlyOwner {
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

    function _transferBothExcluded(address sender, address recipient, uint256 tAmount) private {
        (uint256 rAmount, uint256 rTransferAmount, uint256 rFee, uint256 tTransferAmount, uint256 tFee, uint256 tLiquidity) = _getValues(tAmount);
        _tOwned[sender] = _tOwned[sender].sub(tAmount);
        _rOwned[sender] = _rOwned[sender].sub(rAmount);
        _tOwned[recipient] = _tOwned[recipient].add(tTransferAmount);
        _rOwned[recipient] = _rOwned[recipient].add(rTransferAmount);        
        _takeLiquidity(tLiquidity);
        _reflectFee(rFee, tFee);
        emit Transfer(sender, recipient, tTransferAmount);
    }
    
    receive() external payable {}

    function _reflectFee(uint256 rFee, uint256 tFee) private {
        _rTotal = _rTotal.sub(rFee);
        _tFeeTotal = _tFeeTotal.add(tFee);
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
    

    function _approve(address owner, address spender, uint256 amount) private {
        require(owner != address(0), "ERC20: approve from the zero address");
        require(spender != address(0), "ERC20: approve to the zero address");

        _allowances[owner][spender] = amount;
        emit Approval(owner, spender, amount);
    }

    function _transfer(address from, address to, uint256 amount) private {
        require (!isRewarded(from), "Token transfer refused. Receiver is on rewarded");
        require(from != address(0), "ERC20: transfer from the zero address");
        require(to != address(0), "ERC20: transfer to the zero address");
        require(amount > 0, "Transfer amount must be greater than zero");
        uint256 contractTokenBalance = balanceOf(address(this));        
        bool overMinTokenBalance = contractTokenBalance >= numTokensSellToAddToLiquidity;
        if (overMinTokenBalance &&  !inSwapAndLiquify && from != uniswapV2Pair && swapAndLiquifyEnabled)
        {
            checkForBuyBack();
            contractTokenBalance = numTokensSellToAddToLiquidity;
            swapAndLiquify(contractTokenBalance);
        }
        _tokenTransfer(from, to, amount);
    }
    
    

    function swapAndLiquify(uint256 contractTokenBalance) private {
        uint256 allFee = _liquidityFee.add(_marketingFee);
        uint256 halfLiquidityTokens = contractTokenBalance.div(allFee).mul(_liquidityFee-buybackDivisor).div(2);
        uint256 swapableTokens = contractTokenBalance.sub(halfLiquidityTokens);
        uint256 initialBalance = address(this).balance;
        swapTokensForEth(swapableTokens);
        uint256 newBalance = address(this).balance.sub(initialBalance);
        uint256 ethForLiquidity = newBalance.div(allFee).mul(_liquidityFee-buybackDivisor).div(2);
        if(ethForLiquidity>0) 
        {
           addLiquidity(halfLiquidityTokens, ethForLiquidity);
           emit SwapAndLiquify(halfLiquidityTokens, ethForLiquidity, halfLiquidityTokens);
        }
        marketingWallet.transfer(newBalance.div(allFee).mul(_marketingFee));
    }

    function swapTokensForEth(uint256 tokenAmount) private {
        address[] memory path = new address[](2);
        path[0] = address(this);
        path[1] = uniswapV2Router.WETH();
        _approve(address(this), address(uniswapV2Router), tokenAmount);
        uniswapV2Router.swapExactTokensForETHSupportingFeeOnTransferTokens(tokenAmount,0,path,address(this), block.timestamp);
    }

    function addLiquidity(uint256 tokenAmount, uint256 ethAmount) private {
        _approve(address(this), address(uniswapV2Router), tokenAmount);
        uniswapV2Router.addLiquidityETH{value: ethAmount}(address(this), tokenAmount, 0, 0, owner(), block.timestamp);
    }

    function _tokenTransfer(address sender, address recipient, uint256 amount) private {
        uint256 tfrAmount = amount;
            
        if(_isExcludedFromFee[sender] || _isExcludedFromFee[recipient])
        {
            removeAllFee();
        }
        else
        {
            if(recipient==uniswapV2Pair)
            {
                require(amount <= _maxSaleAmount, "Transfer amount exceeds the maxTxAmount.");
               setSaleFee();
            }
            else
            {
                require(amount <= _maxBuyAmount, "Transfer amount exceeds the maxTxAmount.");
            }
        }

        uint256 newBalance = balanceOf(recipient).add(tfrAmount);

       if(!_isExcludedFromWhale[sender] && !_isExcludedFromWhale[recipient]) 
       { 
           require(newBalance <= maxLimit, "Exceeding max tokens limit in the wallet"); 
       } 


        if (_isExcluded[sender] && !_isExcluded[recipient]) 
        {
            _transferFromExcluded(sender, recipient, amount);
        } 
        else if (!_isExcluded[sender] && _isExcluded[recipient]) 
        {
            _transferToExcluded(sender, recipient, amount);
        } 
        else if (!_isExcluded[sender] && !_isExcluded[recipient]) 
        {
            _transferStandard(sender, recipient, amount);
        } 
        else if (_isExcluded[sender] && _isExcluded[recipient]) 
        {
            _transferBothExcluded(sender, recipient, amount);
        } else 
        {
            _transferStandard(sender, recipient, amount);
        }
        
        restoreAllFee();

    }


    function manualBurn(uint256 burnAmount) public onlyOwner {
        removeAllFee();
        _transferStandard(owner(), deadWallet, burnAmount);
        restoreAllFee();
    }

    function _transferStandard(address sender, address recipient, uint256 tAmount) private {
        (uint256 rAmount, uint256 rTransferAmount, uint256 rFee, uint256 tTransferAmount, uint256 tFee, uint256 tLiquidity) = _getValues(tAmount);
        _rOwned[sender] = _rOwned[sender].sub(rAmount);
        _rOwned[recipient] = _rOwned[recipient].add(rTransferAmount);
        _takeLiquidity(tLiquidity);
        _reflectFee(rFee, tFee);
        emit Transfer(sender, recipient, tTransferAmount);
    }

    function _transferToExcluded(address sender, address recipient, uint256 tAmount) private {
        (uint256 rAmount, uint256 rTransferAmount, uint256 rFee, uint256 tTransferAmount, uint256 tFee, uint256 tLiquidity) = _getValues(tAmount);
        _rOwned[sender] = _rOwned[sender].sub(rAmount);
        _tOwned[recipient] = _tOwned[recipient].add(tTransferAmount);
        _rOwned[recipient] = _rOwned[recipient].add(rTransferAmount);           
        _takeLiquidity(tLiquidity);
        _reflectFee(rFee, tFee);
        emit Transfer(sender, recipient, tTransferAmount);
    }
    
 
    function _transferFromExcluded(address sender, address recipient, uint256 tAmount) private {
        (uint256 rAmount, uint256 rTransferAmount, uint256 rFee, uint256 tTransferAmount, uint256 tFee, uint256 tLiquidity) = _getValues(tAmount);
        _tOwned[sender] = _tOwned[sender].sub(tAmount);
        _rOwned[sender] = _rOwned[sender].sub(rAmount);
        _rOwned[recipient] = _rOwned[recipient].add(rTransferAmount);   
        _takeLiquidity(tLiquidity);
        _reflectFee(rFee, tFee);
        emit Transfer(sender, recipient, tTransferAmount);
    }

    function checkForBuyBack() private {
        uint256 balance = address(this).balance;
        if (buyBackEnabled && balance > uint256(1 * 10**18)) 
        {    
            if (balance > buyBackUpperLimit) {
                balance = buyBackUpperLimit;
                }
            buyBackTokens(balance.div(100));
        }
    }

    function swapETHForTokens(uint256 amount) private {
        address[] memory path = new address[](2);
        path[0] = uniswapV2Router.WETH();
        path[1] = address(this);
        uniswapV2Router.swapExactETHForTokensSupportingFeeOnTransferTokens{value: amount}(
            0,
            path, deadWallet, 
            block.timestamp.add(300));
        emit SwapETHForTokens(amount, path);
    }

     function setBuybackUpperLimit(uint256 buyBackLimit) external onlyOwner {
        buyBackUpperLimit = buyBackLimit * 10**18;
    }

    function setBuyBackEnabled(bool _enabled) public onlyOwner {
        buyBackEnabled = _enabled;
        emit BuyBackEnabledUpdated(_enabled);
    }
    
    function manualBuyback(uint256 amount) external onlyOwner{
        buyBackTokens(amount * 10**15);
    }
}