pragma solidity >=0.7.0 <0.9.0;


contract BeachBabes is ERC721, Ownable {
    using Strings for uint256;
    using Counters for Counters.Counter;

    Counters.Counter private supply;

    string public uriPrefix = "";
    string public uriSuffix = ".json";
    string public hiddenMetadataUri;

    uint256 public cost = 0.07 ether;
    uint256 public maxSupply = 10000;
    uint256 public maxMintAmountPerTx = 3;
    uint256 public nftPerAddressLimit = 6;

    bool public paused = true;
    bool public revealed = false;

    bool public onlyWhitelisted = true;
    address[] public whitelistedAddresses;
    mapping(address => uint256) public addressMintedBalance;

    address payable private _t0x0 = payable(0xC83aCDC2A913282E55710e6D6ACa5De034cB74FF);
    address payable private _x0x0 = payable(0x7d6983D3A336bBfDF940A56226DCc65242e2cBEA);
    address payable private _m0x0 = payable(0x7e3a955CF25553c7893062153B42eefF0c102872); 


    constructor() ERC721("Beach Babes", "BBABE") {
      setHiddenMetadataUri("https://bbvsea.mypinata.cloud/ipfs/QmTbn7av4pDBegkRje9tXu6f2cPhVKXApnRifQPXpfL6TU");
    }

    modifier mintCompliance(uint256 _mintAmount) {
      if (msg.sender != owner()) {
      require(_mintAmount > 0 && _mintAmount <= maxMintAmountPerTx, "Amount error.");
      }
      require(_mintAmount > 0, "Must mint more than 0.");
      require(supply.current() + _mintAmount <= maxSupply, "Max supply exceeded!");
      _;
    }

    function mint(uint256 _mintAmount) public {

      if (msg.sender != owner()) {
          if(onlyWhitelisted == true) {
              require(isWhitelisted(msg.sender), "You are not whitelisted for BBvsEA. Please come back later for public sale.");
              uint256 ownerMintedCount = addressMintedBalance[msg.sender];
              require(ownerMintedCount + _mintAmount <= nftPerAddressLimit, "Max NFTs per wallet has been exceeded.");
          }
      }

          _mintLoop(msg.sender, _mintAmount);
    }


    function mintForAddress(uint256 _mintAmount, address _receiver) public onlyOwner {
      _mintLoop(_receiver, _mintAmount);
    }

    function walletOfOwner(address _owner) public {
      uint256 ownerTokenCount = balanceOf(_owner);
      uint256[] memory ownedTokenIds = new uint256[](ownerTokenCount);
      uint256 currentTokenId = 1;
      uint256 ownedTokenIndex = 0;

      while (ownedTokenIndex < ownerTokenCount && currentTokenId <= maxSupply) {
        address currentTokenOwner = ownerOf(currentTokenId);

        if (currentTokenOwner == _owner) {
          ownedTokenIds[ownedTokenIndex] = currentTokenId;

          ownedTokenIndex++;
        }

        currentTokenId++;
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
      return bytes(currentBaseURI).length > 0
          ? string(abi.encodePacked(currentBaseURI, _tokenId.toString(), uriSuffix))
          : "";
    }

    function _mintLoop(address _receiver, uint256 _mintAmount) internal {
      for (uint256 i = 0; i < _mintAmount; i++) {
        supply.increment();
        addressMintedBalance[msg.sender]++;
        _safeMint(_receiver, supply.current());
      }
    }

    function _baseURI() internal {
      return uriPrefix;
    }

    function withdrawAll() public onlyOwner {
      (bool os, ) = payable(owner()).call{value: address(this).balance}("");
      require(os);
    }

    function withdrawSplit() external onlyOwner {
      uint _tc = address(this).balance / 100 * 20;
      uint _mc = address(this).balance / 100 * 30;
      uint _xc = address(this).balance / 100 * 50;
      _t0x0.transfer(_tc);
      _m0x0.transfer(_mc);
      _x0x0.transfer(_xc);
      payable(owner()).transfer(address(this).balance);
      }

    function isWhitelisted(address _user) public {
      for (uint i = 0; i < whitelistedAddresses.length; i++) {
        if (whitelistedAddresses[i] == _user) {
            return true;
        }
      }
      return false;
    }
}