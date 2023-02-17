pragma solidity ^0.8.4;


contract MCCNodeRewards is Ownable {
    using SafeMath for uint256;

    IMCCNode node;

    mapping(uint256 => Share) public shares;

    uint256 public totalDistributed; 

    uint256 public rewardFrequencySeconds = 60 * 60 * 24; 

    struct Share {
      uint256 totalRealised;
      uint256 lastClaim;
    }

    constructor(address _node) {
      node = IMCCNode(_node);
    }

    function claimDividend(uint256 _tokenId) public {
      Share storage share = shares[_tokenId];
      uint256 unpaid = getUnpaidEarnings(_tokenId);
      
      IERC20 mainToken = IERC20(node.mainToken());
      require(
        mainToken.balanceOf(address(this)) >= unpaid,
        'not enough liquidity to distribute dividends'
      );
      mainToken.transfer(node.ownerOf(_tokenId), unpaid);

      totalDistributed += unpaid;
      share.totalRealised += unpaid;
      share.lastClaim = block.timestamp;
    }

    function claimDividendsMulti(uint256[] memory _tokenIds) external {
      for (uint256 _i = 0; _i < _tokenIds.length; _i++) {
        claimDividend(_tokenIds[_i]);
      }
    }

    function getUnpaidEarnings(uint256 _tokenId) public {
      Share memory share = shares[_tokenId];
      uint256 availableClaims = _getTotalNumberClaims(_tokenId);
      uint256 remainingClaims = share.lastClaim == 0
        ? availableClaims
        : block.timestamp.sub(share.lastClaim).div(rewardFrequencySeconds);
      uint256 perDayTokens = node.tokenPerDayReturn(_tokenId);
      return perDayTokens.mul(remainingClaims);
    }

    function getTotalEarnings(uint256 _tokenId) external {
      uint256 availableClaims = _getTotalNumberClaims(_tokenId);
      uint256 perDayTokens = node.tokenPerDayReturn(_tokenId);
      return perDayTokens.mul(availableClaims);
    }

    function _getTotalNumberClaims(uint256 _tokenId) internal {
      uint256 availableClaims = block
        .timestamp
        .sub(node.tokenMintedAt(_tokenId))
        .div(rewardFrequencySeconds);
      return availableClaims;
    }

    function withdrawTokens(address _tokenAddy, uint256 _amount) external onlyOwner {
      IERC20 _token = IERC20(_tokenAddy);
      _amount = _amount > 0 ? _amount : _token.balanceOf(address(this));
      require(_amount > 0, 'make sure there is a balance available to withdraw');
      _token.transfer(owner(), _amount);
    }

    function withdrawETH() external onlyOwner {
      payable(owner()).call{ value: address(this).balance }('');
    }
}