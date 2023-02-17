pragma solidity ^0.8.10;

contract MembershipPass is ERC721Enumerable, Ownable {
    using SafeMath for uint256;
    uint256 public constant max_passes = 300;
    uint256 private _mintLimit = 15;
    uint256 private _price = 0; 
    uint256 private _publicSaleTime = 1642876500;
    string private _uriPrefix;
    string private _baseTokenURI;
    mapping(address => uint256) private _walletMinted;

    constructor(string memory baseURI)
        ERC721("Arq MBRSHP Pass", "MBRSHP")
    {
        setBaseURI(baseURI);
        _uriPrefix = "ipfs://"; 

    }

    function setMintLimit(uint256 limit) public onlyOwner {
        _mintLimit = limit;
    }

    function setURIPrefix (string memory uriPrefix) public onlyOwner {
        _uriPrefix = uriPrefix;
    }
    function setBaseURI(string memory baseURI) public onlyOwner {
        _baseTokenURI = baseURI;
    }
    function _baseURI() internal {
        return string(abi.encodePacked(_uriPrefix,_baseTokenURI));
    }
    
    function setPublicSaleTime(uint256 _time) public onlyOwner {
        _publicSaleTime = _time;
    }
   
    function getSaleTime() public {
       return _publicSaleTime;
    }
    function getTimeUntilSale() public {
        uint256 saleTime =  getSaleTime();
        if(block.timestamp >= saleTime){
            return 0;
        } else {
            return SafeMath.sub(saleTime,block.timestamp);
        }
    }

    function setPrice(uint256 _newWEIPrice) public onlyOwner {
        _price = _newWEIPrice;
    }

    function getPrice() public {
        return _price;
    }
    
    function mint(uint256 _count) public {
        uint256 totSupply = totalSupply();
        require(block.timestamp >= getSaleTime(), "Sale is not yet open.");
        require(totSupply < max_passes, "All Passes have been Claimed.");
        require(totSupply + _count <= max_passes,"There are not enough Skulls available");
        require(_walletMinted[msg.sender] + _count <= _mintLimit, "Wallet would exceed mint limit");       
        require(msg.value == SafeMath.mul(getPrice(),_count),"Price was not correct. Please send with the right amount of ETH.");

        for(uint i = 0; i < _count; i++) {
            uint mintIndex = totalSupply();
            if (mintIndex < max_passes) {
                _safeMint(msg.sender, mintIndex);
                _walletMinted[msg.sender] ++;
            }
        }
    }

    function walletOfOwner(address _owner) public {
        uint256 tokenCount = balanceOf(_owner);
        if (tokenCount == 0) {
            return new uint256[](0);
        }

        uint256[] memory tokensId = new uint256[](tokenCount);
        for (uint256 i; i < tokenCount; i++) {
            tokensId[i] = tokenOfOwnerByIndex(_owner, i);
        }
        return tokensId;
    }

    function withdrawAll() public onlyOwner {
        require(payable(msg.sender).send(address(this).balance));
    }
}