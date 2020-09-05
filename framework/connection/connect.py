"""This modules is for Zerodha kiteconnect automated authentication.

Date Created: 4-Sept-2020
Author: Nikunj Soni (nks141197@gmail.com)
"""

import os
import time

from kiteconnect import KiteConnect
from selenium import webdriver

from framework.connection.credentials import CREDENTIALS
from framework.connection.html_attributes import CSS
from framework.logging.logger import DEBUG,INFO


def generate_session():
  """Generates a kite trading session.
  
  Returns:
    (str): access_token.
  """
  # Get request_token.
  request_token = _get_request_token()
  INFO(f"Request token:{request_token}")
  
  INFO("Generating trading session")
  # Create Kite object and then generate kite trading session.
  kite = KiteConnect(api_key=CREDENTIALS['api_key'])
  data = kite.generate_session(request_token, 
                               api_secret=CREDENTIALS['api_secret'])
  
  # The access_token is vaild till 6am the next day.
  INFO(f"Access token:{data['access_token']}")
  return data["access_token"]
   
def _get_request_token():
  """
  This method logins to the app created and returns the request_token from the 
  redirect url.
  
  Returns:
    (str): request_token.  
  """
  kite = KiteConnect(api_key=CREDENTIALS['api_key'])
  # Start browser object.
  DEBUG("Starting browser")
  chromedriver_path = os.environ["AUTOKITE_PATH"]+"/driver/chromedriver"
  service = webdriver.chrome.service.Service(chromedriver_path)
  service.start()
  
  # Set browser options.
  DEBUG("Setting browser options")
  options = webdriver.ChromeOptions()
  options.add_argument('--headless')
  options = options.to_capabilities()
  
  # Open kite app.
  DEBUG("Opening the web page in browser")
  driver = webdriver.Remote(service.service_url, options)
  driver.get(kite.login_url())
  driver.implicitly_wait(10)
  
  # Enter credentials and authenticate.
  INFO("Authenticating to app")
  username = driver.find_element_by_css_selector(CSS['username'])
  password = driver.find_element_by_css_selector(CSS['password'])
  username.send_keys(CREDENTIALS['user_id'])
  password.send_keys(CREDENTIALS['password'])
  driver.find_element_by_css_selector(CSS['continue']).click()
  pin = driver.find_element_by_css_selector(CSS['pin'])
  pin.send_keys(CREDENTIALS['pin'])
  driver.find_element_by_css_selector(CSS['login']).click()
  time.sleep(10)
  
  # Get request token from redirect_url.
  # The request_token is valid for few minutes only, hence generate trading 
  # session immediately after getting the request_token.
  request_token=driver.current_url.split('=')[1].split('&action')[0]
  driver.quit()
  return request_token
  