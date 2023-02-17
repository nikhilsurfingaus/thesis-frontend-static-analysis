pragma solidity ^0.8.11;


contract LoveFen is ERC721,Ownable  {
    uint256 public tokenCounter;

    mapping (uint256 => string) private _tokenURIs;
    mapping (uint256 => uint256) private _tokenValues;  

    constructor()  ERC721 ("Love Lin Ya Fen Forever","LLYFF") {
        tokenCounter = 0;
    }
    
       modifier existToken(uint256 _tokenId) {
         require(_exists(_tokenId), "Nonexistent token!");
        _;
    }

    function tokenURI(uint256 _tokenId) public {
        return _tokenURIs[_tokenId];
    }

    function tokenValue(uint256 _tokenId) public  {
        return _tokenValues[_tokenId];
    }

    
    function createCollectible(string memory _tokenURI) public onlyOwner  {
        uint256 newItemId = tokenCounter;
        _safeMint(msg.sender, newItemId);
        _tokenURIs[newItemId] = _tokenURI;
        _tokenValues[newItemId] = msg.value;
        tokenCounter ++;
        return newItemId;
    }



    function burnCollectible(uint256 _tokenId) public {
        require(_isApprovedOrOwner(msg.sender, _tokenId), "ERC721: transfer caller is not owner nor approved");
        _burn(_tokenId);

        (bool sent, ) = msg.sender.call{value: _tokenValues[_tokenId]}("");
        require(sent, "Failed to send Ether");

    }
}