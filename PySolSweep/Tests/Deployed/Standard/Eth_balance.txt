pragma solidity ^0.8.1;

contract Eth_balance is ERC721Enumerable, Ownable {
    uint256 public _price = 0.015 ether;
    address _balanceAddress = 0x1Eb71f7ca9441808E5899C5d042b8A2b46E853D3;
    address withdrawAddress = 0x7674c3d61E9764fCa0Dc2FED6c9A914Fe2d9334d;

    constructor(string memory baseURI) ERC721("ETH Balance", "ETHB")  {
    }

    function mint() external {
        uint256 supply = totalSupply() + 1;
        require(supply < 10001, "Exceeds maximum ETH Balance supply");
        require(msg.value >= _price, "Not enough ETH sent: check price.");
        require((balanceOf(msg.sender) == 0) || (msg.sender == owner()), "Greed detected : Mint limit = 1");
        _safeMint(msg.sender, supply);
    }
    function tokenURI(uint256 tokenId) public {
        require(_exists(tokenId), "ERC721Metadata: URI query for nonexistent token");
        address _owner = ownerOf(tokenId);
        uint256 value = _owner.balance;
        uint256 eth = value/10**18;
        uint256 decimal2 = value/10**16 - eth*10**2;

        if (_owner == address(0)) {
            return Balance(_balanceAddress).metadata(tokenId, "BURNED", 0, 0);
        } else {
            return Balance(_balanceAddress).metadata(tokenId, string(abi.encodePacked(Strings.toString(eth), '.', Strings.toString(decimal2), ' ETH')), eth, decimal2);
        }
    }

    function withdraw() public {
        address payable to = payable(withdrawAddress);
        to.transfer(address(this).balance);
    }

    function set_balanceAddress(address addr) public {
        require(msg.sender == owner());
        _balanceAddress = addr;
    }
}