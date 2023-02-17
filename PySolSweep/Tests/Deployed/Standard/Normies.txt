pragma solidity ^0.8.0;

contract Normies is IERC721, Ownable, Functional {

    using Address for address;
    
    string private _name;

    string private _symbol;
    
    string private _baseURI;

    mapping(uint256 => address) private _owners;

    mapping(address => uint256) private _balances;

    mapping(uint256 => address) private _tokenApprovals;

    mapping(address => mapping(address => bool)) private _operatorApprovals;
    
    bool public mintActive;
    bool public whitelistActive;
    bool private _hideTokens;  
    uint256 public price;
    uint256 public totalTokens;
    uint256 public numberMinted;
    uint256 public maxPerTxn;
    uint256 public whiteListMax;
    uint256 public WLprice;
    
    mapping(address => uint256) private _whitelist;

    constructor() {
        _name = "Paranormies";
        _symbol = "NORMIE";
        _baseURI = "https://paranormies.io/metadata/";
        _hideTokens = true;
        

        totalTokens = 9700;
        price = 69 * (10 ** 15); // Replace leading value with price in finney  0.069E
        WLprice = 69 * (10 ** 15);
        maxPerTxn = 20;
        whiteListMax = 4;
    }

    function supportsInterface(bytes4 interfaceId) public {
        return  interfaceId == type(IERC721).interfaceId ||
                interfaceId == type(IERC721Metadata).interfaceId ||
                interfaceId == type(IERC165).interfaceId ||
                interfaceId == Normies.onERC721Received.selector;
    }
    
    function withdraw() external onlyOwner {
        uint256 Funds = address(this).balance;
        bool success;

        uint256 sendAmount = (Funds * 85) / 100;
        (success, ) = Founder.call{value: sendAmount}("");
        require(success, "Transaction Unsuccessful");
        
        sendAmount = (Funds * 5) / 100;
        (success, ) = Developer.call{value: sendAmount}("");
        require(success, "Transaction Unsuccessful"); 
        
        sendAmount = (Funds * 5) / 100;
        (success, ) = Consulting.call{value: sendAmount}("");
        require(success, "Transaction Unsuccessful");
        
        sendAmount = (Funds * 5) / 100;
        (success, ) = Community.call{value: sendAmount}("");
        require(success, "Transaction Unsuccessful");
        
    }
    
    function ownerMint(address _to, uint256 qty) external onlyOwner {
        require((numberMinted + qty) > numberMinted, "Math overflow error");
        require((numberMinted + qty) <= totalTokens, "Cannot fill order");
        
        uint256 mintSeedValue = numberMinted; 
        
        for(uint256 i = 0; i < qty; i++) {
            _safeMint(_to, mintSeedValue + i);
            numberMinted ++;  //reservedTokens can be reset, numberMinted can not
        }
    }

    function singleAirdrop(address _to) external onlyOwner {
        require(numberMinted <= totalTokens, "Cannot Fill Order");

        uint256 mintSeedValue = numberMinted; 

        numberMinted ++; 
        _safeMint(_to, mintSeedValue);
    }
    
    function airDrop(address[] memory _to) external onlyOwner {
        uint256 qty = _to.length;
        require((numberMinted + qty) > numberMinted, "Math overflow error");
        require((numberMinted + qty) <= totalTokens, "Cannot fill order");
        
        uint256 mintSeedValue = numberMinted;
        
        for(uint256 i = 0; i < qty; i++) {
            _safeMint(_to[i], mintSeedValue + i);
            numberMinted ++;  //reservedTokens can be reset, numberMinted can not
        }
    }
    
    function mintWL(uint256 qty) external {
        require(whitelistActive, "WL not open");
        require(msg.value == qty * WLprice, "WL: Wrong Eth Amount");
        require((qty + numberMinted) <= totalTokens, "WL: Not enough avaialability");
        require(_whitelist[_msgSender()] >= qty, "WL: unauth amount");

        _whitelist[_msgSender()] -= qty;
        
        uint256 mintSeedValue = numberMinted; 

        for(uint256 i = 0; i < qty; i++) {
            _safeMint(_msgSender(), mintSeedValue + i);
            numberMinted ++;
        }

    }

    function mint(uint256 qty) external {
        require(mintActive, "mint not open");
        require(msg.value >= qty * price, "Mint: Insufficient Funds");
        require(qty <= maxPerTxn, "Mint: Above Trxn Threshold!");
        require((qty + numberMinted) <= totalTokens, "Mint: Not enough avaialability");
        
        uint256 mintSeedValue = numberMinted; 

        for(uint256 i = 0; i < qty; i++) {
            _safeMint(_msgSender(), mintSeedValue + i);
            numberMinted ++;
        }
    }
    
    function burn(uint256 tokenID) external {
        require(_msgSender() == ownerOf(tokenID));
        _burn(tokenID);
    }
    
    function whiteList(address account) external onlyOwner {
        _whitelist[account] = whiteListMax;
    }
    
    function whiteListMany(address[] memory accounts) external onlyOwner {
        for (uint256 i; i < accounts.length; i++) {
            _whitelist[accounts[i]] = whiteListMax;
        }
    }

    function _transfer(address from, address to, uint256 tokenId) internal {
        require(ownerOf(tokenId) == from, "ERC721: txfr token not owned");
        require(to != address(0), "ERC721: txfr to 0x0 address");
        _beforeTokenTransfer(from, to, tokenId);

        _approve(address(0), tokenId);

        _balances[from] -= 1;
        _balances[to] += 1;
        _owners[tokenId] = to;

        emit Transfer(from, to, tokenId);
    }

    function _approve(address to, uint256 tokenId) internal {
        _tokenApprovals[tokenId] = to;
        emit Approval(ownerOf(tokenId), to, tokenId);
    }
    
    receive() external payable {}
    
    fallback() external payable {}
}