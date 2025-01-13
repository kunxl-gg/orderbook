#include <cmath>
#include <iostream>
#include <stdexcept>
#include <vector>

typedef std::int32_t Price;
typedef std::uint32_t Quantity;
typedef std::uint32_t OrderId;

struct LevelInfo {
    Price _price;
    Quantity _quantity;
};

typedef std::vector<LevelInfo> LevelInfoList;

class OrderBookLevelInfos {
public:
    OrderBookLevelInfos(const LevelInfoList &bids, const LevelInfoList &asks) :
        _bids(bids),
        _asks(asks) {}

    const LevelInfoList &getBids() const { return _bids; }
    const LevelInfoList &getAsks() const { return _asks; }

private:
    LevelInfoList _bids;
    LevelInfoList _asks;
};

enum OrderType {
    kGoodTillCanceled,
    kFillAndKill,
};

enum Side {
    kBuy,
    kSell,
};

class Order {
public:
    Order(OrderType orderType, OrderId orderId, Price price, Quantity quantity, Side side) :
        _side(side),
        _price(price),
        _quantity(quantity) {}

    OrderId getOrderId() const { return _orderId; }
    OrderType getOrderType() const { return _orderType; }
    Side getSide() const { return _side; }
    Price getPrice() const { return _price; }
    Quantity getInitialQuantity() const { return _initialQuantity; }
    Quantity getRemainingQuantity() const { return _remainingQuantity; }
    Quantity getFilledQuantity() const { return _initialQuantity - _remainingQuantity; }
    void fill(Quantity quantity) {
        if (quantity > _remainingQuantity) {
            throw std::logic_error("Order cannot be filled with more than remaining quantity");
        }
        _remainingQuantity -= quantity;
    }

private:
    OrderId _orderId;
    OrderType _orderType;
    Side _side;
    Price _price;
    Quantity _quantity;
    Quantity _initialQuantity;
    Quantity _remainingQuantity;
};

class OrderModify {
public:
    OrderModify(Price price, Side side, OrderId orderId, Quantity quantity) :
        _orderId(orderId),
        _price(price),
        _side(side),
        _quantity(quantity) {}
private:
    OrderId _orderId;
    Price _price;
    Side _side;
    Quantity _quantity;
};

int main() {

}
