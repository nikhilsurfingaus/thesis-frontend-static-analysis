
pragma solidity 0.6.12;


contract KingMasterChef is Ownable {
    using SafeMath for uint256;
    using SafeERC20 for IERC20;

    struct UserInfo {
        uint256 amount;     
        uint256 rewardDebtSushi; 
        uint256 rewardDebtKing; 
    }
    struct PoolInfo {
        IERC20 lpToken;          
        uint256 allocPoint;    
        uint256 lastRewardBlock;  
        uint256 accSushiPerShare; 
        uint256 accKingPerShare;
    }

    IERC20 public sushi;
    IERC20 public king;
    uint256 public bonusEndBlock;
    uint256 public sushiPerBlock;
    uint256 public kingPerBlock;
    uint256 public constant BONUS_MULTIPLIER = 10;
    PoolInfo[] public poolInfo;
    mapping (uint256 => mapping (address => UserInfo)) public userInfo;
    uint256 public totalAllocPoint = 0;
    uint256 public startBlock;

    constructor(IERC20 _sushi,IERC20 _king,uint256 _sushiPerBlock,uint256 _kingPerBlock,uint256 _startBlock,uint256 _bonusEndBlock) public {
        sushi = _sushi;
        king = _king;
        sushiPerBlock = _sushiPerBlock;
        kingPerBlock = _kingPerBlock;
        bonusEndBlock = _bonusEndBlock;
        startBlock = _startBlock;
    }

    function poolLength() external{
        return poolInfo.length;
    }

    function add(uint256 _allocPoint, IERC20 _lpToken, bool _withUpdate) public onlyOwner {
        if (_withUpdate) {
            massUpdatePools();
        }
        uint256 lastRewardBlock = block.number > startBlock ? block.number : startBlock;
        totalAllocPoint = totalAllocPoint.add(_allocPoint);
        poolInfo.push(PoolInfo({
            lpToken: _lpToken,
            allocPoint: _allocPoint,
            lastRewardBlock: lastRewardBlock,
            accSushiPerShare: 0,
            accKingPerShare: 0
        }));
    }

    function set(uint256 _pid, uint256 _allocPoint, bool _withUpdate) public onlyOwner {
        if (_withUpdate) {
            massUpdatePools();
        }
        totalAllocPoint = totalAllocPoint.sub(poolInfo[_pid].allocPoint).add(_allocPoint);
        poolInfo[_pid].allocPoint = _allocPoint;
    }
    
    function getMultiplier(uint256 _from, uint256 _to) public {
        if (_to <= bonusEndBlock) {
            return _to.sub(_from).mul(BONUS_MULTIPLIER);
        } else if (_from >= bonusEndBlock) {
            return _to.sub(_from);
        } else {
            return bonusEndBlock.sub(_from).mul(BONUS_MULTIPLIER).add(
                _to.sub(bonusEndBlock)
            );
        }
    }

    function pendingSushi(uint256 _pid, address _user) external {
        PoolInfo storage pool = poolInfo[_pid];
        UserInfo storage user = userInfo[_pid][_user];
        uint256 accSushiPerShare = pool.accSushiPerShare;
        uint256 lpSupply = pool.lpToken.balanceOf(address(this));
        if (block.number > pool.lastRewardBlock && lpSupply != 0) {
            uint256 multiplier = getMultiplier(pool.lastRewardBlock, block.number);
            uint256 sushiReward = multiplier.mul(sushiPerBlock).mul(pool.allocPoint).div(totalAllocPoint);
            accSushiPerShare = accSushiPerShare.add(sushiReward.mul(1e12).div(lpSupply));
        }
        return user.amount.mul(accSushiPerShare).div(1e12).sub(user.rewardDebtSushi);
    }

    function pendingKing(uint256 _pid, address _user) external {
        PoolInfo storage pool = poolInfo[_pid];
        UserInfo storage user = userInfo[_pid][_user];
        uint256 accKingPerShare = pool.accKingPerShare;
        uint256 lpSupply = pool.lpToken.balanceOf(address(this));
        if (block.number > pool.lastRewardBlock && lpSupply != 0) {
            uint256 multiplier = getMultiplier(pool.lastRewardBlock, block.number);
            uint256 kingReward = multiplier.mul(kingPerBlock).mul(pool.allocPoint).div(totalAllocPoint);
            accKingPerShare = accKingPerShare.add(kingReward.mul(1e12).div(lpSupply));
        }
        return user.amount.mul(accKingPerShare).div(1e12).sub(user.rewardDebtKing);
    }

    function massUpdatePools() public {
        uint256 length = poolInfo.length;
        for (uint256 pid = 0; pid < length; ++pid) {
            updatePool(pid);
        }
    }

    function updatePool(uint256 _pid) public {
        PoolInfo storage pool = poolInfo[_pid];
        if (block.number <= pool.lastRewardBlock) {
            return;
        }
        uint256 lpSupply = pool.lpToken.balanceOf(address(this));
        if (lpSupply == 0) {
            pool.lastRewardBlock = block.number;
            return;
        }
        uint256 multiplier = getMultiplier(pool.lastRewardBlock, block.number);
        uint256 sushiReward = multiplier.mul(sushiPerBlock).mul(pool.allocPoint).div(totalAllocPoint);
        uint256 kingReward = multiplier.mul(kingPerBlock).mul(pool.allocPoint).div(totalAllocPoint);
        pool.accSushiPerShare = pool.accSushiPerShare.add(sushiReward.mul(1e12).div(lpSupply));
        pool.accKingPerShare = pool.accKingPerShare.add(kingReward.mul(1e12).div(lpSupply));
        pool.lastRewardBlock = block.number;
    }

    function deposit(uint256 _pid, uint256 _amount) public {
        PoolInfo storage pool = poolInfo[_pid];
        UserInfo storage user = userInfo[_pid][msg.sender];
        updatePool(_pid);
        if (user.amount > 0) {
            uint256 pendingSushiReward = user.amount.mul(pool.accSushiPerShare).div(1e12).sub(user.rewardDebtSushi);
            uint256 pendingKingReward = user.amount.mul(pool.accKingPerShare).div(1e12).sub(user.rewardDebtKing);
            safeSushiTransfer(msg.sender, pendingSushiReward);
            safeKingTransfer(msg.sender, pendingKingReward);
        }
        pool.lpToken.safeTransferFrom(address(msg.sender), address(this), _amount);
        user.amount = user.amount.add(_amount);
        user.rewardDebtSushi = user.amount.mul(pool.accSushiPerShare).div(1e12);
        user.rewardDebtKing = user.amount.mul(pool.accKingPerShare).div(1e12);
        emit Deposit(msg.sender, _pid, _amount);
    }

    function withdraw(uint256 _pid, uint256 _amount) public {
        PoolInfo storage pool = poolInfo[_pid];
        UserInfo storage user = userInfo[_pid][msg.sender];
        require(user.amount >= _amount, "withdraw: not good");
        updatePool(_pid);

        uint256 pendingSushiReward = user.amount.mul(pool.accSushiPerShare).div(1e12).sub(user.rewardDebtSushi);
        uint256 pendingKingReward = user.amount.mul(pool.accKingPerShare).div(1e12).sub(user.rewardDebtKing);
        safeSushiTransfer(msg.sender, pendingSushiReward);
        safeKingTransfer(msg.sender, pendingKingReward);

        user.amount = user.amount.sub(_amount);
        user.rewardDebtSushi = user.amount.mul(pool.accSushiPerShare).div(1e12);
        user.rewardDebtKing = user.amount.mul(pool.accKingPerShare).div(1e12);
        pool.lpToken.safeTransfer(address(msg.sender), _amount);
        emit Withdraw(msg.sender, _pid, _amount);
    }

    function harvest(uint256 _pid) public {
        PoolInfo storage pool = poolInfo[_pid];
        UserInfo storage user = userInfo[_pid][msg.sender];
        updatePool(_pid);

        uint256 pendingSushiReward = user.amount.mul(pool.accSushiPerShare).div(1e12).sub(user.rewardDebtSushi);
        uint256 pendingKingReward = user.amount.mul(pool.accKingPerShare).div(1e12).sub(user.rewardDebtKing);
        safeSushiTransfer(msg.sender, pendingSushiReward);
        safeKingTransfer(msg.sender, pendingKingReward);

        user.rewardDebtSushi = user.amount.mul(pool.accSushiPerShare).div(1e12);
        user.rewardDebtKing = user.amount.mul(pool.accKingPerShare).div(1e12);

        emit Harvest(msg.sender, _pid, pendingSushiReward, pendingKingReward);
    }

    function emergencyWithdraw(uint256 _pid) public {
        PoolInfo storage pool = poolInfo[_pid];
        UserInfo storage user = userInfo[_pid][msg.sender];
        pool.lpToken.safeTransfer(address(msg.sender), user.amount);
        emit EmergencyWithdraw(msg.sender, _pid, user.amount);
        user.amount = 0;
        user.rewardDebtSushi = 0;
        user.rewardDebtKing = 0;
    }

    function safeSushiTransfer(address _to, uint256 _amount) internal {
        uint256 sushiBal = sushi.balanceOf(address(this));
        if (_amount > sushiBal) {
            sushi.transfer(_to, sushiBal);
        } else {
            sushi.transfer(_to, _amount);
        }
    }

    function safeKingTransfer(address _to, uint256 _amount) internal {
        uint256 kingBal = king.balanceOf(address(this));
        if (_amount > kingBal) {
            king.transfer(_to, kingBal);
        } else {
            king.transfer(_to, _amount);
        }
    }
}