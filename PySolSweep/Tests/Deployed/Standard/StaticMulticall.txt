pragma solidity ^0.8.4;


contract StaticMulticall {  
    error CallError(bytes err);

    struct Call {
        address target;
        bytes callData;
    }

    struct Result {
        bool success;
        bytes returnData;
    }

    function aggregate(Call[] memory calls) external {
        blockNumber = block.number;
        returnData = new bytes[](calls.length);
        for(uint256 i = 0; i < calls.length; i++) {
            (bool success, bytes memory ret) = calls[i].target.staticcall(calls[i].callData);
            if (!success) {
              revert CallError(ret);
            }
            returnData[i] = ret;
        }
    }
}