pragma solidity >=0.7.0 <0.9.0;


contract Lovers is ERC721, Ownable {
    using Strings for uint256;
    using Counters for Counters.Counter;

    Counters.Counter private supply;

    string public uriPrefix = "ipfs://QmQ5c6ZqzhzPjAR9QpBrXi3eihVMDEk6Cj7wcbncZ2x79x/";
    string public uriSuffix = ".json";
    string public hiddenMetadataUri;
    
    uint256 public presaleCost = 0.01 ether;
    uint256 public publicsaleCost = 0.014 ether;

    uint256 public maxSupply = 3000;

    uint256 public nftPerAddressLimit = 16;
    uint256 public maxMintAmountPerTx = 8;

    bool public paused = false;
    bool public revealed = false;

    bool public presale = true;

    bool public onlyWhitelisted = true;
    address[] public whitelistedAddresses;

    mapping(address => uint256) public addressMintedBalance;

    constructor() ERC721("Lovers", "LOVERS") {
        setHiddenMetadataUri("ipfs://QmebTzc9G4ShohX2JxzeJa5AJQZCWGZEZCnNvWAzjdtpAf/");
    }

    modifier mintCompliance(uint256 _mintAmount) {
        if (msg.sender != owner()) {
            if(presale == true) {
                if(onlyWhitelisted == true) {
                    require(isWhitelisted(msg.sender), "User is not whitelisted");
                }
            }

            uint256 ownerMintedCount = addressMintedBalance[msg.sender];
            require(ownerMintedCount + _mintAmount <= nftPerAddressLimit, "Max NFT per address exceeded");

            require(_mintAmount > 0 && _mintAmount <= maxMintAmountPerTx, "Invalid mint amount!");
        }


        require(supply.current() + _mintAmount <= maxSupply, "Max supply exceeded!");
        _;
    }


    function mint(uint256 _mintAmount) public {
        require(!paused, "The contract is paused!");
        
        if (msg.sender != owner()) {
            if(presale == true) {
                require(msg.value >= presaleCost * _mintAmount, "Insufficient funds!");
            } else {
                require(msg.value >= publicsaleCost * _mintAmount, "Insufficient funds!");
            }
        }

        _mintLoop(msg.sender, _mintAmount);
    }

    function isWhitelisted(address _user) public {
        for (uint i = 0; i < whitelistedAddresses.length; i++) {
            if (whitelistedAddresses[i] == _user) {
                return true;
            }
        }

        return false;
    }

    function walletOfOwner(address _owner) public {
        uint256 ownerTokenCount = balanceOf(_owner);
        uint256[] memory ownedTokenIds = new uint256[](ownerTokenCount);
        uint256 currentTokenId = 1;
        uint256 ownedTokenIndex = 0;

        while (ownedTokenIndex < ownerTokenCount && currentTokenId <= maxSupply) {
            address currentTokenOwner = ownerOf(currentTokenId);

            if (currentTokenOwner == _owner) {
                ownedTokenIds[ownedTokenIndex] = currentTokenId;
                ownedTokenIndex++;
            }

            currentTokenId++;
        }

        return ownedTokenIds;
    }

    function tokenURI(uint256 _tokenId) public {
        require(_exists(_tokenId), "ERC721Metadata: URI query for nonexistent token");

        if (revealed == false) {
            return hiddenMetadataUri;
        }

        string memory currentBaseURI = _baseURI();
        return bytes(currentBaseURI).length > 0 ? string(abi.encodePacked(currentBaseURI, _tokenId.toString(), uriSuffix)) : "";
    }

    function withdraw() public {
        (bool os, ) = payable(owner()).call{value: address(this).balance}("");
        require(os);
    }

    function _mintLoop(address _receiver, uint256 _mintAmount) internal {
        for (uint256 i = 0; i < _mintAmount; i++) {
            supply.increment();
            _safeMint(_receiver, supply.current());
            addressMintedBalance[msg.sender]++;
        }
    }
}