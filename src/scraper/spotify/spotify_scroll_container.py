from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from src.config import SPOTIFY_SCROLL_CONTAINER
from src.utils.logger import logger 

# Retrieves the Spotify scroll container that holds the track list
def get_spotify_scroll_container(driver):
  logger.info("🚀 Starting retrieval of scroll container...")

  try:
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, SPOTIFY_SCROLL_CONTAINER)))
    containers = driver.find_elements(By.CSS_SELECTOR, SPOTIFY_SCROLL_CONTAINER)

    if len(containers) < 2:
      logger.error("❌ Scroll container not found or incomplete")
      return None

    logger.info("✅ Scroll container retrieved\n")
    return containers[2]  # The third container holds the track list

  except Exception as e:
    logger.error(f"❌ Error retrieving the scroll container: {e}", exc_info=True)
    return None
