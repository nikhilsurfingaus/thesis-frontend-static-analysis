pragma solidity >=0.7.0 <0.9.0;

contract BitDoods is ERC721Enumerable, Ownable {
  using Strings for uint256;

  string public baseURI;
  string public baseExtension = ".json";
  uint256 public cost = 0.0088 ether;
  uint256 public maxSupply = 5888;
  uint256 public maxMintAmount = 20;
  uint256 public freeMaxMintAmount = 10;
  uint256 public nftPerAddressLimit = 5;
  bool public paused = false;
  address[] public whitelistedAddresses;
  mapping(address => uint256) public addressMintedBalance;

  constructor(
    string memory _name,
    string memory _symbol,
    string memory _initBaseURI
    
  ) ERC721(_name, _symbol) {
    setBaseURI(_initBaseURI);
    
  }
    
  function mint(uint256 _mintAmount) public {
    require(!paused, "the contract is paused");
    uint256 supply = totalSupply();
    require(_mintAmount > 0, "need to mint at least 1 NFT");
    require(supply + _mintAmount <= maxSupply, "max NFT limit exceeded");
    
    
    if (msg.sender != owner()) {
            uint256 ownerMintedCount = addressMintedBalance[msg.sender];
        if (supply <= 500) {
            require(ownerMintedCount + _mintAmount <= freeMaxMintAmount, "max mint amount per session exceeded");
            require(msg.value >= 0);

        }else if(isWhitelisted(msg.sender)) {
            
            
            if (ownerMintedCount + _mintAmount <= nftPerAddressLimit) {
               require(msg.value >= 0);
            } else {
               require(_mintAmount <= maxMintAmount, "max mint amount per session exceeded");
               require(msg.value >= cost * _mintAmount, "insufficient funds");
            }

        } else {
            require(_mintAmount <= maxMintAmount, "max mint amount per session exceeded");
            require(msg.value >= cost * _mintAmount, "insufficient funds");
           
        }
                
    }    

    for (uint256 i = 1; i <= _mintAmount; i++) {
      addressMintedBalance[msg.sender]++;
      _safeMint(msg.sender, supply + i);
    }
  }

  function isWhitelisted(address _user) public {
      for (uint i = 0; i < whitelistedAddresses.length; i++) {
          if (whitelistedAddresses[i] == _user) {
              return true;
          }
      }
      return false;
  } 

  function walletOfOwner(address _owner) public {
    uint256 ownerTokenCount = balanceOf(_owner);
    uint256[] memory tokenIds = new uint256[](ownerTokenCount);
    for (uint256 i; i < ownerTokenCount; i++) {
      tokenIds[i] = tokenOfOwnerByIndex(_owner, i);
    }
    return tokenIds;
  }
  
  function tokenURI(uint256 tokenId) public{
    require(
      _exists(tokenId),
      "ERC721Metadata: URI query for nonexistent token"
    );
    
    string memory currentBaseURI = _baseURI();
    return bytes(currentBaseURI).length > 0
        ? string(abi.encodePacked(currentBaseURI, tokenId.toString(), baseExtension))
        : "";
  }
   
  function withdraw() public onlyOwner {
    (bool os, ) = payable(owner()).call{value: address(this).balance}("");
    require(os);
  }
}