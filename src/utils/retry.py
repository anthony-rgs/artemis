import sys
import time
from src.config import MAX_RETRIES, RETRY_WAIT_TIME
from src.utils.logger import logger

# Executes a function and allows retrying it in case of an error.
def retry_function(func, *args, **kwargs):
  for attempt in range(1, MAX_RETRIES + 1):

    try:
      return func(*args, **kwargs)  # Execute the function with its arguments

    except Exception:
      logger.error(f"❌ Error detected for function '{func.__name__}'", exc_info=True)
      
      if attempt == MAX_RETRIES:
        logger.critical(f"💀 Maximum retries reached. Aborting\n")
        sys.exit(1)  # Close script

      if RETRY_WAIT_TIME > 0:
        logger.info(f"🔄 Retrying in {RETRY_WAIT_TIME} seconds...\n")
        time.sleep(RETRY_WAIT_TIME)