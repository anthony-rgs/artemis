import time

from src.config import DEEZER_CLOSE_COOKIE_ID, DEEZER_SCROLL_CONTAINER
from src.utils.logger import logger 

# Retrieves the Deezer scroll container that holds the track list
def get_deezer_scroll_container(page):
  logger.info("🚀 Starting retrieval of scroll container...")

  try:
    page.wait_for_selector(DEEZER_SCROLL_CONTAINER, timeout=10_000)
    container = page.query_selector(DEEZER_SCROLL_CONTAINER)
    
    if container:
      # Close the cookie modal and wait until it is fully closed before proceeding
      cookie_button = page.query_selector(f"#{DEEZER_CLOSE_COOKIE_ID}")

      if cookie_button:
        time.sleep(2)
        cookie_button.click()
        logger.info("🍪 Cookie modal closed successfully.")
        time.sleep(1)
      
      logger.info("✅ Scroll container retrieved\n")
      return container
    else:
      logger.error("❌ Scroll container not found or incomplete")
      return None

  except Exception as e:
    logger.error(f"❌ Error retrieving the scroll container: {e}", exc_info=True)
    return None
