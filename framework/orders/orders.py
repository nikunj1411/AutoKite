"""This modules contains methods for placing/modifying/cancelling orders.

Date Created: 12-Sept-2020
Author: Nikunj Soni (nks141197@gmail.com)
"""

from kiteconnect import KiteConnect

from framework.logging.logger import INFO, ERROR

# Market exchange map.
EXCHANGE_MAP = {
  "BSE": KiteConnect.EXCHANGE_BSE,
  "NSE": KiteConnect.EXCHANGE_NSE
}

# Transaction type map.
TRANSACTION_TYPE_MAP = {
  "buy": KiteConnect.TRANSACTION_TYPE_BUY,
  "sell": KiteConnect.TRANSACTION_TYPE_SELL
}

def place_mis_market_order(kite, instrument, type, quantity, exchange="NSE"):
  """Places an intraday market order.

  Args:
    kite(obj): KiteConnect object.
    instrument(str): Symbol of stock.
    type(str): Either "buy" or "sell"
    quantity(int): Number of shares to buy.
    exchange(str): Market exchange("NSE", "BSE").
                   Default: "NSE"

  Returns:
      (int): order_id if successful else -1.

  """
  # Get constants.
  type = TRANSACTION_TYPE_MAP[type]
  exchange = EXCHANGE_MAP[exchange]

  # Place market order.
  try:
    resp = kite.place_order(tradingsymbol=instrument, exchange=exchange,
                            transaction_type=type, quantity=quantity,
                            order_type=KiteConnect.ORDER_TYPE_MARKET,
                            product=KiteConnect.PRODUCT_MIS,
                            variety=KiteConnect.VARIETY_REGULAR)
    if resp["status"] == "success":
      INFO(f"Order placed successfully: Instrument:{exchange}:{instrument}, "
           f"Type:{type}, Quantity:{quantity}")
      return resp["data"]["order_id"]
    else:
      ERROR(f"Error while placing response")
      return -1

  except Exception as ex:
    # If any exception occurred, catch it and return an error response.
    ERROR(f"Error while placing order for {instrument}: {ex}")
    return -1

def place_mis_bracket_order(kite, instrument, type, price, quantity, target_points,
                            stoploss_points, trailing_stoploss, exchange="NSE"):
  """Places an intraday bracket order.

  Args:
    kite(obj): KiteConnect object.
    instrument(str): Symbol of stock.
    type(str): Either "buy" or "sell"
    price(float): Price at which to buy shares.
    quantity(int): Number of shares to buy.
    target_points(float):
    stoploss_points(float):
    trailing_stoploss(int): Trailing stoploss value.
                            Default: 0
    exchange(str): Market exchange("NSE", "BSE").
                   Defaults: "NSE"

  Returns:
    (int): order_id if successful else -1.

  """
  # Get constants.
  type = TRANSACTION_TYPE_MAP[type]
  exchange = EXCHANGE_MAP[exchange]

  # Place bracket order.
  try:
    resp = kite.place_order(tradingsymbol=instrument, exchange=exchange,
                            transaction_type=type, quantity=quantity,
                            order_type=KiteConnect.ORDER_TYPE_LIMIT, price=price,
                            product=KiteConnect.PRODUCT_MIS,
                            variety=KiteConnect.VARIETY_BO,
                            squareoff=target_points,stoploss=stoploss_points,
                            trailing_stoploss=trailing_stoploss)

    if resp["status"] == "success":
      INFO(f"Order placed successfully: Instrument:{exchange}:{instrument}, "
           f"Type:{type}, Quantity:{quantity}")
      return resp["data"]["order_id"]
    else:
      ERROR(f"Error while placing order for {instrument}")
      return -1

  except Exception as ex:
    # If any exception occurred, catch it and return an error response.
    ERROR(f"Error while placing order for {instrument}: {ex}")
    return -1
