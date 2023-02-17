pragma solidity 0.8.11;

contract YobotERC721LimitOrder is Coordinator {
    struct Order {
        address owner;
        address tokenAddress;
        uint256 priceInWeiEach;
        uint256 quantity;
        uint256 num;
    }

    uint256 public orderId = 1;

    mapping(uint256 => Order) public orderStore;
    mapping(address => mapping(uint256 => uint256)) public userOrders;
    mapping(address => uint256) public userOrderCount;
    mapping(address => uint256) public balances;

    constructor(address _profitReceiver, uint32 _botFeeBips) Coordinator(_profitReceiver, _botFeeBips) {}


    function placeOrder(address _tokenAddress, uint256 _quantity) external {

        if (msg.sender != tx.origin) revert NonEOA();
        uint256 priceInWeiEach = msg.value / _quantity;
        if (priceInWeiEach == 0 || _quantity == 0) revert InvalidAmount(msg.sender, priceInWeiEach, _quantity, _tokenAddress);

        uint256 currOrderId = orderId;
        orderId += 1;

        uint256 currUserOrderCount = userOrderCount[msg.sender];

        orderStore[currOrderId].owner = msg.sender;
        orderStore[currOrderId].tokenAddress = _tokenAddress;
        orderStore[currOrderId].priceInWeiEach = priceInWeiEach;
        orderStore[currOrderId].quantity = _quantity;
        orderStore[currOrderId].num = currUserOrderCount;

        userOrders[msg.sender][currUserOrderCount] = currOrderId;
        userOrderCount[msg.sender] += 1;

        emit Action(msg.sender, _tokenAddress, priceInWeiEach, _quantity, "ORDER_PLACED", currOrderId, currUserOrderCount, 0);
    }

    
    function cancelOrder(uint256 _orderNum) external {
        uint256 currUserOrderCount = userOrderCount[msg.sender];
        if (_orderNum >= currUserOrderCount) revert OrderOOB(msg.sender, _orderNum, currUserOrderCount);

        uint256 currOrderId = userOrders[msg.sender][_orderNum];
        
        if (currOrderId == 0) revert OrderNonexistent(msg.sender, _orderNum, currOrderId);
        Order memory order = orderStore[currOrderId];
        uint256 amountToSendBack = order.priceInWeiEach * order.quantity;
        if (amountToSendBack == 0) revert InvalidAmount(msg.sender, order.priceInWeiEach, order.quantity, order.tokenAddress);
        delete orderStore[currOrderId];
        delete userOrders[msg.sender][_orderNum];
        sendValue(payable(msg.sender), amountToSendBack);
        emit Action(msg.sender, order.tokenAddress, order.priceInWeiEach, order.quantity, "ORDER_CANCELLED", currOrderId, _orderNum, 0);
    }

    function fillOrder(uint256 _orderId, uint256 _tokenId, uint256 _expectedPriceInWeiEach, address _profitTo, bool _sendNow) public {
        Order storage order = orderStore[_orderId];

        uint256 orderIdFromMap = userOrders[order.owner][order.num];
        if (order.quantity == 0 || order.priceInWeiEach == 0 || orderIdFromMap == 0) revert InvalidAmount(order.owner, order.priceInWeiEach, order.quantity, order.tokenAddress);

        if (order.priceInWeiEach < _expectedPriceInWeiEach) revert InsufficientPrice(msg.sender, _orderId, _tokenId, _expectedPriceInWeiEach, order.priceInWeiEach);

        IERC721(order.tokenAddress).safeTransferFrom(msg.sender, order.owner, _tokenId);
        
        order.quantity -= 1;
        uint256 botFee = (order.priceInWeiEach * botFeeBips) / 10_000;
        balances[profitReceiver] += botFee;

        uint256 botPayment = order.priceInWeiEach - botFee;
        if (_sendNow) {
            sendValue(payable(_profitTo), botPayment);
        } else {
            balances[_profitTo] += botPayment;
        }

        emit Action(order.owner, order.tokenAddress, order.priceInWeiEach, order.quantity, "ORDER_FILLED", _orderId, order.num, _tokenId);

        if (order.quantity == 0) {
            delete orderStore[_orderId];
            userOrders[order.owner][order.num] = 0;
        }

        return botPayment;
    }


    function fillMultipleOrdersOptimized(uint256[] memory _orderIds, uint256[] memory _tokenIds, uint256[] memory _expectedPriceInWeiEach, address _profitTo, bool _sendNow) external {
        if (_orderIds.length != _tokenIds.length || _tokenIds.length != _expectedPriceInWeiEach.length) revert InconsistentArguments(msg.sender);
        uint256[] memory output = new uint256[](_orderIds.length);
        for (uint256 i = 0; i < _orderIds.length; i++) {
            output[i] = fillOrder(_orderIds[i], _tokenIds[i], _expectedPriceInWeiEach[i], _profitTo, _sendNow);
        }
        return output;
    }

    function fillMultipleOrdersUnOptimized(uint256[] memory _orderIds, uint256[] memory _tokenIds, uint256[] memory _expectedPriceInWeiEach, address[] memory _profitTo, bool[] memory _sendNow) external {
        if (
            _orderIds.length != _tokenIds.length
            || _tokenIds.length != _expectedPriceInWeiEach.length
            || _expectedPriceInWeiEach.length != _profitTo.length
            || _profitTo.length != _sendNow.length
        ) revert InconsistentArguments(msg.sender);

        uint256[] memory output = new uint256[](_orderIds.length);
        for (uint256 i = 0; i < _orderIds.length; i++) {
            output[i] = fillOrder(_orderIds[i], _tokenIds[i], _expectedPriceInWeiEach[i], _profitTo[i], _sendNow[i]);
        }
        return output;
    }

    function withdraw() external {
        uint256 amount = balances[msg.sender];
        delete balances[msg.sender];
        sendValue(payable(msg.sender), amount);
    }


    function sendValue(address payable recipient, uint256 amount) internal {
        require(address(this).balance >= amount, "Address: insufficient balance");
        (bool success, ) = recipient.call{value: amount}("");
        require(success, "Address: unable to send value, recipient may have reverted");
    }

    function viewUserOrder(address _user, uint256 _orderNum) public {
        uint256 _orderId = userOrders[_user][_orderNum];
        if (_orderId == 0) revert OrderNonexistent(_user, _orderNum, _orderId);
        return orderStore[_orderId];
    }

    function viewUserOrders(address _user) public {
        uint256 _userOrderCount = userOrderCount[_user];
        output = new Order[](_userOrderCount);
        for (uint256 i = 0; i < _userOrderCount; i += 1) {
            uint256 _orderId = userOrders[_user][i];
            output[i] = orderStore[_orderId]; 
        }
    }


    function viewMultipleOrders(address[] memory _users) public {
        Order[][] memory output = new Order[][](_users.length);
        for (uint256 i = 0; i < _users.length; i++) {
            output[i] = viewUserOrders(_users[i]);
        }
    }
}