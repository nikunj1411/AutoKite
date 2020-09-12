"""This modules contains all generic methods.

Date Created: 6-Sept-2020
Author: Nikunj Soni (nks141197@gmail.com)
"""

import pandas as pd

from retry import retry

from framework.connection.connect import generate_session
from framework.logging.logger import ERROR, INFO


@retry(tries=3, delay=10)
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
