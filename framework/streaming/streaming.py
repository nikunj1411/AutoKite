"""This modules contains web socket streaming methods to get live market quotes.

Date Created: 20-Sept-2020
Author: Nikunj Soni (nks141197@gmail.com)
"""

import datetime
import os
import sqlite3

from kiteconnect import KiteTicker

from config.streaming_config import tickers
from framework.common.generic import get_instrument_tokens
from framework.connection.credentials import CREDENTIALS

# Get the instrument tokens for tickes and store it.
tokens = get_instrument_tokens(tickers)

def on_ticks(ws, ticks):
  """Callback to receive ticks.

  Args:
    ws(WebSocket): Websocket object used for streaming.
    ticks(json): Quotes data.

  """
  # Insert the ticks in DB.
  _insert_ticks(ticks)

def on_connect(ws, response):
  """Callback when successful connection is established.

  Args:
    ws(WebSocket): Websocket object used for streaming.
    response(json): Response obtained for connection.

  """
  # Subscribe to a list of instrument_tokens.
  ws.subscribe(tokens)
  ws.set_mode(ws.MODE_FULL, tokens)

def setup_streaming(db_file):
  """Setup for web socket streaming.

  Args:
    db_file(str): Path where database will be created and streaming data
                  will be stored.

  """
  # Create database directory and file.
  if not db_file:
    try:
      db_dir = os.path.join(os.environ.get('AUTOKITE_PATH'), 'db')
    except Exception:
      raise Exception("AUTOKITE_PATH environment variable is not defined")

    if not os.path.exists(db_dir):
      os.makedirs(db_dir)
    db_file = os.path.join(db_dir, "ticks.db")
    os.environ['AUTOKITE_DB_DIR'] = db_dir
    os.environ['AUTOKITE_DB_FILE'] = db_file

  # Connect to the database.
  global db
  db = sqlite3.connect(db_file)
  _create_tables()

def start_streaming(kite):
  """ Start getting the live market quotes and storing it in db.

  Args:
    kite(obj): KiteConnect object.

  """
  # Create KiteTicker object and initialize the callbacks.
  kws = KiteTicker(CREDENTIALS['api_key'], kite.access_token)

  # Start streaming only during market hours.
  while True:
    now = datetime.datetime.now()
    if (now.hour >= 9 and now.minute >= 15):
      kws.on_ticks = on_ticks
      kws.on_connect = on_connect
      kws.connect()
    if (now.hour >= 15 and now.minute >= 30):
      kws.stop()
      break

  # Close the db after market closes and exit.
  db.close()

def _create_tables():
  """Create a table for each token.
  """
  cur = db.cursor()

  # Make (timestamp, ltp, volume) as columns of table.
  for token in tokens:
    cmd = f"CREATE TABLE IF NOT EXISTS TOKEN{token} (ts datetime primary key," \
          f" price real(15,5), volume integer)"
    cur.execute(cmd)

  try:
    db.commit()
  except:
    db.rollback()

def _insert_ticks(ticks):
  """Insert the ticks for token into the db tables.

  Args:
    ticks(list): list of json which has quotes for token.

  """
  cur = db.cursor()

  # For each tick insert the data as a row in db.
  for tick in ticks:
    try:
      tok = "TOKEN" + str(tick['instrument_token'])
      vals = [tick['timestamp'], tick['last_price'], tick['volume']]
      query = f"INSERT INTO {tok}(ts,price,volume) VALUES (?,?,?)"
      cur.execute(query, vals)
    except:
      pass # If timestamp remains the same and an exception is raised, ignore it.

  try:
    db.commit()
  except:
    db.rollback()
