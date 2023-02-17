pragma solidity 0.5.8;

contract MetaPlay is ERC20 {
    string public constant name = "Meta Play";
    string public constant symbol = "MTY";
    uint8 public constant decimals = 18;
    uint256 public constant initialSupply = 1000000000 * (10 ** uint256(decimals));
    address public owner;

    constructor() public {
        super._mint(msg.sender, initialSupply);
        owner = msg.sender;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Not owner");
        _;
    }

    function _transferOwnership(address _newOwner) internal {
        require(_newOwner != address(0), "Already Owner");
        emit OwnershipTransferred(owner, _newOwner);
        owner = _newOwner;
    }

    function transfer(address _to, uint256 _value) public {
        releaseLock(msg.sender);
        return super.transfer(_to, _value);
    }

    function transferFrom(address _from, address _to, uint256 _value) public {
        releaseLock(_from);
        return super.transferFrom(_from, _to, _value);
    }

    function burn(uint256 _value) public onlyOwner {
        require(_value <= super.balanceOf(owner), "Balance is too small.");

        _burn(owner, _value);
        emit Burn(owner, _value);
    }

    function balanceOf(address _holder) public {
        uint256 lockedBalance = 0;
        for(uint256 i = 0; i < lockInfo[_holder].length ; i++ ) {
            lockedBalance = lockedBalance.add(lockInfo[_holder][i].balance);
        }
        return super.balanceOf(_holder).add(lockedBalance);
    }

    function releaseLock(address _holder) internal {

        for(uint256 i = 0; i < lockInfo[_holder].length ; i++ ) {
            if (lockInfo[_holder][i].releaseTime <= now) {
                _balances[_holder] = _balances[_holder].add(lockInfo[_holder][i].balance);
                emit Unlock(_holder, lockInfo[_holder][i].balance);
                lockInfo[_holder][i].balance = 0;

                if (i != lockInfo[_holder].length - 1) {
                    lockInfo[_holder][i] = lockInfo[_holder][lockInfo[_holder].length - 1];
                    i--;
                }
                lockInfo[_holder].length--;

            }
        }
    }
    
    function lock(address _holder, uint256 _amount, uint256 _releaseTime) public onlyOwner {
        require(super.balanceOf(_holder) >= _amount, "Balance is too small.");
        require(block.timestamp <= _releaseTime, "TokenTimelock: release time is before current time");
        
        _balances[_holder] = _balances[_holder].sub(_amount);
        lockInfo[_holder].push(
            LockInfo(_releaseTime, _amount)
        );
        emit Lock(_holder, _amount, _releaseTime);
    }

    function unlock(address _holder, uint256 i) public onlyOwner {
        require(i < lockInfo[_holder].length, "No lock information.");

        _balances[_holder] = _balances[_holder].add(lockInfo[_holder][i].balance);
        emit Unlock(_holder, lockInfo[_holder][i].balance);
        lockInfo[_holder][i].balance = 0;

        if (i != lockInfo[_holder].length - 1) {
            lockInfo[_holder][i] = lockInfo[_holder][lockInfo[_holder].length - 1];
        }
        lockInfo[_holder].length--;
    }

    function transferWithLock(address _to, uint256 _value, uint256 _releaseTime) public onlyOwner {
        require(_to != address(0), "wrong address");
        require(_value <= super.balanceOf(owner), "Not enough balance");
        require(block.timestamp <= _releaseTime, "TokenTimelock: release time is before current time");

        _balances[owner] = _balances[owner].sub(_value);
        lockInfo[_to].push(
            LockInfo(_releaseTime, _value)
        );
        emit Transfer(owner, _to, _value);
        emit Lock(_to, _value, _releaseTime);

        return true;
    }

}