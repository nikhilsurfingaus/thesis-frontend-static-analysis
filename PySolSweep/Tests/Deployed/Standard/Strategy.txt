pragma solidity 0.6.12;

contract Strategy is BaseStrategy {
    using SafeERC20 for IERC20;
    using Address for address;
    using SafeMath for uint256;

    address public constant yvBoost        = 0x9d409a0A012CFbA9B15F6D4B36Ac57A46966Ab9a;
    address public constant crv            = 0xD533a949740bb3306d119CC777fa900bA034cd52;
    address public constant usdc           = 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48;
    address public constant crv3           = 0x6c3F90f043a72FA612cbac8115EE7e52BDe6E490;
    address public constant crv3Pool       = 0xbEbc44782C7dB0a1A60Cb6fe97d0b483032FF1C7;
    address public constant weth           = 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2;
    address public constant sushiswap      = 0xd9e1cE17f2641f24aE83637ab66a2cca9C378B9F;
    address public constant ethCrvPair     = 0x58Dc5a51fE44589BEb22E8CE67720B5BC5378009; 
    address public constant ethYvBoostPair = 0x9461173740D27311b176476FA27e94C681b1Ea6b; 
    address public constant ethUsdcPair    = 0x397FF1542f962076d0BFE58eA045FfA2d347ACa0;
    address public proxy                   = 0xA420A63BbEFfbda3B147d0585F1852C358e2C152;


    uint256 public vaultBuffer = 30;
    uint256 internal constant DENOMINATOR = 1000;

    event UpdatedBuffer(uint256 newBuffer);
    event BuyOrMint(bool shouldMint, uint256 projBuyAmount, uint256 projMintAmount);

    constructor(address _vault) public BaseStrategy(_vault) {
        healthCheck = address(0xDDCea799fF1699e98EDF118e0629A974Df7DF012);
        IERC20(crv).safeApprove(address(want), type(uint256).max);
        IERC20(usdc).safeApprove(sushiswap, type(uint256).max);
    }

    function prepareReturn(uint256 _debtOutstanding) internal {
        if (_debtOutstanding > 0) {
            (_debtPayment, _loss) = liquidatePosition(_debtOutstanding);
        }

        uint256 claimable = getClaimable3Crv();
        claimable = claimable > 0 ? claimable : IERC20(crv3).balanceOf(address(this)); 
        uint256 debt = vault.strategies(address(this)).totalDebt;
        if (claimable > 0 || estimatedTotalAssets() > debt) {
            IyveCRV(address(want)).claim();
            withdrawFrom3CrvToUSDC(); 
            uint256 usdcBalance = IERC20(usdc).balanceOf(address(this));
            if(usdcBalance > 0){
                if(shouldMint(usdcBalance)){
                    swap(usdc, crv, usdcBalance);
                    deposityveCRV(); 
                }
                else{
                    uint256 strategistRewards = vault.balanceOf(address(this));
                    swap(usdc, yvBoost, usdcBalance);
                    uint256 swapGain = vault.balanceOf(address(this)).sub(strategistRewards);
                    if(swapGain > 0){
                        vault.withdraw(swapGain);
                        debt = vault.strategies(address(this)).totalDebt;
                    }
                }
            }
            uint256 assets = estimatedTotalAssets();
            if(assets >= debt){
                _profit = assets.sub(debt);
            }
            else{
                _loss = debt.sub(assets);
            }
        }
    }

    function adjustPosition(uint256 _debtOutstanding) internal {
        IVoterProxy(proxy).lock();
    }

    function liquidatePosition(uint256 _amountNeeded) internal {
        uint256 totalAssets = want.balanceOf(address(this));
        if (_amountNeeded > totalAssets) {
            _liquidatedAmount = totalAssets;
            _loss = _amountNeeded.sub(totalAssets);
        } else {
            _liquidatedAmount = _amountNeeded;
        }
    }


    function prepareMigration(address _newStrategy) internal {
        uint256 balance3crv = IERC20(crv3).balanceOf(address(this));
        uint256 balanceYveCrv = IERC20(address(want)).balanceOf(address(this));
        if(balance3crv > 0){
            IERC20(crv3).safeTransfer(_newStrategy, balance3crv);
        }
        if(balanceYveCrv > 0){
            IERC20(address(want)).safeTransfer(_newStrategy, balanceYveCrv);
        }
        IERC20(crv).safeApprove(address(want), 0);
        IERC20(usdc).safeApprove(sushiswap, 0);
    }

    function shouldMint(uint256 _amountIn) internal {
        address[] memory path = new address[](3);
        path[0] = usdc;
        path[1] = weth;
        path[2] = yvBoost;
        uint256[] memory amounts = ISwap(sushiswap).getAmountsOut(_amountIn, path);
        uint256 projectedYvBoost = amounts[2];
        uint256 projectedYveCrv = projectedYvBoost.mul(vault.pricePerShare()).div(1e18);

        path = new address[](3);
        path[0] = usdc;
        path[1] = weth;
        path[2] = crv;
        amounts = ISwap(sushiswap).getAmountsOut(_amountIn, path);
        uint256 projectedCrv = amounts[2];

        bool shouldMint = projectedCrv.mul(DENOMINATOR.add(vaultBuffer)).div(DENOMINATOR) > projectedYveCrv;
        emit BuyOrMint(shouldMint, projectedYveCrv, projectedCrv);

        return shouldMint;
    }

    function withdrawFrom3CrvToUSDC() internal {
        uint256 amount = IERC20(crv3).balanceOf(address(this));
        if(amount > 0){
            ICurveFi(crv3Pool).remove_liquidity_one_coin(amount, 1, 0);
        }
    }

    function getClaimable3Crv() public {
        IyveCRV YveCrv = IyveCRV(address(want));
        uint256 claimable = YveCrv.claimable(address(this));
        uint256 claimableToAdd = (YveCrv.index().sub(YveCrv.supplyIndex(address(this))))
            .mul(YveCrv.balanceOf(address(this)))
            .div(1e18);
        return claimable.mul(1e18).add(claimableToAdd);
    }


    function swap(address token_in, address token_out, uint256 amount_in) internal {
        if(amount_in == 0){
            return;
        }
        bool is_weth = token_in == weth || token_out == weth;
        address[] memory path = new address[](is_weth ? 2 : 3);
        path[0] = token_in;
        if (is_weth) {
            path[1] = token_out;
        } else {
            path[1] = weth;
            path[2] = token_out;
        }
        ISwap(sushiswap).swapExactTokensForTokens(
            amount_in,
            0,
            path,
            address(this),
            now
        );
    }


    function setBuffer(uint256 _newBuffer) external {
        require(_newBuffer < DENOMINATOR);
        vaultBuffer = _newBuffer;
        emit UpdatedBuffer(_newBuffer);
    }

    function restoreApprovals() external {
        IERC20(crv).safeApprove(address(want), 0); 
        IERC20(usdc).safeApprove(sushiswap, 0);
        IERC20(crv).safeApprove(address(want), type(uint256).max);
        IERC20(usdc).safeApprove(sushiswap, type(uint256).max);
    }
}