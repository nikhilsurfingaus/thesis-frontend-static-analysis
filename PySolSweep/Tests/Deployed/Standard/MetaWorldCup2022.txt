pragma solidity >=0.7.0 <0.9.0;

contract MetaWorldCup2022 is Ownable {
    using Strings for uint256;

    string baseURI;
    string public baseExtension = ".json";
    uint256 public cost = 0.09 ether;
    uint256 public maxSupply = 4480;
    uint256 public maxMintAmount = 20;
    bool public paused = true;  
    bool public revealed = false; 
    string public notRevealedUri;

    constructor(string memory _name, string memory _symbol, string memory _initBaseURI, string memory _initNotRevealedUri) {
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

    function reveal() public onlyOwner {
        revealed = true;
    }

    function setCost(uint256 _newCost) public onlyOwner {
      cost = _newCost;
    }

    function setmaxMintAmount(uint256 _newmaxMintAmount) public onlyOwner {
      maxMintAmount = _newmaxMintAmount;
    }

    function setNotRevealedURI(string memory _notRevealedURI) public onlyOwner {
      notRevealedUri = _notRevealedURI;
    }

    function setBaseURI(string memory _newBaseURI) public onlyOwner {
      baseURI = _newBaseURI;
    }

    function setBaseExtension(string memory _newBaseExtension) public onlyOwner {
      baseExtension = _newBaseExtension;
    }

    function pause(bool _state) public onlyOwner {
      paused = _state;
    }

    function withdraw() public onlyOwner {
      (bool os, ) = payable(owner()).call{value: address(this).balance}("");
      require(os);
    }
}