pragma solidity 0.8.7;

contract SuperlativeMagicLaboratory is ERC1155Burnable, Ownable, ReentrancyGuard {

    using Strings for uint256;
    SUPERLATIVEAPES public slapeContract;

    string public baseURI;
    string public baseExtension = ".json";


    uint256 constant public MagicVialMaxReserve = 3333;
    uint256 constant public MagicHerbsMaxReserve = 1106;
    uint256 constant public MagicPotsMaxReserve = 5;

    uint256 public vialMinted;
    uint256 public herbsMinted;
    uint256 public potsMinted;


    bool public WhitelistOpen = false;

    mapping (address => uint256) public totalPresaleMinted;

    mapping (address => bool) public whitelistClaim;

    constructor(string memory _initBaseURI, address slapesAddress) ERC1155(_initBaseURI) {
        setBaseURI(_initBaseURI);
        slapeContract = SUPERLATIVEAPES(slapesAddress);

        vialMinted++;
        _mint(msg.sender, 1, 1, ""); 
    }

    function randomNum(uint256 _mod, uint256 _seed, uint256 _salt) internal {
        return uint256(keccak256(abi.encodePacked(block.timestamp, msg.sender, _seed, _salt))) % _mod;
    }

    function Whitelist() public {
        bool skipHerbs = false;
        bool skipPots = false;

        require(whitelistClaim[msg.sender] == false, "You have claimed already!");
        require(slapeContract.balanceOf(msg.sender) >= 1, "You dont have anything to claim");
        require((vialMinted < MagicVialMaxReserve || herbsMinted < MagicHerbsMaxReserve || potsMinted < MagicPotsMaxReserve) , "No serums left!");

        if(potsMinted >= MagicPotsMaxReserve) {
            skipPots = true;
        }
        else if(herbsMinted >= MagicHerbsMaxReserve) {
            skipHerbs = true;
        }

        for(uint256 i=0; i<slapeContract.balanceOf(msg.sender);i++) {      
            bool notMintedYet = false;
            while(!notMintedYet) {
                uint256 selectedSerum = randomNum(12, (block.timestamp * randomNum(1000, block.timestamp, block.timestamp) * i), (block.timestamp * randomNum(1000, block.timestamp, block.timestamp) * i));
                
                if(selectedSerum == 0 && !skipPots) {
                    notMintedYet = true;
                    potsMinted++;
                    _mint(msg.sender, 3, 1, "");                   
                }
                else if(selectedSerum >= 1 && selectedSerum <= 3 && !skipHerbs) {
                    notMintedYet = true;
                    herbsMinted++;
                    _mint(msg.sender, 2, 1, "");                   
                }
                else {
                    notMintedYet = true;
                    vialMinted++;
                    _mint(msg.sender, 1, 1, "");                  
                }
            }
        }

        whitelistClaim[msg.sender] = true;

    }

    function _withdraw(address payable address_, uint256 amount_) internal {
        (bool success, ) = payable(address_).call{value: amount_}("");
        require(success, "Transfer failed");
    }

    function withdrawEther() external onlyOwner {
        _withdraw(payable(msg.sender), address(this).balance);
    }

    function withdrawEtherTo(address payable to_) external onlyOwner {
        _withdraw(to_, address(this).balance);
    }

    function uri(uint256 tokenId) public {
        string memory currentBaseURI = _baseURI();
        return bytes(currentBaseURI).length > 0 ? string(abi.encodePacked(currentBaseURI, tokenId.toString(), baseExtension)) : "";
    }
}