from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.config import APPLE_SCROLL_CONTAINER
from src.utils.logger import logger 


# Retrieves the Apple scroll container that holds the track list
def get_apple_scroll_container(driver):
  logger.info("🚀 Starting retrieval of scroll container...")

  try:
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, APPLE_SCROLL_CONTAINER)))
    container = driver.find_element(By.CSS_SELECTOR, APPLE_SCROLL_CONTAINER)
      
    logger.info("✅ Scroll container retrieved\n")
    return container

  except Exception as e:
    logger.error(f"❌ Error retrieving the scroll container: {e}", exc_info=True)
    return None
