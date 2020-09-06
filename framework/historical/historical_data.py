"""This modules contains methods to get historical data.

Date Created: 6-Sept-2020
Author: Nikunj Soni (nks141197@gmail.com)
"""

import datetime as dt
import pandas as pd

from framework.logging.logger import DEBUG, INFO

def fetch_historical_ohlc(kite, instrument, start_date, interval):
  """
  Fetch historical data for given instrument from start_date to present date
  for given interval.

  Args:
    kite(obj): KiteConnect object.
    instrument(int): instrument_token of instrument.
    start_date(str): date in format (dd-mm-yyyy).
    interval(str): interval between consecutive data rows.

  Returns:
    (DataFrame): DataFrame with (time, open, high, low, close, volume) columns.

  """
  INFO(f"Getting historical data for {instrument} from {start_date} with "
       f"interval {interval}")
  from_date = dt.datetime.strptime(start_date, '%d-%m-%Y')
  data = pd.DataFrame(columns=['date', 'open', 'high', 'low', 'close', 'volume'])

  while True:
    if from_date.date() >= (dt.date.today() - dt.timedelta(100)):
      to_date = dt.date.today()
      DEBUG(f"Loop start-end date:{from_date.strftime('%d-%m-%Y')}-"
            f"{to_date.strftime('%d-%m-%Y')}")
      data = data.append(pd.DataFrame(kite.historical_data(instrument,
                                                           from_date,
                                                           to_date,
                                                           interval)),
                         ignore_index=True)
      break
    else:
      to_date = from_date + dt.timedelta(100)
      DEBUG(f"Loop start-end date:{from_date.strftime('%d-%m-%Y')}-"
            f"{to_date.strftime('%d-%m-%Y')}")
      data = data.append(pd.DataFrame(kite.historical_data(instrument,
                                                           from_date,
                                                           to_date,
                                                           interval)),
                         ignore_index=True)
      from_date = to_date
  data.set_index("date", inplace=True)
  return data
