"""This is a customized logger module for AutoKite.

Date Created: 2-Sept-2020
Author: Nikunj Soni (nks141197@gmail.com)
"""

import os
import sys
import threading
import traceback

import logging
import logging.config

logging.addLevelName(logging.WARNING, 'WARN')

def concat_thread_name(msg):
  """
  Concatenate thread name if not main thread.

  Args:
    msg (str): The message to be logged.

  Returns:
    msg (str): Concatenated message.
  """
  try:
    if str(threading.current_thread().name) != "MainThread":
      msg = " : ".join(["PID-"+str(os.getpid()),
                        threading.current_thread().name,
                        msg]).encode('utf-8')
  except Exception:
    return msg
  return msg

def ERROR(msg, sublogger_name=None):
  """Logs an error message.

  Args:
    msg (str): The message to be logged.
    sublogger_name (str): Name of the sub-logger to log through. If not
      provided, the AutoKite logger will be used directly.
  """
  logger = (logging.autokite_logger if sublogger_name is None
            else _get_sublogger(name=sublogger_name))
  logger.error(concat_thread_name(msg), extra=__extra())

def WARN(msg, sublogger_name=None):
  """Logs a warning message.

  Args:
    msg (str): The message to be logged.
    sublogger_name (str): Name of the sub-logger to log through. If not
      provided, the AutoKite logger will be used directly.
  """
  logger = (logging.autokite_logger if sublogger_name is None
            else _get_sublogger(name=sublogger_name))
  logger.warning(concat_thread_name(msg), extra=__extra())

def INFO(msg, sublogger_name=None):
  """Logs an info message.

  Args:
    msg (str): The message to be logged.
    sublogger_name (str): Name of the sub-logger to log through. If not
      provided, the AutoKite logger will be used directly.
  """
  logger = (logging.autokite_logger if sublogger_name is None
            else _get_sublogger(name=sublogger_name))
  logger.info(concat_thread_name(msg), extra=__extra())

def DEBUG(msg, sublogger_name=None):
  """Logs a debug message.

  Args:
    msg (str): The message to be logged.
    sublogger_name (str): Name of the sub-logger to log through. If not
      provided, the AutoKite logger will be used directly.
  """
  logger = (logging.autokite_logger if sublogger_name is None
            else _get_sublogger(name=sublogger_name))
  logger.debug(concat_thread_name(msg), extra=__extra())

def CRITICAL(msg, sublogger_name=None):
  """Logs a critical message.

  Args:
    msg (str): The message to be logged.
    sublogger_name (str): Name of the sub-logger to log through. If not
      provided, the AutoKite logger will be used directly.
  """
  logger = (logging.autokite_logger if sublogger_name is None
            else _get_sublogger(name=sublogger_name))
  logger.critical(concat_thread_name(msg), extra=__extra())

def configure(log_dir=None, log_file='autokite.log',
              console_only=False, level=logging.INFO):
  """Initializes and configures the loggers.

  Args:
    log_dir (str): The log folder where the logs will be created
                  Default is under $AutoKitePath/logs
    log_file (str): The log file to send the logs to.
                    Defaults to 'autokite.log'.
    console_only (bool): Whether to log to console only or to files as well.
                         Defaults to False.
    level (str): The log level.
                 Defaults to 'INFO'
  """

  # Create the loggers
  logging.autokite_logger = logging.getLogger('autokite')

  # Remove all existing handlers
  logging.autokite_logger.handlers = []

  # Disable the root logger
  logging.getLogger().disabled = True

  __set_default_config(level=level)

  if not console_only:
    logging.autokite_logger.handlers[0].stream = sys.stdout
    # Set the log directory
    if not log_dir:
      try:
        log_dir = os.path.join(os.environ.get('AUTOKITE_PATH'), 'logs')
      except Exception:
        raise Exception("AUTOKITE_PATH environment variable is not defined")

    if not os.path.exists(log_dir):
      os.makedirs(log_dir)

    os.environ['AUTOKITE_LOGDIR'] = log_dir
    os.environ['AUTOKITE_LOGFILE'] = log_file

    # Add appropriate file_handler file path and formatter.
    fh = logging.FileHandler(os.path.join(log_dir, log_file), 'a')
    formatter = _get_autokite_formatter()
    fh.setFormatter(formatter)
    fh.set_name('primary')
    logging.autokite_logger.addHandler(fh)
    sys.stderr = Tee(sys.stderr, fh.stream)
    set_level(level)

# Private class to write the stderr to both console and log file
class Tee(object):
  """This class defines a proxy to redirect stderr to both console and file.
  """
  def __init__(self, stream1, stream2):
    """Initialize Tee object.
    
    Args:
      stream1(object): File handle to write to console.
      stream2(object): File handle to write to file.
    """
    self.stream1, self.stream2 = stream1, stream2

  def write(self, msg):
    """Writes the message to file handles.

    Args:
      msg(str): Message to be written.
    """
    self.stream1.write(msg)
    self.stream2.write(msg)

  def flush(self):
    """Flush the messages written so far.
    """
    self.stream2.flush()

def set_level(level):
  """Sets the logging level to the desired one.

  Args:
    level (int): The desired log level

  Returns:
    None
  """
  logging.autokite_logger.setLevel(level)

def __extra():
  """Function to pass the callers name and line number.
  
  Returns:
    A dictionary with 'file_line' details.
  """
  frame = traceback.extract_stack()[-3]
  file_name = frame[0].split("/")[-1]
  file_line = frame[1]
  return {
    'file_line': "%s:%s" % (file_name, file_line)
  }

def __set_default_config(level=logging.INFO):
  """Sets the default logging config.
  
  Args:
    level(int): Log level.
                Default: logging.INFO
  """
  handler = logging.StreamHandler()
  formatter = _get_autokite_formatter()
  handler.setFormatter(formatter)
  handler.set_name('console')
  logging.autokite_logger.addHandler(handler)
  logging.autokite_logger.setLevel(level)
  #logging.autokite_logger.propagate = 0
  
def _get_autokite_formatter():
  """
  Method to generate the formatter for autokite logs.

  Returns:
    Formatter(loggig.formatter): AutoKite logging formatter.
  """
  
  # The formatter uses localtime for logging.
  formatter = logging.Formatter('%(asctime)s %(levelname)-5s %(file_line)s '
                                '%(message)s', datefmt='%Y-%m-%d %H:%M:%S')
  return formatter

def _get_sublogger(name):
  """Obtain a sublogger to the AutoKite Logger.

  Args:
    name (str): Name of the sublogger.

  Returns:
    logging.Logger
  """
  return logging.getLogger("autokite-" + name)

configure()