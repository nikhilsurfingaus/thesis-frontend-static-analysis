pragma solidity ^0.8.0;

contract Dynamic1155 is ERC1155Burnable, Ownable {
    bool public manualMintAllowed = true;
    mapping (uint256 => string) public typeToUri;
    bool public isUriFreezed;
    mapping (uint256 => bool) public typeIsUriFreezed;
    
    constructor(string memory _uri){}
    
    function mintOwner(address[] calldata owners, uint256[] calldata types, uint256[] calldata counts) public onlyOwner {
      require(manualMintAllowed, "Not allowed");
      require(owners.length == types.length && types.length == counts.length, "Bad array lengths");
         
      for (uint256 i = 0; i < owners.length; i++) {
        _mint(owners[i], types[i], counts[i], "");
      }
    }

    function mintOwnerOneToken(address[] calldata owners, uint256 typeId) public onlyOwner {
      require(manualMintAllowed, "Not allowed");
         
      for (uint256 i = 0; i < owners.length; i++) {
        _mint(owners[i], typeId, 1, "");
      }
    }

    function uri(uint256 typeId) public {
        string memory typeUri = typeToUri[typeId];
        if (bytes(typeUri).length == 0) {
            return super.uri(typeId);
        } else {
            return typeUri;
        }
    }
   

    function updateUri(string calldata newUri) public onlyOwner {
        require(!isUriFreezed, "Freezed");
        _setURI(newUri);
    }

    function updateUriForType(string calldata newUri, uint256 typeId) public onlyOwner {
        require(!typeIsUriFreezed[typeId], "Freezed");
        typeToUri[typeId] = newUri;
    }
}