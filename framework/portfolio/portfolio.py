"""This modules contains methods to get portfolio related details.

Date Created: 12-Sept-2020
Author: Nikunj Soni (nks141197@gmail.com)
"""

from retry import retry

from framework.logging.logger import INFO, ERROR

@retry(tries=3, delay=5)
def get_orders(kite):
  """get current orders.

    Args:
      kite(obj):KiteConnect object.

    Returns:
      (list): list of dicts with orders info.

    """
  # Get orders.
  try:
    resp = kite.orders()

    # Return if success else raise exception.
    if resp["status"] == "success":
      INFO(f"Current orders are: {resp['data']}")
    else:
      raise Exception(f"Status:{resp['status']}, Error:{resp['error_type']}, "
                      f"Error Message:{resp['message']}")

  except Exception as ex:
    ERROR(f"Error occurred while getting orders:{ex}")
    raise
  return resp["data"]

@retry(tries=3, delay=5)
def get_positions(kite):
  """get current positions.

    Args:
      kite(obj):KiteConnect object.

    Returns:
      (list): list of dicts with positions info.

  """
  # Get positions.
  try:
    resp = kite.positions()

    # Return if success else raise exception.
    if resp["status"] == "success":
      INFO(f"Current positions are: {resp['data']}")
    else:
      raise Exception(f"Status:{resp['status']}, Error:{resp['error_type']}, "
                      f"Error Message:{resp['message']}")

  except Exception as ex:
    ERROR(f"Error occurred while getting positions:{ex}")
    raise
  return resp["data"]

@retry(tries=3, delay=5)
def get_holdings(kite):
  """get current holdings for given kite object.

  Args:
    kite(obj):KiteConnect object.

  Returns:
    (list): list of dicts with holdings info.

  """
  # Get holdings.
  try:
    resp = kite.holdings()

    # Return if success else raise exception.
    if resp["status"] == "success":
      INFO(f"Current holdings are: {resp['data']}")
    else:
      raise Exception(f"Status:{resp['status']}, Error:{resp['error_type']}, "
                      f"Error Message:{resp['message']}")

  except Exception as ex:
    ERROR(f"Error occurred while getting holdings:{ex}")
    raise
  return resp["data"]
