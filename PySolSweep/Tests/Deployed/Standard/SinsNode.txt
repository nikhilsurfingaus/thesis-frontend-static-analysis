pragma solidity >=0.7.0 <0.9.0;

contract SinsNode is ERC721Enumerable, Ownable, ControlledAccess{
    using Strings for uint256;
    bool public autosell = false;
    string baseURI;
    string public baseExtension = ".json";
    uint256 public maxSupply = 10000000;
    uint256 public timeDeployed;
    uint256 public allowMintingAfter = 0;
    address public Sins;
    bool public isPaused = false;
    address public rewardPool;
    mapping(uint256 => uint) public nodeType;
    IUniswapV2Router02 public uniswapV2Router;
    uint256 public tax;
    uint256[5] public mintPrices=[0,0,0,0,0];

    constructor(string memory _name, string memory _symbol, string memory _initBaseURI, uint256 _revealTime,address _sinsAddress) ERC721(_name, _symbol) {
        if (_revealTime > block.timestamp) {
            allowMintingAfter = _revealTime;
        }
        Sins = _sinsAddress;
        timeDeployed = block.timestamp;
        setBaseURI(_initBaseURI);
        IUniswapV2Router02 _uniswapV2Router = IUniswapV2Router02(0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D);
        uniswapV2Router = _uniswapV2Router;
        
    }

    receive() external payable {
  	}

   
    function mint(uint _type) public {
        require(
            block.timestamp >= allowMintingAfter,
            "Minting now allowed yet"
        );
        require(_type>0 && _type<=5, "Invalid node type");

        uint256 supply = totalSupply();
        nodeType[supply+1] = _type;
        
        require(!isPaused);
        require(supply + 1 <= maxSupply);
        uint256 price = mintPrices[_type-1];
        uint256 _tax = (price*tax)/10000;

        if (msg.sender != owner()) {
            require(IERC20(Sins).transferFrom(msg.sender, address(this), price), "Not enough funds");
            IERC20(Sins).approve(address(uniswapV2Router), _tax);
            if (autosell) {
                swapTokensForEth(_tax);
            }
            IERC20(Sins).transfer(rewardPool, price-_tax);
        }
        _safeMint(msg.sender, supply + 1);
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

        string memory currentBaseURI = _baseURI();
        return
            bytes(currentBaseURI).length > 0
                ? string(
                    abi.encodePacked(
                        currentBaseURI,
                        nodeType[tokenId].toString(),
                        baseExtension
                    )
                )
                : "";
    }

    function getSecondsUntilMinting() public {
        if (block.timestamp < allowMintingAfter) {
            return (allowMintingAfter) - block.timestamp;
        } else {
            return 0;
        }
    }

    function swapTokensForEth(uint256 tokenAmount) private {

        address[] memory path = new address[](2);
        path[0] = Sins;
        path[1] = uniswapV2Router.WETH();

        IERC20(Sins).approve(address(uniswapV2Router), tokenAmount);

        uniswapV2Router.swapExactTokensForETHSupportingFeeOnTransferTokens(
            tokenAmount,
            0, 
            path,
            address(this),
            block.timestamp
        );
        
    }

    function sell(uint256 tokenAmount) public onlyOwner {

        address[] memory path = new address[](2);
        path[0] = Sins;
        path[1] = uniswapV2Router.WETH();

        IERC20(Sins).approve(address(uniswapV2Router), tokenAmount);

        uniswapV2Router.swapExactTokensForETHSupportingFeeOnTransferTokens(
            tokenAmount,
            0, 
            path,
            address(this),
            block.timestamp
        );
        
    }


    function _beforeTokenTransfer(address from, address to, uint256 tokenId) internal {
        super._beforeTokenTransfer(from, to, tokenId);
        if (from == address(0)) {
            IRewardPool(rewardPool).addNodeInfo(tokenId, nodeType[tokenId], to);        
        } else if (from != to) {
            IRewardPool(rewardPool).claimReward(tokenId);        
            IRewardPool(rewardPool).updateNodeOwner(tokenId, to);
        }
    }

    function claimRewards( address _owner) public {
        uint256[] memory tokens = walletOfOwner(_owner);
        for (uint256 i; i < tokens.length; i++) {
            IRewardPool(rewardPool).claimReward(tokens[i]);
        }
    }


    function withdraw() public onlyOwner {
        (bool success, ) = payable(msg.sender).call{
            value: address(this).balance
        }("");
        require(success);
    }
}