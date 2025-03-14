import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from src.config import DEEZER_CLOSE_COOKIE_ID, DEEZER_SCROLL_CONTAINER
from src.utils.logger import logger 

# Retrieves the Deezer scroll container that holds the track list
def get_deezer_scroll_container(driver):
  logger.info("🚀 Starting retrieval of scroll container...")

  try:
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, DEEZER_SCROLL_CONTAINER)))
    container = driver.find_element(By.TAG_NAME, DEEZER_SCROLL_CONTAINER)
    
    if container:
      # Close the cookie modal and wait until it is fully closed before proceeding
      cookie_button = driver.find_element(By.ID, DEEZER_CLOSE_COOKIE_ID)

      if cookie_button:
        time.sleep(1)
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
