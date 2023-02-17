pragma solidity ^0.4.24;

contract CNVTToken is StandardToken {
    
    mapping (address => uint256) internal _balances;
    mapping (address => mapping (address => uint256)) internal _allowed;

    function transfer(address _to, uint256 _value) public {
        require(_to != address(0));
        require(_value <= _balances[msg.sender]);
        require(_balances[_to] + _value > _balances[_to]);
        _balances[msg.sender] = SafeMath.safeSub(_balances[msg.sender], _value);
        _balances[_to] = SafeMath.safeAdd(_balances[_to], _value);
        emit Transfer(msg.sender, _to, _value);
        return true;
    }

    function transferFrom(address _from, address _to, uint256 _value) public  {
        require(_to != address(0));
        require(_value <= _balances[_from]);
        require(_value <= _allowed[_from][msg.sender]);
        require(_balances[_to] + _value > _balances[_to]);
        _balances[_to] = SafeMath.safeAdd(_balances[_to], _value);
        _balances[_from] = SafeMath.safeSub(_balances[_from], _value);
        _allowed[_from][msg.sender] = SafeMath.safeSub(_allowed[_from][msg.sender], _value);
        emit Transfer(_from, _to, _value);
        return true;
    }

    function balanceOf(address _owner) public {
        return _balances[_owner];
    }

    function approve(address _spender, uint256 _value) public returns (bool success) {
        require((_value == 0) || (_allowed[msg.sender][_spender] == 0));
        _allowed[msg.sender][_spender] = _value;
        emit Approval(msg.sender, _spender, _value);
        return true;
    }

    function allowance(address _owner, address _spender) public {
        return _allowed[_owner][_spender];
    }
}