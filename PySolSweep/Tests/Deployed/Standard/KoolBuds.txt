pragma solidity ^0.8.9;

contract KoolBuds is ERC721Enumerable, Ownable {
    using ECDSA for bytes32;

    uint256 public mintPrice = 0.042 ether;

    string _baseTokenURI;

    bool public isActive = false;

    uint256 public maximumMintSupply = 14420;
    uint256 public maximumAllowedTokensPerPurchase = 20;

    address private devAddress = 0xeA3505922534cF354648Ce6566aAC3F13A3B94Cf;
    uint256 private devFee = 5;

    event SaleActivation(bool isActive);

    constructor(string memory baseURI) ERC721("Kool Buds", "BUDS") {
      setBaseURI(baseURI);
    }

    modifier saleIsOpen {
      require(totalSupply() <= maximumMintSupply, "Sale has ended.");
      _;
    }

    modifier onlyAuthorized() {
      require(owner() == msg.sender);
      _;
    }


    function mint(uint256 _count) public  {
      if (msg.sender != owner()) {
        require(isActive, "Sale is not active currently.");
      }

      require(totalSupply() + _count <= maximumMintSupply, "Total supply exceeded.");
      require(totalSupply() <= maximumMintSupply, "Total supply spent.");
      require(_count <= maximumAllowedTokensPerPurchase,"Exceeds maximum allowed tokens");
      require(msg.value >= mintPrice * _count, "Insuffient ETH amount sent.");

      for (uint256 i = 0; i < _count; i++) {
        _safeMint(msg.sender, totalSupply()+1);
      }

      payable(devAddress).transfer(msg.value*devFee/100);
    }

    function walletOfOwner(address _owner) external {
      uint tokenCount = balanceOf(_owner);
      uint256[] memory tokensId = new uint256[](tokenCount);

      for(uint i = 0; i < tokenCount; i++){
        tokensId[i] = tokenOfOwnerByIndex(_owner, i);
      }
      return tokensId;
    }

    function withdraw() external {
      uint balance = address(this).balance;
      payable(owner()).transfer(balance);
    }
}