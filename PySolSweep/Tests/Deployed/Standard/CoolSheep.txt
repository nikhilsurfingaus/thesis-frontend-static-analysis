pragma solidity ^0.8.0;

contract CoolSheep is Ownable, ERC721 {
    uint constant maxPerFreeMint = 1;
    uint public reservedSupply = 3000;
    uint constant tokenPrice = .02 ether;
    uint constant maxSupply = 10000;
    uint public totalSupply = 0;
    uint8 public saleStatus = 0;
    address public referenceContract = 0xb5e366c938fe38De600A7fe2F3949A9F41157FD6;

    ERC721 AlienFrens = ERC721(0x123b30E25973FeCd8354dd5f41Cc45A3065eF88C);
    ERC721 CoolDogs = ERC721(0x56681458E00CafE1206313D2D033946f458FDEfD);
    ERC721 CoolCats = ERC721(0x1A92f7381B9F03921564a437210bB9396471050C);
    ERC721 BabySpookles = ERC721(0x87e8AeE88AE939465dA795D6C32963854Bb5fBA0);

    string private baseURI;
    mapping(address => bool) private presaleList;
    mapping(address => bool) private winnerList;

    modifier mutualCheck() {
        require(saleStatus != 0, "sale is not active");
        require(totalSupply + reservedSupply < maxSupply, "all tokens have been minted");
        _;
    }

    constructor() ERC721("Cool Sheep", "CLSP"){}

    function gift() public {

        require(CoolCats.balanceOf(msg.sender) > 0 || CoolDogs.balanceOf(msg.sender) > 0 || AlienFrens.balanceOf(msg.sender) > 0 || BabySpookles.balanceOf(msg.sender)> 0 || ERC721(referenceContract).balanceOf(msg.sender) > 0, "You are not CoolCats, Cool Dogs, Alien frens holder");
        require(balanceOf(msg.sender) < maxPerFreeMint, "One token per wallet for holders");
        
        reservedSupply = reservedSupply - 1;
        _safeMint(msg.sender,++totalSupply);
    }

    function mint(uint _count) public {
        require(_count > 0, "mint at least one token");
        require(totalSupply + reservedSupply + _count <= maxSupply, "not enough tokens left");
        require(msg.value == tokenPrice * _count, "incorrect ether amount");
        for(uint i = 0; i < _count; i++)
            _safeMint(msg.sender, totalSupply + 1 + i);
        totalSupply += _count;
    }

    function sendGifts(address[] memory _wallets) public onlyOwner{
        require(totalSupply + reservedSupply + _wallets.length <= maxSupply, "not enough tokens left");
        for(uint i = 0; i < _wallets.length; i++)
            _safeMint(_wallets[i], totalSupply + 1 + i);
        totalSupply += _wallets.length;
    }

    function checkGift() public {
        return CoolCats.balanceOf(msg.sender) > 0 || CoolDogs.balanceOf(msg.sender) > 0 || AlienFrens.balanceOf(msg.sender) > 0 || BabySpookles.balanceOf(msg.sender)> 0 || ERC721(referenceContract).balanceOf(msg.sender) > 0;
    }
    function checkMaxFreeMint() public {
        return balanceOf(msg.sender) < maxPerFreeMint;
        
    }

    function addWinnerList(address[] memory _wallets) public onlyOwner{
        for(uint i; i < _wallets.length; i++)
            winnerList[_wallets[i]] = true;
    }

    function addPresaleList(address[] memory _wallets) public onlyOwner{
        for(uint i; i < _wallets.length; i++)
            presaleList[_wallets[i]] = true;
    }

    function withdraw() public onlyOwner{
        uint _balance = address(this).balance;
        payable(0xef265de68010bfC2445A66BbEd80d4C09c1E2530).transfer(_balance * 95 / 100);
        payable(0xbE60e7f33d3Bb37f4d1cEd1521A0896730bE8cE3).transfer(_balance * 3 / 100);
        payable(0xDF4f13CEb3215f39f602744284aB598AeA43CcBd).transfer(_balance * 2 / 100);
    }
}