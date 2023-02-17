contract GolemZ is ERC721, Ownable, PaymentSplitter {
    using SafeMath for uint256;

    uint256 public maxAmntTokens;
    uint256 public maxTknPerTxs;
    uint256 public price;
    uint256 public maxNFTsPresale;
    uint256 public maxMintsPreSale;
    string newURI;
    bool public saleIsActive;
    bool public URIlocked;
    bool public ownershipLocked;
    bool public preSaleIsActive;
    mapping(address => bool) public reserveListPreSale;
    mapping(address => uint) public reserveListPreSaleCounter;

    constructor(address[] memory _payees, uint256[] memory _shares) ERC721("GolemZ Genesis", "GLZG") PaymentSplitter(_payees, _shares) payable {
        maxAmntTokens = 888;
        maxTknPerTxs = 3;
        price = 100000000000000000 wei;
        saleIsActive = false;
        URIlocked = false;
        ownershipLocked = false;
        maxNFTsPresale = 1;
        preSaleIsActive = false;
        maxMintsPreSale = 1;
    }

    function addPreSaleAddresses(address[] calldata _users) public onlyOwner {
        for(uint i = 0; i < _users.length; i++) {
            reserveListPreSale[_users[i]] = true;
        }    
    }

    function flipPreSaleState () public onlyOwner {
        preSaleIsActive = !preSaleIsActive;
    }

    function totalSupply() public {
        return maxAmntTokens;
    } 
    
    function flipSaleState() public onlyOwner{
        saleIsActive = !saleIsActive;
    }
    
    function reserveNFT(uint256 reservedTokens) public onlyOwner{
        require ((reservedTokens.add(checkMintedTokens()) <= maxAmntTokens), "You are minting more NFTs than there are available, mint less tokens!");
        require (reservedTokens <= 20, "Sorry, the max amount of reserved tokens per transaction is set to 20");
        
        for (uint i=0; i<reservedTokens; i++){
            safeMint(msg.sender);
        }
    }
    
    function changeURI(string calldata _newURI) public onlyOwner{
        require (URIlocked == false, "URI locked, you can't change it anymore");
        newURI = _newURI;
    }

    function lockURI() public onlyOwner {
        require(URIlocked == false, "URI already locked");
        URIlocked = true;
    }
    
    function _baseURI() internal {
        return newURI;
    }
    
    function safeMint(address to) internal {
        _safeMint(to, _tokenIdCounter.current());
        _tokenIdCounter.increment();
    }
    
    function checkMintedTokens() public {
        return(_tokenIdCounter._value);
    }

    function mintNFT(uint256 amountTokens) public {

        if (preSaleIsActive) {
            require (reserveListPreSale[msg.sender], "You are not part of the pre sale.");
            require (amountTokens + reserveListPreSaleCounter[msg.sender] == maxMintsPreSale, "You are allowed to mint a max of 1 NFTs in the presale phase.");             
        }
        require(saleIsActive, "Sale is not active at this moment");
        require ((amountTokens.add(checkMintedTokens()) <= maxAmntTokens), "You are minting more NFTs than there are available, mint less tokens!");
        require (amountTokens <= maxTknPerTxs, "Sorry, the max amount of tokens per transaction is set to 3");
        require (msg.value == (price.mul(amountTokens)), "Amount of Ether incorrect, try again.");
        
        for (uint i=0; i<amountTokens; i++){
            safeMint(msg.sender);
        }

        if (preSaleIsActive) {
            reserveListPreSaleCounter[msg.sender] += amountTokens;
        }
        
    }
}