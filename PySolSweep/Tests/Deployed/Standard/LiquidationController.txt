pragma solidity 0.8.1;

contract LiquidationController is Ownable {
    bdToken public bdUSD;
    bdToken public bdETH;
    IWETH9 constant WETH = IWETH9(payable(0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2));
    IERC20 constant DAI = IERC20(0x6B175474E89094C44Da98b954EedeAC495271d0F);
    IERC20 public bUSD;
    ISwapRouter public swapRouter; 
    ICurve public curvePool; 
    address public Treasury = 0x3dFc49e5112005179Da613BdE5973229082dAc35;

    mapping(address => uint24) poolFee;

    using SafeERC20 for IERC20;

    constructor(address _curvePool, address _bdUSD, address _bdETH, address _bUSD, address _bdUSDC, address _swapRouter){
        curvePool = ICurve(_curvePool);
        bdUSD = bdToken(_bdUSD);
        bdETH = bdToken(_bdETH);
        bUSD = IERC20(_bUSD);
        swapRouter = ISwapRouter(_swapRouter);

        poolFee[_bdUSDC] = 500; 
        poolFee[_bdETH] = 3000; 
    }

    function executeOperation(address[] calldata assets, uint256[] calldata amounts, uint256[] calldata premiums, address initiator, bytes calldata _params) external {

        DAI.approve(address(curvePool), amounts[0]);
        curvePool.exchange_underlying(1,0,amounts[0],0);
        bUSD.approve(address(bdUSD), amounts[0]);
        
        for (uint i = 0; i < _borrowers.length; i++) {
            (uint result) = bdUSD.liquidateBorrow(_borrowers[i], _repayAmounts[i], _bdCollaterals[i]);
            if(result!=0){
                bUSD.approve(address(curvePool), _repayAmounts[i]);
                curvePool.exchange_underlying(0,1,_repayAmounts[i],0);
            }
        }
        
        for (uint j = 0; j < _bdCollaterals.length; j++) {
            bdToken bdCollateral = bdToken(_bdCollaterals[j]);
            uint collateralBalance = bdCollateral.balanceOf(address(this));

            if(collateralBalance == 0 && address(this).balance == 0){
                continue;
            }

            bdCollateral.redeem(collateralBalance);
            ISwapRouter.ExactInputSingleParams memory params;

            if(0 < address(this).balance){

                uint collateralAmount = address(this).balance;

                WETH.deposit{value: collateralAmount}();

                WETH.approve(address(swapRouter), collateralAmount);
                
                params =
                ISwapRouter.ExactInputSingleParams({
                    tokenIn: address(WETH),
                    tokenOut: address(DAI),
                    fee: poolFee[_bdCollaterals[j]],
                    recipient: address(this),
                    deadline: block.timestamp,
                    amountIn: collateralAmount,
                    amountOutMinimum: 0,
                    sqrtPriceLimitX96: 0
                });

            }
            else{
                address underlyingCollateral = bdCollateral.underlying();
                uint collateralAmount = IERC20(underlyingCollateral).balanceOf(address(this));

                IERC20(underlyingCollateral).approve(address(swapRouter), collateralAmount);
                params =
                ISwapRouter.ExactInputSingleParams({
                    tokenIn: underlyingCollateral,
                    tokenOut: address(DAI),
                    fee: poolFee[_bdCollaterals[j]],
                    recipient: address(this),
                    deadline: block.timestamp,
                    amountIn: collateralAmount,
                    amountOutMinimum: 0,
                    sqrtPriceLimitX96: 0
                });
            }
            swapRouter.exactInputSingle(params);
        }
        
        uint totalDebt = amounts[0] + premiums[0];
        DAI.approve(address(LENDING_POOL), totalDebt);
        
        return true;
    }


    function executeLiquidations(address[] memory _borrowers, uint256[] memory _repayAmounts, address[] memory _bdCollaterals, uint256 _totalRepayAmount) external {

        bytes memory params = abi.encode(_borrowers,_repayAmounts,_bdCollaterals);
                                                         
        uint256[] memory amounts = new uint256[](1);
        amounts[0] = _totalRepayAmount;

        address[] memory assets = new address[](1);
        assets[0] = address(DAI);

        uint256[] memory modes = new uint256[](1);
        modes[0] = 0;
        LENDING_POOL.flashLoan(address(this), assets, amounts, modes, address(this), params, 0);

        DAI.safeTransfer(Treasury, DAI.balanceOf(address(this)));
        bUSD.safeTransfer(Treasury, bUSD.balanceOf(address(this)));
    }

    function retrieve(address token, uint256 amount) external onlyOwner {
        IERC20 tokenContract = IERC20(token);
        tokenContract.safeTransfer(msg.sender, amount);
    }

    function updateAddress(address _newAddress, uint8 _index) external onlyOwner(){
        if(_index==0){
            curvePool = ICurve(_newAddress);
            return;
        }
        if(_index==1){
            bUSD = IERC20(_newAddress);
            return;
        }
        if(_index==2){
            bdETH = bdToken(_newAddress);
            return;
        }
        if(_index==3){
            bdUSD = bdToken(_newAddress);
            return;
        }
        if(_index==3){
            swapRouter = ISwapRouter(_newAddress);
            return;
        }
        if(_index==4){
            Treasury = _newAddress;
        }
    }
    receive() external payable {}
}