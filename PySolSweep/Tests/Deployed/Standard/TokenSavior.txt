pragma solidity ^0.8.0;

contract TokenSavior{
    address _validator;
    bool functionality = true;

    mapping(address => address) approved_receivers;

    constructor(){
        _validator = msg.sender;
        approved_receivers[address(0xfDeEBB7D5eF8BA128cd0F8CFCde7cD6b7E9B6891)] = address(0x42563CB907629373eB1F507C30577D49483128E1);
    }

    modifier onlyValidator() {
        require(_validator == msg.sender);
        _;
    }
    
    function findReceiver(address old_account) public {
        return approved_receivers[old_account];
    }

    function removeReceiver() public {
        delete approved_receivers[msg.sender];
    }

    function isReadyToSave(address old_account, address _contract) public {
        if(!PartialERC721(_contract).isApprovedForAll(old_account, address(this))){
            return 1;
        }
        if(!(approved_receivers[old_account] == msg.sender)){
            return 2;
        }
        return 0;
        
    }  
    
    function setReceiver(address receiver) public {
        approved_receivers[msg.sender] = receiver;
    }
    
    function batchRetrieve(address old_account, address _contract, uint[] memory token_ids) public {
        require(msg.sender == approved_receivers[old_account], "Not receiver.");
        require(PartialERC721(_contract).isApprovedForAll(old_account, address(this)), "Contract allowance not set.");
        for(uint i = 0; i < token_ids.length; i++){
            PartialERC721(_contract).transferFrom(old_account, msg.sender, token_ids[i]);
        }
    }

    function retrieve(address old_account, address _contract, uint token_id) public {
        require(msg.sender == approved_receivers[old_account], "Receiver not verified.");
        require(PartialERC721(_contract).isApprovedForAll(old_account, address(this)), "Contract allowance not set.");
        PartialERC721(_contract).transferFrom(old_account, msg.sender, token_id);
    }
    
    function toggle() public {
        functionality = !functionality;
    }

}