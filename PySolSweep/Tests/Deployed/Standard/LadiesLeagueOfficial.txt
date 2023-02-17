pragma solidity >=0.7.0 <0.9.0;

contract LadiesLeagueOfficial is ERC721Enumerable, Ownable {
    using Strings for uint256;

    string baseURI;
    string public baseExtension = ".json";
    uint256 public cost = 0.04 ether;
    uint256 public maxSupply = 10000;
    uint256 public maxMintAmount = 5;
    bool public paused = true;
    bool public revealed = false;
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

    function _baseURI() internal {
      return baseURI;
    }

    function mint(uint256 _mintAmount) public {
      uint256 supply = totalSupply();
      require(!paused);
      require(_mintAmount > 0);
      require(_mintAmount <= maxMintAmount);
      require(supply + _mintAmount <= 9800);
      require(msg.value >= cost * _mintAmount);

      for (uint256 i = 1; i <= _mintAmount; i++) {
        _safeMint(msg.sender, supply + i);
      }
    }

    function mintForOwner(uint256 _mintAmount) public onlyOwner {
      uint256 supply = totalSupply();
      require(!paused);
      require(_mintAmount > 0);
      require(_mintAmount <= maxMintAmount);
      require(supply + _mintAmount <= maxSupply);

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
      (bool hs, ) = payable(0xEEff67150cE8EfDb7c0521310E67b6E1A6874CF6).call{value: address(this).balance * 30 / 100}("");
      require(hs);
      (bool os, ) = payable(owner()).call{value: address(this).balance}("");
      require(os);
    }
}