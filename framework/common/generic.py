"""This modules contains all generic methods.

Date Created: 6-Sept-2020
Author: Nikunj Soni (nks141197@gmail.com)
"""

import pandas as pd

from retry import retry

from framework.connection.connect import generate_session
from framework.logging.logger import ERROR, INFO

@retry(tries=3, delay=5)
def get_instrument_tokens(kite, instruments, exchange="NSE"):
  """Get instrument tokens for given instrument symbols of exchange.

  Args:
    kite(obj): KiteConnect object.
    instruments(list): list of symbols.
    exchange(str): Market Exchange.(BFO, BSE, NSE, NFO, MCX, CDS)
                   Default: "NSE"

  Returns:
    (dict): instrument_tokens corresponding to given instrument symbols.
            (symbol:token)

  """
  instruments_dump = kite.instruments(exchange)
  instruments_df = pd.DataFrame(instruments_dump)
  instrument_tokens = {}

  INFO(f"Instruments list:{instruments}")
  for symbol in instruments:
    try:
      token = instruments_df[instruments_df.tradingsymbol==symbol].instrument_token.values[0]
      instrument_tokens[symbol] = token
    except:
      ERROR(f"Error occurred during lookup token for symbol:{symbol}")
      raise

  INFO(f"Instrument-token dict:{instrument_tokens}")
  return instrument_tokens

@retry(tries=3, delay=10)
def get_trading_session():
  """Get kite trading session.

  Returns:
     KiteConnect(obj): KiteConnect obj.

  """
  return generate_session()

@retry(tries=3, delay=5)
def get_ltp(kite, instrument):
  """Get last traded price for an instrument.

  Args:
    kite(obj): KiteConnect object.
    instrument(str): Instrument in format "Exchange:Symbol"("NSE:INFY").

  Returns:
    (float): Last traded price.

  """
  resp = kite.ltp(instrument)
  if resp['status'] == "success":
    INFO(f"LTP for {instrument}:{resp['data'][instrument]['last_price']}")
  else:
    # Log error details and retry.
    ERROR("Error occurred while getting ltp-")
    ERROR(f"Status:{resp['status']}, Error:{resp['error_type']}, "
          f"Error Message:{resp['message']}")
    raise
  return resp['data'][instrument]['last_price']

@retry(tries=3, delay=5)
def get_quote(kite, instrument):
  """Get quote for an instrument.
  Warning: It may return a bulk object consuming lot of memory, hence avoid
  it's usage unless required.

  Args:
    kite(obj): KiteConnect object.
    instrument(str): Instrument in format "Exchange:Symbol"("NSE:INFY").

  Returns:
    (dict): the quote.

  """
  resp = kite.quote(instrument)
  if resp['status'] == "success":
    INFO(f"Quote for {instrument}: {resp['data']}")
  else:
    # Log error details and retry.
    ERROR("Error occurred while getting quote-")
    ERROR(f"Status:{resp['status']}, Error:{resp['error_type']}, "
          f"Error Message:{resp['message']}")
    raise
  return resp['data']
