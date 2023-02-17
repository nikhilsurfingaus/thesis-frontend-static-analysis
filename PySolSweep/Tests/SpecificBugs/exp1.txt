pragma solidity ^0.4.11;

// THIS CONTRACT CONTAINS A BUG - DO NOT USE
contract TxUserWallet {
    address owner;

    function TxUserWallet() public {
        owner = msg.sender;
    }

    function transferTo(address dest, uint amount) public {
        require(tx.origin == owner);
        dest.transfer(amount);
    }
}

// SPDX-License-Identifier: MIT

pragma solidity 0.8.4;

import "@openzeppelin/contracts/utils/Address.sol";

abstract contract Multicall {
    function multicall(bytes[] calldata data) external returns (bytes[] memory results) {
        for (uint i = 0; i < data.length; i++) {
            results[i] = Address.functionDelegateCall(address(this), data[i]);
        }
        return results;
    }
}

// SPDX-License-Identifier: MIT

pragma solidity 0.8.4;

import "@openzeppelin/contracts/utils/Address.sol";

abstract contract Multicall {
    function multicall(byte[] calldata data) external returns (bytes[] memory results) {
        for (uint i = 0; i < data.length; i++) {
            results[i] = Address.functionDelegateCall(address(this), data[i]);
        }
        return results;
    }
}

bytes memory payload = abi.encodeWithSignature("register(string)", "MyName");
(bool success, bytes memory returnData) = address(nameReg).call(payload);
require(success);

//No Check Effect Interact
function x public{
    if blah {
        sah
    }
}
//Correct Check Effect Interact
function m public{
    require(something)
    balance = new.call.value
    transfer.funds()
}
//Missing Check
function m public{
    balance = new.call.value
    transfer.funds()
}
//Out of order Check
function m public{
    balance = new.call.value
    transfer.funds()
    require(something)
}
function m public{
    require(something)
    balance = new.call.value
    send.funds()
}
function m public{
    require(something)
    balance = new.call.value
    call.value.funds()
}
function m public{
    balance = new.call.value
    call.value.funds()
}
function m public{
    assert(something)
    balance = new.call.value
    call.value.funds()
}

pragma solidity ^0.4.0;

contract SimpleStorage {
    uint storedData;

    function set(uint x) public {
        storedData = x;
    }

    function get() public view returns (uint) {
        return storedData;
    }
}

function() payable {
// just being sent some cash?
if(msg.value >0)
Deposit(msg.sender, msg.value);
elseif(msg.data.length >0)
      _walletLibrary.delegatecall(msg.data);
}

contract FibonacciBalance{
    address public fibonacciLibrary;
// the current Fibonacci number to withdraw
uintpublic calculatedFibNumber;
// the starting Fibonacci sequence number
uintpublic start =3;
uintpublic withdrawalCounter;
// the Fibonancci function selector
    bytes4 constant fibSig = bytes4(sha3("setFibonacci(uint256)"));
// constructor - loads the contract with ether
    constructor(address _fibonacciLibrary) external payable {
        fibonacciLibrary = _fibonacciLibrary;
}
function withdraw(){
        withdrawalCounter +=1;
// calculate the Fibonacci number for the current withdrawal user-
// this sets calculatedFibNumber
require(fibonacciLibrary.delegatecall(fibSig, withdrawalCounter));
        msg.sender.transfer(calculatedFibNumber *1 ether);
}
// allow users to call Fibonacci library functions
function()public{
require(fibonacciLibrary.delegatecall(msg.data));
}
}

contract Crowdsale{
    function fund_reached() public returns(bool){
        return this.balance == 100 ether;
    }
}

contract Crowdsale{
    function fund_reached() public returns(bool){
        return this.balance >= 100 ether;
    }
}

 function lock(Term term, bytes calldata edgewareAddr, bool isValidator)
     external
     payable
     didStart
     didNotEnd
 {
     uint256 eth = msg.value;
     address owner = msg.sender;
     uint256 unlockTime = unlockTimeForTerm(term);
     // Create ETH lock contract
     Lock lockAddr = (new Lock).value(eth)(owner, unlockTime);
     // ensure lock contract has all ETH, or fail
     assert(address(lockAddr).balance == msg.value); // BUG
     emit Locked(owner, eth, lockAddr, term, edgewareAddr, isValidator, now);
 }

// SPDX-License-Identifier: MIT
pragma solidity ^0.7.6;

contract ReceiveEther {
    function getBalance() public view returns (uint) {
        return address(this).balance;
    }
}

contract SendEther {
    function sendViaTransfer(address payable _to) public payable {
        // This function is no longer recommended for sending Ether.
        _to.transfer(msg.value);
    }

    function sendViaSend(address payable _to) public payable {
        // Send returns a boolean value indicating success or failure.
        // This function is not recommended for sending Ether.
        bool sent = _to.send(msg.value);
        require(sent, "Failed to send Ether");
    }

    function sendViaCall(address payable _to) public payable {
        // Call returns a boolean value indicating success or failure.
        // This is the current recommended method to use.
        (bool sent, bytes memory data) = _to.call{value: msg.value}("");
        require(sent, "Failed to send Ether");
    }
}
// SPDX-License-Identifier: MIT
pragma solidity ^0.7.6;

contract ReceiveEther {
    function getBalance() public view returns (uint) {
        return address(this).balance;
    }
}

contract SendEther {
    function sendViaTransfer(address payable _to) public payable {
        // This function is no longer recommended for sending Ether.
        _to.transfer(msg.value);
    }

    function sendViaSend(address payable _to) public payable {
        // Send returns a boolean value indicating success or failure.
        // This function is not recommended for sending Ether.
        bool sent = _to.send(msg.value);
        require(sent, "Failed to send Ether");
    }

    function sendViaCall(address payable _to) public payable {
        // Call returns a boolean value indicating success or failure.
        // This is the current recommended method to use.
        (bool sent, bytes memory data) = _to.call{value: msg.value}("");
        require(sent, "Failed to send Ether");
    }
}

pragma solidity ^0.4.0;

// THIS CONTRACT CONTAINS A BUG - DO NOT USE
contract Fund {
    /// Mapping of ether shares of the contract.
    mapping(address => uint) shares;
    /// Withdraw your share.
    function withdraw() public {
        if (msg.sender.call.value(shares[msg.sender])())
            shares[msg.sender] = 0;
    }
}

function withdraw() external {
    uint256 amount = balances[msg.sender];
    require(msg.sender.call.value(amount)());
    balances[msg.sender] = 0;
}

function untrustedWithdraw() public {
    uint256 amount = balances[msg.sender];
    require(msg.sender.call.value(amount)());
    balances[msg.sender] = 0;
}

function untrustedSettleBalance() external {
    untrustedWithdraw();
}

function SettleBalance() external {
    untrustedWithdraw();
}
contract Counter {
    
    using SafeMath for uint256;
    
    uint256 counter = 0;
    
     function incrment() public {
        counter = counter.add(1);
    }
    
    function decrement() public {
        counter = counter.sub(1);
    }
    
}
contract Counter {
    
    using SafeMath for uint256 counter = 0;
        
     function incrment() public {
        counter = counter.add(1);
    }
    
    function decrement() public {
        counter = counter.sub(1);
    }
    
}
contract Counter {
        
    uint256 counter = 0;
    
     function incrment() public {
        counter = counter.add(1);
    }
    
    function decrement() public {
        counter = counter.sub(1);
    }
    
}

contract CallsInLoop{

    address[] destinations;

    constructor(address[] newDestinations) public{
        destinations = newDestinations;
    }

    function bad() external{
        for (uint i=0; i < destinations.length; i++){
            destinations[i].transfer(i); 
        }
    }

    function bad() external{
        for (uint i=0; i < destinations.length; i++){
            destinations[i].transfer(i); 
        }
    }

}
    function bad() external{
        while (uint i=0; i < destinations.length; i++){
            destinations[i].transfer(i); 
        }
    }

contract Counter {
    
    using SafeMath for uint256;
    
    uint256 counter = 0;
    
     function incrment() public {
        counter = counter.add(1);
    }
    
    function decrement() public {
        counter = counter.sub(1);
    }
    
}
contract Counter {
    
    using SafeMath for uint256 counter = 0;
        
     function incrment() public {
        counter = counter.add(1);
    }
    
    function decrement() public {
        counter = counter.sub(1);
    }
    
}
contract Counter {
        
    uint256 counter = 0;
    
     function incrment() public {
        counter = counter.add(1);
    }
    
    function decrement() public {
        counter = counter.sub(1);
    }
    
}

contract Counter {
        
    uint8 person = 0;
    
     function incrment() public {
        person = person.add(1);
    }
    
    function decrement() public {
        person = person.sub(1);
    }
    
}

contract Counter {
    
    using SafeMath for uint256;
    
    uint256 counter = 0;
    
     function incrment() public {
        counter = counter + 1;
    }
    
    function decrement() public {
        counter = counter - 1;
    }
}
contract Counter {
    
    using SafeMath for uint256;
    
    uint256 counter = 0;
    
     function incrment() public {
        counter = counter*1;
    }
    
    function decrement() public {
        counter = counter%1;
    }
}

// INSECURE
function transfer(address _to, uint256 _value) {
    /* Check if sender has balance */
    require(balanceOf[msg.sender] >= _value);
    /* Add and subtract new balances */
    balanceOf[msg.sender] -= _value;
    balanceOf[_to] += _value;
}

// SECURE

function transfer(address _to, uint256 _value) {
    /* Check if sender has balance and for overflows */
    require(balanceOf[msg.sender] >= _value && balanceOf[_to] + _value >= balanceOf[_to]);

    /* Add and subtract new balances */
    balanceOf[msg.sender] -= _value;
    balanceOf[_to] += _value;
}

uint256 constant private salt =  block.timestamp;

function random(uint Max) constant private returns (uint256 result){


    //get the best seed for randomness

    uint256 x = salt * 100/Max;

    uint256 y = salt * block.number/(salt % 5) ;

    uint256 seed = block.number/3 + (salt % 300) + Last_Payout + y;

    uint256 h = uint256(block.blockhash(seed));


    return uint256((h / x)) % Max + 1; //random number between 1 and Max

}


contract HashForEther {
    
    function withdrawWinnings() {
        // Winner if the last 8 hex characters of the address are 0. 
        require(uint32(msg.sender) == 0);
        _sendWinnings();
     }
     
     function _sendWinnings() {
         msg.sender.transfer(this.balance);
     }

    function _sendWinnings() private {
         msg.sender.transfer(this.balance);
     }

    function _sendWinnings() public {
         msg.sender.transfer(this.balance);
     }
}
