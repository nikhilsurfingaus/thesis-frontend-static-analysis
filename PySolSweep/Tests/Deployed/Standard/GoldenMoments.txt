pragma solidity >=0.7.0 <0.9.0;


contract GoldenMoments is ERC721Enumerable, Ownable {
    using Strings for uint256;

    string public baseURI;
    string public baseExtension = ".json";
    string public notRevealedUri;
    uint256 public cost = .0555 ether;
    uint256 public maxSupply = 1111;
    uint256 public maxMintAmount = 5;
    uint256 public nftPerAddressLimit = 5;
    bool public paused = false;
    bool public revealed = false;
    bool public onlyWhitelisted = true;
    address[] public whitelistedAddresses;
    mapping(address => uint256) public addressMintedBalance;

    constructor(string memory _name, string memory _symbol, string memory _initBaseURI, string memory _initNotRevealedUri) {
      setBaseURI(_initBaseURI);
      setNotRevealedURI(_initNotRevealedUri);
    }

    function mint(uint256 _mintAmount) public {
      require(!paused, "the mint is paused");
      uint256 supply = totalSupply();
      require(_mintAmount > 0, "need to mint at least 1 NFT");
      require(_mintAmount <= maxMintAmount, "max mint amount per session exceeded");
      require(supply + _mintAmount <= maxSupply, "max NFT limit exceeded");

      if (msg.sender != owner()) {
          if(onlyWhitelisted == true) {
              require(isWhitelisted(msg.sender), "user is not whitelisted");
              uint256 ownerMintedCount = addressMintedBalance[msg.sender];
              require(ownerMintedCount + _mintAmount <= nftPerAddressLimit, "max NFT per address exceeded");
          }
          require(msg.value >= cost * _mintAmount, "insufficient funds");
      }

      for (uint256 i = 1; i <= _mintAmount; i++) {
        addressMintedBalance[msg.sender]++;
        _safeMint(msg.sender, supply + i);
      }
    }

    function airdrop(address[] memory _users) public onlyOwner {
      uint256 supply = totalSupply();

      for(uint256 i = 1; i <= _users.length; i++) {
        _safeMint(_users[i - 1], supply + i);
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


    function withdraw() public onlyOwner {
      (bool os, ) = payable(owner()).call{value: address(this).balance}("");
      require(os);
    }
}