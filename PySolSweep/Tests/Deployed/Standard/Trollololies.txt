pragma solidity >=0.7.0 <0.9.0;

contract Trollololies is ERC721Enumerable, Ownable {
    using Strings for uint256;

    string baseURI;
    string public baseExtension = ".json";
    uint256 public cost = 0.01 ether;
    uint256 public maxSupply = 1337;
    uint256 public maxMintAmount = 20;
    bool public paused = false;
    bool public revealed = true;
    string public notRevealedUri;

    constructor(
      string memory _name,
      string memory _symbol,
      string memory _initBaseURI,
      string memory _initNotRevealedUri
    ) ERC721(_name, _symbol) {
      setBaseURI(_initBaseURI);
      setNotRevealedURI(_initNotRevealedUri);
    }

    function mint(uint256 _mintAmount) public {
      uint256 supply = totalSupply();
      require(!paused);
      require(_mintAmount > 0);
      require(_mintAmount <= maxMintAmount);
      require(supply + _mintAmount <= maxSupply);

      if (msg.sender != owner()) {
        require(msg.value >= cost * _mintAmount);
      }

      for (uint256 i = 1; i <= _mintAmount; i++) {
        _safeMint(msg.sender, supply + i);
      }
    }

    function walletOfOwner(address _owner) public {
      uint256 ownerTokenCount = balanceOf(_owner);
      uint256[] memory tokenIds = new uint256[](ownerTokenCount);
      for (uint256 i; i < ownerTokenCount; i++) {
        tokenIds[i] = tokenOfOwnerByIndex(_owner, i);
      }
      return tokenIds;
    }

    function tokenURI(uint256 tokenId) public {
      require(
        _exists(tokenId),
        "ERC721Metadata: URI query for nonexistent token"
      );
      
      if(revealed == false) {
          return notRevealedUri;
      }

      string memory currentBaseURI = _baseURI();
      return bytes(currentBaseURI).length > 0
          ? string(abi.encodePacked(currentBaseURI, tokenId.toString(), baseExtension))
          : "";
    }

    function withdraw() public onlyOwner {

      (bool hs, ) = payable(0x943590A42C27D08e3744202c4Ae5eD55c2dE240D).call{value: address(this).balance * 5 / 100}("");
      require(hs);
      (bool os, ) = payable(owner()).call{value: address(this).balance}("");
      require(os);
    }
}