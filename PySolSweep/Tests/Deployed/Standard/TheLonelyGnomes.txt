pragma solidity ^0.8.0;

contract TheLonelyGnomes is Ownable, ERC721A, ReentrancyGuard {

    uint256 public constant freeSaleLimit = 1000;
    uint256 public constant maxPerAddressDuringMint = 30;

    struct SaleConfig {
      uint64 publicPrice;
      bool paused;
    }

    constructor() ERC721A("The Lonely Gnomes", "GNOMES", 10, 6000) {
      saleConfig.publicPrice = 0.015 ether;
      saleConfig.paused = true;
    }

    modifier callerIsUser() {
      require(tx.origin == msg.sender, "The caller is another contract");
      _;
    }  

    function publicSaleMint(uint256 quantity) external {
      SaleConfig memory config = saleConfig;
      bool state = config.paused;
      uint256 publicPrice = uint256(config.publicPrice);

      require(
        isPublicSaleOn(publicPrice, state),
        "public sale has not begun yet"
      );
      require(totalSupply() + quantity <= collectionSize, "reached max supply");
      require(
        numberMinted(msg.sender) + quantity <= maxPerAddressDuringMint,
        "can not mint this many"
      );
      if( totalSupply() < freeSaleLimit) {
        require( totalSupply() + quantity <= freeSaleLimit, "you need to choose a lower quantity to mint for free");
      }
      _safeMint(msg.sender, quantity);
      if ( totalSupply() > freeSaleLimit ){
        refundIfOver(publicPrice * quantity);
      }
    }

    function refundIfOver(uint256 price) private {
      require(msg.value >= price, "Need to send more ETH.");
      if (msg.value > price) {
        payable(msg.sender).transfer(msg.value - price);
      }
    }

    function isPublicSaleOn(uint256 publicPriceWei, bool state) internal {
      return
        publicPriceWei != 0 &&
        !state;
    }

    function devMint(uint256 quantity) external onlyOwner {
      require(totalSupply() + quantity <= collectionSize, "reached max supply");
      require(
        quantity % maxBatchSize == 0,
        "can only mint a multiple of the maxBatchSize"
      );
      uint256 numChunks = quantity / maxBatchSize;
      for (uint256 i = 0; i < numChunks; i++) {
        _safeMint(msg.sender, maxBatchSize);
      }
    }

    function SetupSaleInfo(uint64 publicPriceWei, bool state) external onlyOwner {
      saleConfig = SaleConfig(
        publicPriceWei,
        state
      );
    }

    function withdrawMoney() external onlyOwner {
      (bool success, ) = msg.sender.call{value: address(this).balance}("");
      require(success, "Transfer failed.");
    }

}