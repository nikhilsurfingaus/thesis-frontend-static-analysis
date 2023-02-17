pragma solidity 0.7.5;

contract rewardPool is Ownable {
    using SafeMath for uint;
    using SafeMath for uint32;
    struct NftData{
        uint nodeType;
        address owner;
        uint256 lastClaim;
    }
    uint256[5] public rewardRates;
    IUniswapV2Router02 public uniswapV2Router;
    mapping (uint => NftData) public nftInfo;
    uint totalNodes = 0;

    constructor(address _sinAddress) {     
        IUniswapV2Router02 _uniswapV2Router = IUniswapV2Router02(0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D);
        uniswapV2Router = _uniswapV2Router;
        Sins = _sinAddress;
    }
    
    receive() external payable {
    }

    function addNodeInfo(uint _nftId, uint _nodeType, address _owner) external {
        require(nftInfo[_nftId].owner == address(0), "Node already exists");
        nftInfo[_nftId].nodeType = _nodeType;
        nftInfo[_nftId].owner = _owner;
        nftInfo[_nftId].lastClaim = block.timestamp;
        totalNodes += 1;
        return true;
    }

    function updateNodeOwner(uint _nftId, address _owner) external {
        require(nftInfo[_nftId].owner != address(0), "Node does not exist");
        nftInfo[_nftId].owner = _owner;
        return true;
    }

    function updateRewardRates(uint256[5] memory _rewardRates) external onlyOwner {
        for (uint i = 1; i < totalNodes; i++) {
            claimReward(i);
        }
        rewardRates = _rewardRates;
    }    

    function pendingRewardFor(uint _nftId) public {
        uint _nodeType = nftInfo[_nftId].nodeType;
        uint _lastClaim = nftInfo[_nftId].lastClaim;
        uint _daysSinceLastClaim = ((block.timestamp - _lastClaim).mul(1e9)) / 86400;
        _reward = (_daysSinceLastClaim * rewardRates[_nodeType-1]).div(1e9);
        return _reward;
    }

    function claimReward(uint _nftId) public {
        uint _reward = pendingRewardFor(_nftId);
        nftInfo[_nftId].lastClaim = block.timestamp;
        IERC20(Sins).transfer(nftInfo[_nftId].owner, _reward);
        return true;
    }
}