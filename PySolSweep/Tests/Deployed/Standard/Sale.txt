pragma solidity ^0.8.9;


contract Sale {
    using SafeMath for uint256;

    address payable public owner;
    bool public isClaimable;
    bool public closed;
    IERC20 public token;
    AggregatorV3Interface internal priceFeed;
    mapping(address => uint256) public claimable;
    uint256 public minBuy;
    uint256 public maxBuy;

    constructor(address spumeAddress, uint256 min, uint256 max) {
        owner = payable(msg.sender);
        isClaimable = false;
        closed = false;
        token = IERC20(spumeAddress);
        priceFeed = AggregatorV3Interface(0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419);
        minBuy = min;
        maxBuy = max;
    }

    function updateMinMax(uint256 min, uint256 max) public {
        require(msg.sender == owner, "Caller must be owner");
        minBuy = min;
        maxBuy = max;
    }

    function closeSale() public {
        require(msg.sender == owner, "Caller must be owner");
        closed = true;
    }

    function openSale() public {
        require(msg.sender == owner, "Caller must be owner");
        closed = false;
    }

    function closeClaim() public {
        require(msg.sender == owner, "Caller must be owner");
        isClaimable = false;
    }

    function openClaim() public {
        require(msg.sender == owner, "Caller must be owner");
        isClaimable = true;
    }

    function buy() public {
        require(closed == false, "Sale is closed");
        int price = getETHUSDPrice();
        require(price > 0, "Error with Chainlink");
        uint256 spumeAmount = uint256(price) * msg.value;
        spumeAmount = (((spumeAmount / (10 ** 8)) * 3333) / 1000);
        require(spumeAmount >= minBuy, "Cannot buy that few tokens");
        require(spumeAmount <= maxBuy, "Cannot buy that many tokens");
        spumeAmount = spumeAmount / 2;
        require(spumeAmount <= token.allowance(owner, address(this)), "Sale is sold out");
        owner.transfer(msg.value);
        token.transferFrom(owner, msg.sender, spumeAmount);
        claimable[msg.sender] += spumeAmount;
    }

    function claim() public {
        require(isClaimable, "Cannot claim tokens yet");
        uint256 spumeAmount = claimable[msg.sender];
        require(spumeAmount > 0, "No tokens to claim or tokens already claimed");
        require(spumeAmount <= token.allowance(owner, address(this)), "Error with token allocation");
        claimable[msg.sender] = 0;
        token.transferFrom(owner, msg.sender, spumeAmount);
    }

    function getETHUSDPrice() public {
        (
            uint80 roundID, 
            int price,
            uint startedAt,
            uint timeStamp,
            uint80 answeredInRound
        ) = priceFeed.latestRoundData();
        return price;
    }
}