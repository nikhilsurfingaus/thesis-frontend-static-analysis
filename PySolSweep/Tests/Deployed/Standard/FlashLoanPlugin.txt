pragma solidity 0.6.12;

contract FlashLoanPlugin is ICallee, DydxFlashloanBase {
    using SafeERC20 for IERC20;
    using SafeMath for uint256;

    IERC20 internal want;
    address internal SOLO;
    IStrategy internal strategy;

    bool internal awaitingFlash = false;

    uint256 public dyDxMarketId;

    event Leverage(uint256 amountRequested, uint256 amountGiven, bool deficit, address flashLoan);

    constructor (address _strategy) public {
        strategy = IStrategy(_strategy);

        want = IERC20(strategy.want());
        want.approve(_strategy, uint256(-1));
        want.safeApprove(SOLO, type(uint256).max);
    }

    function updateMarketId() external {
        require(msg.sender == address(strategy));
        _setMarketIdFromTokenAddress();
    }

    function setSOLO(address _solo) external {   
        require(msg.sender == address(strategy));
        want.approve(SOLO, 0);
        SOLO = _solo;
        want.approve(SOLO, uint256(-1));
    }

    function doDyDxFlashLoan(bool _deficit, uint256 _amountDesired) external {
        require(msg.sender == address(strategy), "not strategy!");
        uint256 amount = _amountDesired;
        ISoloMargin solo = ISoloMargin(SOLO);

        uint256 amountInSolo = want.balanceOf(SOLO);
        if (amountInSolo < amount) {
            amount = amountInSolo;
        }
        uint256 repayAmount = amount.add(2); 

        bytes memory data = abi.encode(_deficit, amount, repayAmount);

        Actions.ActionArgs[] memory operations = new Actions.ActionArgs[](3);

        operations[0] = _getWithdrawAction(dyDxMarketId, amount);
        operations[1] = _getCallAction(
            data
        );
        operations[2] = _getDepositAction(dyDxMarketId, repayAmount);

        Account.Info[] memory accountInfos = new Account.Info[](1);
        accountInfos[0] = _getAccountInfo();
        
        solo.operate(accountInfos, operations);

        emit Leverage(_amountDesired, amount, _deficit, SOLO);

        return amount;
    }
    
    function _setMarketIdFromTokenAddress() internal {
        ISoloMargin solo = ISoloMargin(SOLO);

        uint256 numMarkets = solo.getNumMarkets();

        address curToken;
        for (uint256 i = 0; i < numMarkets; i++) {
            curToken = solo.getMarketTokenAddress(i);

            if (curToken == address(want)) {
                dyDxMarketId = i;
                return;
            }
        }

        revert("No marketId found for provided token");
    }

    function callFunction(address sender, Account.Info memory account, bytes memory data) external {
        (bool deficit, uint256 amount, uint256 repayAmount) = abi.decode(data, (bool, uint256, uint256));
        require(msg.sender == SOLO, "NOT_SOLO");

        _loanLogic(deficit, amount, repayAmount);    
    }

    function _loanLogic(bool deficit, uint256 amount, uint256 repayAmount) internal {   
        want.transfer(address(strategy), want.balanceOf(address(this)));
        strategy.useLoanTokens(deficit, amount, repayAmount);
    }
}