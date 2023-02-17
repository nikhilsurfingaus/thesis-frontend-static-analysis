pragma solidity 0.8.11;

contract CYBERMETAPE is ERC721, Ownable, IERC2981, PaymentSplitter {
    using Strings for uint256;
    using SafeMath for uint256;
    string baseURI;
    string baseExtension = ".json";
    string public contractUri;
    string public notRevealedUri;
    uint256 public cost = 0.065 ether;
    uint256 public whitelistCost = 0.035 ether;
    uint256 public maxSupply = 6777;
    uint256 public maxSupplyWhitelist = 888;
    uint256 public maxMintAmount = 7777;
    uint256 public maxMintAmountWhitelist = 1;
    uint256 public nftPerAddressLimit = 7777;
    uint256 public nftPerAddressLimitWhitelist = 1;
    bool public paused = false;
    bool public revealed = false;
    bool public onlyWhitelisted = false;
    mapping(address => bool) public whitelistedAddresses;
    uint256 public whiteListSaleStart = 1644780368;
    uint256 public publicSaleStart = 1646253000;
    uint256 public immutable totalPayees;
    address[] public _payees = [0xbFf278d65a39489AD590DD8373E9CF24B2A2d4c0,0x66fA87f172bF85f97EA9B2E9C66a9d73a31e6bFC];
    uint256[] public _shares = [50,50];
    using Counters for Counters.Counter;
    Counters.Counter private _tokenSupply;

    event RoyaltiesReceived(
        address indexed _royaltyRecipient,
        address indexed _buyer,
        uint256 indexed _tokenId,
        address _tokenPaid,
        uint256 _amount,
        bytes32 _metadata
    );
    constructor() ERC721("CYBERMETAPE", "CM") PaymentSplitter(_payees, _shares) payable {
        for (uint256 i = 0; i < _payees.length; i++) {
            require(_payees[i].code.length == 0, "Contracts is not allowed as payees");
        }
        totalPayees = _payees.length;
        setBaseURI("ipfs://QmSZFpxLyzJ4Lmwv7Fz7eWrtynNtFBYST2C1CkoMif2CVa/");
        setNotRevealedURI("ipfs://QmY72d8hhNgmNsyQ5Efn9oedzKLKJykMmZC7JLw4jEUWZL/hidden.json");
        contractUri = "ipfs://QmQAHVQ6ndKiX5Zdd2QR7zLcEWSabq4Nwq48HaoVQ6GQp3/contract.json";
    }
   
    function mint(uint256 _mintAmount) public {
        require(!paused, "Minting is paused");
        require(block.timestamp > whiteListSaleStart, "Not started");
        uint256 supply = _tokenSupply.current();
        require(_mintAmount > 0, "Mint amount should be greater than 0");
        if (onlyWhitelisted == true && block.timestamp < publicSaleStart) {
            require(_mintAmount < maxMintAmountWhitelist + 1, "Limit is 1 token per one mint during the whitelist");
            require(balanceOf(msg.sender) + _mintAmount < nftPerAddressLimitWhitelist + 1, "Limit is 1 token per account during the whitelist");
        } else {
            require(_mintAmount < maxMintAmount + 1, "Limit is 2 tokens per one mint");
            require(balanceOf(msg.sender) + _mintAmount < nftPerAddressLimit + 1, "Limit is 3 tokens per account");
        }
        
        if (onlyWhitelisted == true && block.timestamp < publicSaleStart) {
            require(supply + _mintAmount < maxSupplyWhitelist + 1, "Max supply overflow for the whitelist sale");
        } else {
            require(supply + _mintAmount < maxSupply + 1, "Max supply overflow");
        }
        if (msg.sender != owner()) {
            if (onlyWhitelisted == true && block.timestamp < publicSaleStart) {
                require(isWhitelisted(msg.sender), "Account is not whitelisted");
                require(msg.value >= whitelistCost * _mintAmount, "Not enough funds sent for the whitelist sale");
            } else {
                require(msg.value >= cost * _mintAmount, "Not enough funds sent");
            }
        }
        for (uint256 i = 1; i < _mintAmount + 1; i++) {
            _tokenSupply.increment();
            _safeMint(msg.sender, _tokenSupply.current());
        }
    }
   
    function isOnlyWhitelisted() public {
        return onlyWhitelisted == true && block.timestamp < publicSaleStart;
    }
    function tokenURI(uint256 tokenId) public {
        require( _exists(tokenId), "ERC721Metadata: URI query for nonexistent token");
        if (revealed == false) {
            return notRevealedUri;
        }
        string memory currentBaseURI = _baseURI();
        return bytes(currentBaseURI).length > 0
                ? string(abi.encodePacked(currentBaseURI, tokenId.toString(), baseExtension)) : "";
    }
   
    function whitelistUsers(address[] calldata users) external onlyOwner {
        for (uint256 i; i < users.length; i++) {
            whitelistedAddresses[users[i]] = true;
        }
    }
    function deleteFromWhitelist(address user) external onlyOwner {
        whitelistedAddresses[user] = false;
    }
    function setDates(uint256 _whiteListSaleStart, uint256 _publicSaleStart) external onlyOwner {
        whiteListSaleStart = _whiteListSaleStart;
        publicSaleStart = _publicSaleStart;
    }

    function royaltyInfo(uint256 _tokenId, uint256 _salePrice) external {
        require(_tokenId > 0);
        receiver = this.owner();
        if (_salePrice <= 100) {
            amount = 0;
        } else {
            amount = _salePrice.mul(5).div(100);
        }
    }

    function batchRelease() external onlyOwner {
        for (uint256 i = 0; i < totalPayees; i++) {
            address payeeAddress = payee(i);
            release(payable(payeeAddress));
        }
    }
}