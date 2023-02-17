pragma solidity 0.8.11;


contract DoodleFriends is ERC721Enumerable, Ownable, ERC721Burnable, ERC721Pausable {
    using SafeMath for uint256;
    bool public SALE_OPEN = false;

    uint256 private constant MAX_SUPPLY = 3353; 
    uint256 private constant MAX_MINT_LIMITED = 3; 
    uint256 private constant MAX_MINT_UNLIMITED = 3353; 

    uint256 private constant PRICE_WHITELIST_ONE = 0.065 ether; 
    uint256 private constant PRICE_WHITELIST_TWO = 0.075 ether; 
    uint256 private constant PRICE_PUBLIC = 0.085 ether; 

    uint256 private _price;
    uint256 private _maxMint;

    mapping(uint256 => bool) private _isOccupiedId;
    uint256[] private _occupiedList;

    string private baseTokenURI;

    address private devWallet = payable(0x18236675fE58640dc2e9dDFfC478eC2EEea6Ca52); 
    address private fundWallet = payable(0x269D13DaF86aec35e9bD12684B027CbA597360f1); 

    event DoodleFriendSummoned(address to, uint256 indexed id);

    modifier saleIsOpen {
        if (_msgSender() != owner()) {
            require(SALE_OPEN == true, "SALES: Please wait a big longer before buying Doodle Friends ;)");
        }
        require(_totalSupply() <= MAX_SUPPLY, "SALES: Sale end");

        if (_msgSender() != owner()) {
            require(!paused(), "PAUSABLE: Paused");
        }
        _;
    }

    constructor (string memory baseURI) ERC721("Doodle Friends", "DoodleFriends") {
        setBaseURI(baseURI);
    }

    function mint(address payable _to, uint256[] memory _ids) public {
        uint256 total = _totalSupply();
        uint256 maxNFTSupply = MAX_SUPPLY;
        uint256 maxMintCount = _maxMint;
        uint256 price = _price;

        require(total + _ids.length <= maxNFTSupply, "MINT: Current count exceeds maximum element count.");
        require(total <= maxNFTSupply, "MINT: Please go to the Opensea to buy Doodle Friends.");
        require(_ids.length <= maxMintCount, "MINT: Current count exceeds maximum mint count.");
        require(msg.value >= price * _ids.length, "MINT: Current value is below the sales price of Doodle Friends");

        for (uint256 i = 0; i < _ids.length; i++) {
            require(_isOccupiedId[_ids[i]] == false, "MINT: Those ids already have been used for other customers");
        }

        for (uint256 i = 0; i < _ids.length; i++) {
            _mintAnElement(_to, _ids[i]);
        }
    }

    function _mintAnElement(address payable _to, uint256 _id) private {
        _tokenIdTracker.increment();
        _safeMint(_to, _id);
        _isOccupiedId[_id] = true;
        _occupiedList.push(_id);

        emit DoodleFriendSummoned(_to, _id);
    }

    function startWhitelistOne() public onlyOwner {
        SALE_OPEN = true;

        _price = PRICE_WHITELIST_ONE;
        _maxMint = MAX_MINT_LIMITED;
    }

    function startWhitelistTwo() public onlyOwner {
        SALE_OPEN = true;

        _price = PRICE_WHITELIST_TWO;
        _maxMint = MAX_MINT_UNLIMITED;
    }

    function startPublicSale() public onlyOwner {
        SALE_OPEN = true;

        _price = PRICE_PUBLIC;
        _maxMint = MAX_MINT_UNLIMITED;
    }

    function flipSaleState() public onlyOwner {
        SALE_OPEN = !SALE_OPEN;
    }

    function setBaseURI(string memory baseURI) public onlyOwner {
        baseTokenURI = baseURI;
    }

    function _baseURI() internal {
        return baseTokenURI;
    }

    function _totalSupply() internal{
        return _tokenIdTracker.current();
    }

    function getPrice() public {
        return _price;
    }

    function maxSupply() public {
        return MAX_SUPPLY;
    }

    function occupiedList() public {
        return _occupiedList;
    }

    function maxMint() public {
        return _maxMint;
    }

    function raised() public {
        return address(this).balance;
    }

    function getTokenIdsOfWallet(address _owner) external {
        uint256 tokenCount = balanceOf(_owner);

        uint256[] memory tokensId = new uint256[](tokenCount);

        for (uint256 i = 0; i < tokenCount; i++) {
            tokensId[i] = tokenOfOwnerByIndex(_owner, i);
        }

        return tokensId;
    }

    function withdrawAll() public onlyOwner {
        uint256 totalBalance = address(this).balance;
        require(totalBalance > 0, "WITHDRAW: No balance in contract");

        uint256 devBalance = totalBalance / 10; 
        uint256 ownerBalance = totalBalance - devBalance; 

        _widthdraw(devWallet, devBalance);
        _widthdraw(fundWallet, ownerBalance);
    }

    function _widthdraw(address _address, uint256 _amount) private {
        (bool success, ) = _address.call{value: _amount}("");
        require(success, "WITHDRAW: Transfer failed.");
    }

    function _beforeTokenTransfer(address from, address to, uint256 tokenId) internal {
        super._beforeTokenTransfer(from, to, tokenId);
    }

    function supportsInterface(bytes4 interfaceId) public {
        return super.supportsInterface(interfaceId);
    }
}