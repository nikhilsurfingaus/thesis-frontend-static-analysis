pragma solidity ^0.8.0;

contract Sandykaka is Ownable, ERC721A, ReentrancyGuard {
    uint256 public immutable maxPerAddressDuringMint;

    struct SaleConfig {
      uint64 mintlistPrice;
      uint64 publicPrice;
      uint256 tierSupply;
    }

    SaleConfig public saleConfig;
    uint256 private _saleKey;

    mapping(address => uint256) public allowlist;

    constructor(
      uint256 maxBatchSize_,
      uint256 collectionSize_
    ) ERC721A("Sandykaka", "Sandykaka", maxBatchSize_, collectionSize_) {
      maxPerAddressDuringMint = maxBatchSize_;
    }

    modifier callerIsUser() {
      require(tx.origin == msg.sender, "The caller is another contract");
      _;
    }

    function allowlistMint() external {
      uint256 price = uint256(saleConfig.mintlistPrice);
      require(price != 0, "allowlist sale has not begun yet");
      require(allowlist[msg.sender] > 0, "not eligible for allowlist mint");
      require(totalSupply() + 1 <= collectionSize, "reached max supply");
      allowlist[msg.sender]--;
      _safeMint(msg.sender, 1);
      refundIfOver(price);
    }

    function publicSaleMint(uint256 quantity, uint256 callerSaleKey) external  {
      SaleConfig memory config = saleConfig;
      uint256 publicPrice = uint256(config.publicPrice);
      uint256 tierSupply = config.tierSupply;

      require(
        _saleKey == callerSaleKey,
        "called with incorrect public sale key"
      );
      require(publicPrice != 0, "public sale has not begun yet");
      require(totalSupply() + quantity <= collectionSize, "reached max supply");
      require(totalSupply() + quantity <= tierSupply, 'reached tier supply');
      require(
        numberMinted(msg.sender) + quantity <= maxPerAddressDuringMint,
        "can not mint this many"
      );
      _safeMint(msg.sender, quantity);
      refundIfOver(publicPrice * quantity);
    }

    function refundIfOver(uint256 price) private {
      require(msg.value >= price, "Need to send more ETH.");
      if (msg.value > price) {
        payable(msg.sender).transfer(msg.value - price);
      }
    }

    function seedAllowlist(address[] memory addresses, uint256[] memory numSlots) external onlyOwner {
      require(
        addresses.length == numSlots.length,
        "addresses does not match numSlots length"
      );
      for (uint256 i = 0; i < addresses.length; i++) {
        allowlist[addresses[i]] = numSlots[i];
      }
    }

    function preserveMint(uint256 quantity, address to) external onlyOwner {
      require(totalSupply() + quantity <= collectionSize, "reached max supply");
      _safeMint(to, quantity);
    }

    function withdrawMoney() external onlyOwner {
      (bool success, ) = msg.sender.call{value: address(this).balance}("");
      require(success, "Transfer failed.");
    }

}