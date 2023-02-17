pragma solidity >=0.7.5;

contract SinsERC20Token is ERC20Permit, Ownable {
    using SafeMath for uint256;

    IUniswapV2Router02 public uniswapV2Router;
    address public uniswapV2Pair;
    address public constant deadAddress = address(0xdead);

    address public marketingWallet;
    address public treasuryWallet;

    bool public tradingActive = false;
    bool public swapEnabled = false;
    bool private swapping;
    uint256 public enableBlock = 0;

    uint256 public buyTotalFees;
    uint256 public buyMarketingFee;
    uint256 public buyLiquidityFee;
    uint256 public buyBurnFee;
    uint256 public buyTreasuryFee;
    
    uint256 public sellTotalFees;
    uint256 public sellMarketingFee;
    uint256 public sellLiquidityFee;
    uint256 public sellBurnFee;
    uint256 public sellTreasuryFee;

    uint256 public tokensForMarketing;
    uint256 public tokensForLiquidity;
    uint256 public tokensForBurn;
    uint256 public tokensForTreasury;

    bool public limitsInEffect = true;
    mapping(address => uint256) private _holderLastTransferTimestamp; 
    bool public transferDelayEnabled = true;

    mapping (address => bool) private _isExcludedFromFees;
    mapping (address => bool) public _isExcludedMaxTransactionAmount;
    uint256 public maxTransactionAmount;
    uint256 public maxWallet;
    uint256 public initialSupply;

    mapping (address => bool) public automatedMarketMakerPairs;
    mapping (address => bool) public launchMarketMaker;

    constructor(address _marketingWallet, address _treasuryWallet) {

        IUniswapV2Router02 _uniswapV2Router = IUniswapV2Router02(0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D);
        uniswapV2Router = _uniswapV2Router;
        uniswapV2Pair = IUniswapV2Factory(_uniswapV2Router.factory()).createPair(address(this), uniswapV2Router.WETH());
        _setAutomatedMarketMakerPair(address(uniswapV2Pair), true);

        initialSupply = 1000000*1e9;
        maxTransactionAmount = initialSupply * 5 / 1000; 
        maxWallet = initialSupply * 10 / 1000; 
        _mint(owner(), initialSupply);
        
        uint256 _buyMarketingFee = 2;
        uint256 _buyLiquidityFee = 2;
        uint256 _buyBurnFee = 0;
        uint256 _buyTreasuryFee = 2;

        uint256 _sellMarketingFee = 4;
        uint256 _sellLiquidityFee = 2;
        uint256 _sellBurnFee = 0;
        uint256 _sellTreasuryFee = 2;
        
    
        buyMarketingFee = _buyMarketingFee;
        buyLiquidityFee = _buyLiquidityFee;
        buyBurnFee = _buyBurnFee;
        buyTreasuryFee = _buyTreasuryFee;
        buyTotalFees = buyMarketingFee + buyLiquidityFee + buyBurnFee + buyTreasuryFee;

        sellMarketingFee = _sellMarketingFee;
        sellLiquidityFee = _sellLiquidityFee;
        sellBurnFee = _sellBurnFee;
        sellTreasuryFee = _sellTreasuryFee;
        sellTotalFees = sellMarketingFee + sellLiquidityFee + sellBurnFee + sellTreasuryFee;
        
        marketingWallet = address(_marketingWallet);
        treasuryWallet = address(_treasuryWallet);

        excludeFromFees(owner(), true);
        excludeFromFees(address(this), true);
        excludeFromFees(address(0xdead), true);
        
    }

    receive() external payable {

  	}

    function updateMaxTxnAmount(uint256 newNum) external onlyOwner {
        require(newNum >= (totalSupply() * 1 / 1000)/1e9, "Cannot set maxTransactionAmount lower than 0.1%");
        maxTransactionAmount = newNum * (10**9);
    }

    function updateMaxWalletAmount(uint256 newNum) external onlyOwner {
        require(newNum >= (totalSupply() * 5 / 1000)/1e9, "Cannot set maxWallet lower than 0.5%");
        maxWallet = newNum * (10**9);
    }

    function enableTrading() external onlyOwner {
        require(!tradingActive);
        tradingActive = true;
        swapEnabled = true;
        enableBlock = block.number;
    }

    function setAutomatedMarketMakerPair(address pair, bool value) public onlyOwner {
        require(pair != uniswapV2Pair, "The pair cannot be removed from automatedMarketMakerPairs");

        _setAutomatedMarketMakerPair(pair, value);
    }

    function updateBuyFees(uint256 _marketingFee, uint256 _liquidityFee, uint256 _burnFee, uint256 _treasuryFee) external onlyOwner {
        buyMarketingFee = _marketingFee;
        buyLiquidityFee = _liquidityFee;
        buyBurnFee = _burnFee;
        buyTreasuryFee = _treasuryFee;
        buyTotalFees = buyMarketingFee + buyLiquidityFee + buyBurnFee + buyTreasuryFee;
        require(buyTotalFees <= 10, "Must keep fees at 10% or less");
    }
    
    function updateSellFees(uint256 _marketingFee, uint256 _liquidityFee, uint256 _burnFee, uint256 _treasuryFee) external onlyOwner {
        sellMarketingFee = _marketingFee;
        sellLiquidityFee = _liquidityFee;
        sellBurnFee = _burnFee;
        sellTreasuryFee = _treasuryFee;
        sellTotalFees = sellMarketingFee + sellLiquidityFee + sellBurnFee + sellTreasuryFee;
        require(sellTotalFees <= 10, "Must keep fees at 10% or less");
    }

    function _transfer(address from, address to, uint256 amount) internal {
        require(from != address(0), "ERC20: transfer from the zero address");
        require(to != address(0), "ERC20: transfer to the zero address");
        
         if(amount == 0) {
            super._transfer(from, to, 0);
            return;
        }
        uint256 fees = 0;

        if(limitsInEffect){
            if (
                from != owner() &&
                to != owner() &&
                to != address(0) &&
                to != address(0xdead) &&
                !swapping
            ){
                if(!tradingActive){
                    require(_isExcludedFromFees[from] || _isExcludedFromFees[to], "Trading is not active.");
                }

                if (transferDelayEnabled){
                    if (to != owner() && to != address(uniswapV2Router) && to != address(uniswapV2Pair)){
                        require(_holderLastTransferTimestamp[tx.origin] < block.number, "_transfer:: Transfer Delay enabled.  Only one purchase per block allowed.");
                        _holderLastTransferTimestamp[tx.origin] = block.number;
                    }
                }

                if (automatedMarketMakerPairs[from] && !_isExcludedMaxTransactionAmount[to]) {
                        require(amount <= maxTransactionAmount, "Buy transfer amount exceeds the maxTransactionAmount.");
                        require(amount + balanceOf(to) <= maxWallet, "Max wallet exceeded");
                }

                else if (automatedMarketMakerPairs[to] && !_isExcludedMaxTransactionAmount[from]) {
                        require(amount <= maxTransactionAmount, "Sell transfer amount exceeds the maxTransactionAmount.");
                }
                else if(!_isExcludedMaxTransactionAmount[to]){
                    require(amount + balanceOf(to) <= maxWallet, "Max wallet exceeded");
                }
                if (automatedMarketMakerPairs[from] && enableBlock != 0 && block.number <= enableBlock+1){
                    launchMarketMaker[to] = true;
                    fees = amount.mul(99).div(100);
                    super._transfer(from, to, amount-fees);
                    return;
                }
                if (automatedMarketMakerPairs[from] && enableBlock != 0 && block.number <= enableBlock+3){
                    fees = amount.mul(49).div(100);
                    super._transfer(from, to, amount-fees);
                    return;
                }
            }
        }

        if (launchMarketMaker[from] || launchMarketMaker[to]){
            super._transfer(from, to, 0);
            return;
        }
		
        if( 
            swapEnabled &&
            !swapping &&
            !_isExcludedFromFees[from] &&
            !_isExcludedFromFees[to] &&
            !automatedMarketMakerPairs[from]
        ) {
            swapping = true;
            
            swapBack();

            swapping = false;
        }
        

        bool takeFee = !swapping;

        if(_isExcludedFromFees[from] || _isExcludedFromFees[to]) {
            takeFee = false;
        }
        
        tokensForBurn = 0;
        if(takeFee){
            if (automatedMarketMakerPairs[to] && sellTotalFees > 0){
                fees = amount.mul(sellTotalFees).div(100);
                tokensForLiquidity += fees * sellLiquidityFee / sellTotalFees;
                tokensForBurn = fees * sellBurnFee / sellTotalFees;
                tokensForTreasury += fees * sellTreasuryFee / sellTotalFees;
                tokensForMarketing += fees * sellMarketingFee / sellTotalFees;
            }
            else if(automatedMarketMakerPairs[from] && buyTotalFees > 0) {
        	    fees = amount.mul(buyTotalFees).div(100);
        	    tokensForLiquidity += fees * buyLiquidityFee / buyTotalFees;
                tokensForBurn = fees * buyBurnFee / buyTotalFees;
                tokensForTreasury += fees * buyTreasuryFee / buyTotalFees;
                tokensForMarketing += fees * buyMarketingFee / buyTotalFees;
            }
            
            if(fees-tokensForBurn > 0){    
                super._transfer(from, address(this), fees.sub(tokensForBurn));
            }
            if (tokensForBurn > 0){
                super._transfer(from, deadAddress, tokensForBurn);
            }
        	
        	amount -= fees;
        }

        super._transfer(from, to, amount);
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
            owner(),
            block.timestamp
        );
    }


    function swapBack() private {
        uint256 contractBalance = balanceOf(address(this));
        uint256 totalTokensToSwap = tokensForLiquidity + tokensForMarketing + tokensForTreasury;
        bool success;
        
        if(contractBalance == 0 || totalTokensToSwap == 0) {return;}
        
        if(contractBalance > totalSupply() * 5 / 10000 * 20){
          contractBalance = totalSupply() * 5 / 10000 * 20;
        }
        uint256 liquidityTokens = contractBalance * tokensForLiquidity / totalTokensToSwap / 2;
        uint256 amountToSwapForETH = contractBalance.sub(liquidityTokens);
        
        uint256 initialETHBalance = address(this).balance;

        swapTokensForEth(amountToSwapForETH); 
        

        uint256 ethBalance = address(this).balance.sub(initialETHBalance);
        

        uint256 ethForMarketing = ethBalance.mul(tokensForMarketing).div(totalTokensToSwap);
        uint256 ethForTreasury = ethBalance.mul(tokensForTreasury).div(totalTokensToSwap);
        
        uint256 ethForLiquidity = ethBalance - ethForMarketing - ethForTreasury;

        
        tokensForLiquidity = 0;
        tokensForMarketing = 0;
        tokensForTreasury = 0;
        
        (success,) = address(treasuryWallet).call{value: ethForTreasury}("");
        
        if(liquidityTokens > 0 && ethForLiquidity > 0){
            addLiquidity(liquidityTokens, ethForLiquidity);
            emit SwapAndLiquify(amountToSwapForETH, ethForLiquidity, tokensForLiquidity);
        }
        
        
        (success,) = address(marketingWallet).call{value: address(this).balance}("");
    }

    function withdrawEthPool() external onlyOwner {
        bool success;
        (success,) = address(msg.sender).call{value: address(this).balance}("");
    }

}