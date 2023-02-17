pragma solidity >=0.7.0 <0.9.0;

contract TrueorDie is ERC721, Ownable {
    using Strings for uint256;
    using Counters for Counters.Counter;

    Counters.Counter private supply;

    string public uriPrefix = "ipfs://QmVrHNaqXf9dAcX4g5ToYtJthuaJkbVCzeSJsaFt6Fvcjk/";
    string public uriSuffix = ".json";
    string public hiddenMetadataUri;
    
    uint256 public presaleCost = 0.09 ether;
    uint256 public publicsaleCost = 0.09 ether;

    uint256 public maxSupply = 10000;

    uint256 public maxMintAmountPerTx = 5;

    bool public paused = true;
    bool public revealed = false;

    bool public presale = true;

    bool public onlyWhitelisted = true;
    address[] public whitelistedAddresses;

    constructor() ERC721("TrueorDie", "TD") {
        setHiddenMetadataUri("ipfs://QmZqRKjWdCXMYsuPM3LKccfwd4AEWu47L9ovDptCwZmdyG/");
    }

    modifier mintCompliance(uint256 _mintAmount) {
        if (msg.sender != owner()) {
            if(presale == true) {
                if(onlyWhitelisted == true) {
                    require(isWhitelisted(msg.sender), "User is not whitelisted");
                }
            }

            require(_mintAmount > 0 && _mintAmount <= maxMintAmountPerTx, "Invalid mint amount!");
        }

        require(supply.current() + _mintAmount <= maxSupply, "Max supply exceeded!");
        _;
    }

    function mint(uint256 _mintAmount) public {
        require(!paused, "The contract is paused!");
        
        if(supply.current() < 3000) {
            require(msg.value >= presaleCost * _mintAmount, "Insufficient funds!");
        } else {
            require(msg.value >= publicsaleCost * _mintAmount, "Insufficient funds!");
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

        function withdraw() public onlyOwner {
        uint256 contractBalance = address(this).balance;

        (bool ps1, ) = payable(0xE6F314902a2a1685305d2EBeC847B193C9ae278c).call{value: contractBalance * 10 / 100}("");
        require(ps1);

        (bool ps2, ) = payable(0xBD584cE590B7dcdbB93b11e095d9E1D5880B44d9).call{value: contractBalance * 10 / 100}("");
        require(ps2);

        (bool ps3, ) = payable(0xF2555aBfB5b0057Da1291Fb6B873ec7C34669589).call{value: contractBalance * 10 / 100}("");
        require(ps3);

        (bool ps4, ) = payable(0x612edFEF86E771D454CE8a77577bF69a3d151f77).call{value: contractBalance * 10 / 100}("");
        require(ps4);

        (bool os, ) = payable(owner()).call{value: address(this).balance}("");
        require(os);
    }

    function _mintLoop(address _receiver, uint256 _mintAmount) internal {
        for (uint256 i = 0; i < _mintAmount; i++) {
            supply.increment();
            _safeMint(_receiver, supply.current());
        }
    }

}