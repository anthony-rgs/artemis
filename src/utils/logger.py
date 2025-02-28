import logging
import sys
from src.config import LOG_FILE, SAVE_LOG

# Handlers array
handlers = []

# File log
if SAVE_LOG:
  handlers.append(logging.FileHandler(LOG_FILE))

# Console log
handlers.append(logging.StreamHandler(sys.stdout)) 

logging.basicConfig(
  level=logging.INFO, # DEBUG - INFO - WARNING - ERROR
  format="%(asctime)s - %(levelname)s - %(message)s",
  handlers=handlers,
)

# Create the global logger
logger = logging.getLogger()
logger.info("✅ Global logger initialized successfully\n")
