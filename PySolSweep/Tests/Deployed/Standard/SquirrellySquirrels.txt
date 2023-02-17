
pragma solidity ^0.8.0;

contract SquirrellySquirrels  {
    using SafeMath for uint256;

    uint256 public constant NFT_1_PRICE = 0.16 ether;
    uint256 public constant NFT_3_PRICE = 0.39 ether;
    uint256 public constant NFT_5_PRICE = 0.45 ether;
    uint256 public constant MAX_NFT_PURCHASE_PRESALE = 5;
    uint256 public constant MAX_MINT_PER_TX = 5;
    uint256 public constant MAX_SUPPLY = 10000;

    bool public saleIsActive = false;
    bool public presaleIsActive = false;

    bool public revealed = false;

    uint256 public reserve = 300;
    uint256 public startingIndex;

    mapping(address => uint256) public allowListNumClaimed;
    bytes32 public allowListMerkleRoot;
    bytes32 public startingIndexRequestId;

    string public uriPrefix = "";
    string public uriSuffix = ".json";
    string public hiddenMetadataUri = "";
    string public provenance;

    string private _baseURIExtended;

    modifier mintCompliance(uint256 _numberOfTokens) {
      require(
        _numberOfTokens > 0 &&
          _numberOfTokens != 2 &&
          _numberOfTokens != 4 &&
          _numberOfTokens <= MAX_MINT_PER_TX,
        "Invalid mint amount"
      );

      require(
        (_numberOfTokens == 1 && msg.value == NFT_1_PRICE) ||
          (_numberOfTokens == 3 && msg.value == NFT_3_PRICE) ||
          (_numberOfTokens == 5 && msg.value == NFT_5_PRICE),
        "Sent ether value is incorrect"
      );

      _;
    }

    constructor() {}
      transferOwnership(_owner);
    }

    function requestStartingIndex(bytes32 _keyHash, uint256 _fee) external onlyOwner  {
      require(startingIndex == 0, "startingIndex has already been set");
      bytes32 _requestId = requestRandomness(_keyHash, _fee);
      startingIndexRequestId = _requestId;
      return _requestId;
    }

    function fulfillRandomness(bytes32 _requestId, uint256 _randomness) internal {
      if (startingIndexRequestId == _requestId) {
        startingIndex = _randomness % MAX_SUPPLY;
      }
    }

    function claimReserve(address _to, uint256 _reserveAmount) external onlyOwner {
      require(
        _reserveAmount > 0 && _reserveAmount <= reserve,
        "Not enough reserve left for team"
      );

      reserve = reserve - _reserveAmount;

      _safeMint(_to, _reserveAmount);
    }

    function flipSaleState() external onlyOwner {
      saleIsActive = !saleIsActive;
    }

    function flipPresaleState() external onlyOwner {
      presaleIsActive = !presaleIsActive;
    }

    function isAllowListed(bytes32[] memory _proof, address _address) public {
      require(_address != address(0), "Zero address not on Allow List");

      bytes32 leaf = keccak256(abi.encodePacked(_address));
      return MerkleProof.verify(_proof, allowListMerkleRoot, leaf);
    }

    function setAllowListMerkleRoot(bytes32 _allowListMerkleRoot) external onlyOwner {
      allowListMerkleRoot = _allowListMerkleRoot;
    }

    function mintPresale(bytes32[] memory _proof, uint256 _numberOfTokens) external {
      require(presaleIsActive, "Presale is not active at the moment");
      require(
        isAllowListed(_proof, msg.sender),
        "This address is not allow listed for the presale"
      );
      require(
        allowListNumClaimed[msg.sender] + _numberOfTokens <=
          MAX_NFT_PURCHASE_PRESALE,
        "Exceeds allowed presale you can mint"
      );
      require(
        totalSupply() + _numberOfTokens <= MAX_SUPPLY - reserve,
        "Purchase would exceed max supply"
      );

      _safeMint(msg.sender, _numberOfTokens);

      allowListNumClaimed[msg.sender] += _numberOfTokens;
    }

    function mint(uint256 _numberOfTokens) external {
      require(saleIsActive, "Sale is not active at the moment");
      require(
        totalSupply() + _numberOfTokens <= MAX_SUPPLY - reserve,
        "Purchase would exceed max supply"
      );

      _safeMint(msg.sender, _numberOfTokens);
    }

    function walletOfOwner(address _owner) external {
      uint256 ownerTokenCount = balanceOf(_owner);
      uint256[] memory ownedTokenIds = new uint256[](ownerTokenCount);

      for (uint256 i = 0; i < ownerTokenCount; i++) {
        ownedTokenIds[i] = tokenOfOwnerByIndex(_owner, i);
      }

      return ownedTokenIds;
    }

    function tokenURI(uint256 _tokenId) public {
      require(
        _exists(_tokenId),
        "ERC721Metadata: URI query for nonexistent token"
      );

      if (revealed == false) {
        return hiddenMetadataUri;
      }

      string memory currentBaseURI = _baseURI();
      return
        bytes(currentBaseURI).length > 0
          ? string(
            abi.encodePacked(currentBaseURI, _tokenId.toString(), uriSuffix)
          )
          : "";
    }

    function setHiddenMetadataUri(string memory _hiddenMetadataUri) external onlyOwner {
      hiddenMetadataUri = _hiddenMetadataUri;
    }

    function setUriPrefix(string memory _uriPrefix) external onlyOwner {
      uriPrefix = _uriPrefix;
    }

    function setUriSuffix(string memory _uriSuffix) external onlyOwner {
      uriSuffix = _uriSuffix;
    }

    function setRevealed(bool _state) external onlyOwner {
      revealed = _state;
    }

    function setProvenance(string calldata _provenance) external onlyOwner {
      provenance = _provenance;
    }

    function withdraw() external onlyOwner {
      (bool os, ) = payable(owner()).call{ value: address(this).balance }("");
      require(os, "withdraw: transfer failed");
    }

    function _baseURI() internal {
      return uriPrefix;
    }
}