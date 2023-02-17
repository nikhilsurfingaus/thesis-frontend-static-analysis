pragma solidity ^0.8.0;

contract BattleCatsArena is ERC721A, Ownable {
    using Strings for uint256;

    string public baseURI;
    string public baseExtension = ".json";
    string public notRevealedUri;

    uint256 public cost = 0.065 ether;
    uint256 public maxSupply = 10000;
    uint256 public setMaxMintAmountPerTxn = 20; 
    uint256 public maxMintAmountPerWallet = 10000; 
    uint256 public totalPresaleTickets = 5000;
    uint256 public reserve = 200;
    uint256 public reserveMinted = 0;

    bool public paused = true;
    bool public revealed = false;
    bool public startMainSale = false;

    mapping(address => bool) private _presaleList;
    mapping(address => bool) private _giftFreeMint;
    mapping(address => uint256) public _totalMintedPresale;
    mapping(address => uint256) public _totalMintedMainsale;
  
    constructor() ERC721A("BattleCatsArena", "BCA", maxSupply, maxSupply) {
        setBaseURI("ipfs://Qmebgy2SzpgUa9EskNwoFYSBUMbP7Nzx6sCyvfZrW8Tdsj/");
        setNotRevealedURI("ipfs://QmSReC6aRvBKHvMBZosnnfxFwFE4hV8QWECxXYkq2Xet2x");
    }
  
    function preSaleMint(uint256 _mintAmount) public {
        if (msg.sender != owner()){
            require(!paused, "Public sale is not live, can't mint");
            require(_presaleList[msg.sender] == true,"You're not on the whitelist");
            require(_mintAmount <= maxMintAmountPerWallet, "Max Mint amount per session exceeded");
        }
        require(_mintAmount > 0, "Need to mint atleast 1 BattleCat");
        uint256 supply = totalSupply();
        require(supply + _mintAmount <= maxSupply - (reserve - reserveMinted), "Max NFT limit exceeded");
        require(supply + _mintAmount <= totalPresaleTickets, "Limit exceeded for presale");
        require(_totalMintedPresale[msg.sender] + _mintAmount <= maxMintAmountPerWallet,
            "exceeded presale total mints per wallet");
       
        if (msg.sender != owner()) {
            if (_giftFreeMint[msg.sender]==false){
                require(msg.value >= cost * _mintAmount, "insufficient funds");
            }
            else{
                require(_mintAmount == 1, "You can only 1 free mint");
                _giftFreeMint[msg.sender]=false;
            }
        }
        _totalMintedPresale[msg.sender] = _totalMintedPresale[msg.sender] + _mintAmount;
        _safeMint(msg.sender, _mintAmount);
        
    }
  
    function addToPresaleListing(address[] calldata _addresses) external onlyOwner {
        for (uint256 index = 0; index < _addresses.length; index++) {
            require(_addresses[index] != address(0),"Can't add a zero address");
            if (_presaleList[_addresses[index]] == false) {
                _presaleList[_addresses[index]] = true;
            }
        }
    }

    function removeFromPresaleListing(address[] calldata _addresses) external onlyOwner{
        for (uint256 ind = 0; ind < _addresses.length; ind++) {
            require(_addresses[ind] != address(0),"Can't remove a zero address");
            if (_presaleList[_addresses[ind]] == true) {
                _presaleList[_addresses[ind]] = false;
            }
        }
    }
    function checkIsOnPresaleList(address _address) external {
        return _presaleList[_address];
    }

    function checkIsOnFreesaleList(address _address) external  {
        return _giftFreeMint[_address];
    }

    function saleMint(uint256 _mintAmount) public {
        if (msg.sender != owner()){
            require(!paused, "Public sale is not live, can't mint");
            require(_mintAmount <= setMaxMintAmountPerTxn, "Max Mint amount exceeded");
            require(startMainSale == true, "Main sale is not started yet");
        }
        require(_mintAmount > 0, "Need to mint at least 1 BattleCat");
        
        uint256 supply = totalSupply();
        require(supply + _mintAmount <= maxSupply - (reserve - reserveMinted), "Max NFT limit exceeded");

        require(
            _totalMintedMainsale[msg.sender] + _mintAmount <= maxMintAmountPerWallet,
            "exceeded presale total mints per wallet"
            );
        if (msg.sender != owner()) {
            if (_giftFreeMint[msg.sender]==false){
                require(msg.value >= cost * _mintAmount, "insufficient funds");
            }
            else{
                require(_mintAmount == 1, "You can only 1 free mint");
                _giftFreeMint[msg.sender]=false;
            }
            
        }
        
        _safeMint(msg.sender, _mintAmount);
    }

    function reserveNFTs(uint256 amount) public onlyOwner{
        require(reserveMinted + amount <= reserve, "Max NFT limit reserveration exceeded");
        
        _safeMint(msg.sender, amount);
        reserveMinted = reserveMinted + amount;
    }

    function walletOfOwner(address _owner) public {
        uint256 ownerTokenCount = balanceOf(_owner);
        uint256[] memory tokenIds = new uint256[](ownerTokenCount);
        for (uint256 i; i < ownerTokenCount; i++) {
            tokenIds[i] = tokenOfOwnerByIndex(_owner, i);
        }
        return tokenIds;
    }

    function tokenURI(uint256 tokenId) public {
        require(
        _exists(tokenId),
        "ERC721Metadata: URI query for nonexistent token"
        );
        
        if(revealed == false) {
            return notRevealedUri;
        }

        string memory currentBaseURI = _baseURI();
        return bytes(currentBaseURI).length > 0
            ? string(abi.encodePacked(currentBaseURI, tokenId.toString(), baseExtension))
            : "";
    }
  
    function addToFreeMint(address[] calldata _addresses) external onlyOwner {
        for (uint256 index = 0; index < _addresses.length; index++) {
                require(_addresses[index] != address(0),"Can't add a zero address");
                if (_giftFreeMint[_addresses[index]] == false) {
                    _giftFreeMint[_addresses[index]] = true;
                }
            }
    }

    function removeFromFreeMint(address[] calldata _addresses) external onlyOwner {
        for (uint256 index = 0; index < _addresses.length; index++) {
            require(_addresses[index] != address(0),"Can't remove a zero address");
            if (_giftFreeMint[_addresses[index]] == true) {
                _giftFreeMint[_addresses[index]] = false;
            }
        }
    }
 
    function withdraw() external payable onlyOwner {
        (bool success, ) = payable(msg.sender).call{value: address(this).balance}("");
        require(success);
    }
}