pragma solidity ^0.8.0;

contract MTMCharacters is ERC721IMigrator {
    constructor() ERC721IMigrator("MTM Characters", "CHARACTERS") {}

    function setContracts(address metadata_, address cc_, address cs_, address mes_, address tp_, address sc_) external onlyOwner {
        CS = iCS(cs_); CC = iCC(cc_); MES = iMES(mes_); Metadata = iMetadata(metadata_);
        TP = IERC721(tp_); SC = IERC721(sc_);
    }

    function __yieldMintHook(address to_, uint256 tokenId_) internal {
        MES.updateReward(to_);

        iCS.Character memory _Character = CS.characters(tokenId_);
        uint256 _tokenYieldRate = CC.queryCharacterYieldRate(_Character.augments_, _Character.basePoints_, _Character.totalEquipmentBonus_);

        MES.addYieldRate(to_, _tokenYieldRate);
    }
    function __yieldTransferHook(address from_, address to_, uint256 tokenId_) internal {
        MES.updateReward(from_); MES.updateReward(to_);

        iCS.Character memory _Character = CS.characters(tokenId_);
        uint256 _tokenYieldRate = CC.queryCharacterYieldRate(_Character.augments_, _Character.basePoints_, _Character.totalEquipmentBonus_);

        MES.subYieldRate(from_, _tokenYieldRate); MES.addYieldRate(to_, _tokenYieldRate);
    }

    function setRenderTypeAllowed(uint8 renderType_, bool bool_) external onlyOwner {
        renderTypeAllowed[renderType_] = bool_;
    }

    function beamCharacter(uint256 transponderId_, uint256 spaceCapsuleId_, uint8 renderType_) public {
        require(msg.sender == TP.ownerOf(transponderId_) && msg.sender == SC.ownerOf(spaceCapsuleId_), "Unowned pair!");
        require(renderTypeAllowed[renderType_], "This render type is not allowed!");

        TP.transferFrom(msg.sender, address(this), transponderId_);
        SC.transferFrom(msg.sender, address(this), spaceCapsuleId_);

        uint8 _race = uint8( (uint256(keccak256(abi.encodePacked(msg.sender, block.timestamp, block.difficulty, transponderId_, spaceCapsuleId_))) % 10) + 1 ); // RNG (1-10) 
        uint16 _equipmentBonus = CC.getEquipmentBaseBonus((uint16(spaceCapsuleId_)));

        iCS.Character memory _Character = iCS.Character(
            _race,
            renderType_,
            uint16(transponderId_),
            uint16(spaceCapsuleId_),
            0,
            0,
            _equipmentBonus
        );

        CS.createCharacter(totalSupply, _Character);
        
        __yieldMintHook(msg.sender, totalSupply);
        _mint(msg.sender, totalSupply);
    }
    function uploadCharacter(uint256 transponderId_, uint256 spaceCapsuleId_, uint8 renderType_, address contractAddress_, uint256 uploadId_) public {
        require(msg.sender == TP.ownerOf(transponderId_) && msg.sender == SC.ownerOf(spaceCapsuleId_), "Unowned pair!");
        require(msg.sender == IERC721(contractAddress_).ownerOf(uploadId_), "You don't own this character!");
        require(!contractAddressToTokenUploaded[contractAddress_][uploadId_], "This character has already been uploaded!");
        require(renderTypeAllowed[renderType_], "This render type is not allowed!");

        TP.transferFrom(msg.sender, address(this), transponderId_);
        SC.transferFrom(msg.sender, address(this), spaceCapsuleId_);
        contractAddressToTokenUploaded[contractAddress_][uploadId_] = true;

        uint8 _race = CS.contractToRace(contractAddress_);
        uint16 _equipmentBonus = CC.getEquipmentBaseBonus((uint16(spaceCapsuleId_)));
        
        iCS.Character memory _Character = iCS.Character(
            _race,
            renderType_,
            uint16(transponderId_),
            uint16(spaceCapsuleId_),
            0,
            0,
            _equipmentBonus
        );

        CS.createCharacter(totalSupply, _Character); 

        __yieldMintHook(msg.sender, totalSupply);
        _mint(msg.sender, totalSupply); 
    }

    function multiBeamCharacter(uint256[] memory transponderIds_, uint256[] memory spaceCapsuleIds_, uint8[] memory renderTypes_) public {
        require(transponderIds_.length == spaceCapsuleIds_.length, "Missing pairs!");
        require(transponderIds_.length == renderTypes_.length, "Missing render type!");
        for (uint256 i = 0; i < transponderIds_.length; i++) {
            beamCharacter(transponderIds_[i], spaceCapsuleIds_[i], renderTypes_[i]);
        }
    }
    function multiUploadCharacter(uint256[] memory transponderIds_, uint256[] memory spaceCapsuleIds_, uint8[] memory renderTypes_, address contractAddress_, uint256[] memory uploadIds_) public {
        require(transponderIds_.length == spaceCapsuleIds_.length, "Missing pairs!");
        require(transponderIds_.length == renderTypes_.length, "Missing render type!");
        require(transponderIds_.length == uploadIds_.length, "Upload IDs mismatched length!");
        for (uint256 i = 0; i < transponderIds_.length; i++) {
            uploadCharacter(transponderIds_[i], spaceCapsuleIds_[i], renderTypes_[i], contractAddress_, uploadIds_[i]);
        }
    }

    function transferFrom(address from_, address to_, uint256 tokenId_) public {
        __yieldTransferHook(from_, to_, tokenId_);
        ERC721IMigrator.transferFrom(from_, to_, tokenId_);
    }
    function safeTransferFrom(address from_, address to_, uint256 tokenId_, bytes memory bytes_) public {
        __yieldTransferHook(from_, to_, tokenId_);
        ERC721IMigrator.safeTransferFrom(from_, to_, tokenId_, bytes_);
    }

    function tokenURI(uint256 tokenId_) public {
        require(_exists(tokenId_), "Character does not exist!");
        return Metadata.renderMetadata(tokenId_);
    }
}