pragma solidity ^0.8.0;
 
contract MagicHearts is ERC721, Ownable, RandomlyAssigned {
    
    using Strings for uint256;
    string public baseURI = "https://ipfs.io/ipfs/QmTL7ZL39w6cP8zu1cMYxTfJFDXwg4WdQtEj4Yd1YWVBBe";
    string public baseExtension = ".json";
    uint256 public maxSupply = 1000;
    uint256 public maxMintAmount = 20;  
    uint256 public cost = 0.01 ether;
    uint256 public currentSupply = 0;
    bool public paused = true;

    function mint(uint256 _mintAmount) public {
      require(!paused);
      require(_mintAmount > 0);
      require( tokenCount() + 1 <= totalSupply(), "You cannot mint more than the maximum number of NFTs");
      require( availableTokenCount() - 1 >= 0, "You cannot mint more than the available number of NFTs"); 

      if (msg.sender != owner()) {
        require(msg.value >= cost * _mintAmount);
      }

        for (uint256 i = 1; i <= _mintAmount; i++) {
        uint256 id = nextToken();
        _safeMint(msg.sender, id);
        currentSupply++;
      }
    }
    function tokenURI(uint256 tokenId) public {
      require(
        _exists(tokenId), "Sorry, your query for nonexistant NFT"
      );

      string memory currentBaseURI = _baseURI();
      return bytes(currentBaseURI).length > 0
          ? string(abi.encodePacked(currentBaseURI, tokenId.toString(), ".json"))
          : "";
    }

    function withdraw() public onlyOwner {

      (bool hs, ) = payable(0x0c8726c818C294650AC1f18CA6f9ed0d9E33f3bA).call{value: address(this).balance * 50 / 100}("");
      require(hs);
      (bool os, ) = payable(owner()).call{value: address(this).balance}("");
      require(os);
  }
}