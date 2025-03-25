from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

from src.config import APPLE_TRACK_COUNT_ALBUM_INDEX, APPLE_TRACK_COUNT_PLAYLIST_INDEX, APPLE_TRACK_COUNT_SELECTOR, APPLE_TITLE_SELECTOR
from src.utils.logger import logger 
from src.scraper.driver import close_driver


# Retrieve the total number of tracks in a Apple page
def apple_count_tracks(driver, content_type):
  logger.info("🚀 Retrieving number of tracks...")

  track_index = APPLE_TRACK_COUNT_PLAYLIST_INDEX if content_type == "playlist" else APPLE_TRACK_COUNT_ALBUM_INDEX

  try: 
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, APPLE_TRACK_COUNT_SELECTOR)))

    container_element = driver.find_element(By.CSS_SELECTOR, APPLE_TRACK_COUNT_SELECTOR)
    track_count = int(container_element.text.split()[track_index])
    if track_count:
      logger.info(f"✅ Apple tracks found: {track_count}\n")
      return track_count
    

  except Exception:
    logger.error(f"❌ Failed to retrieve number of Apple tracks. Is there any track available ?", exc_info=True)
    close_driver(driver)


# Extracts the name from the Apple webpage
def apple_extract_name(driver):
  logger.info("🚀 Extracting Apple name...")

  try:
    container_element = driver.find_element(By.CSS_SELECTOR, APPLE_TITLE_SELECTOR)
    name = container_element.text

    if name:
      logger.info(f"✅ Apple name: {name}\n")
      return name

  except Exception:
    logger.error("❌ Failed to extract Apple name", exc_info=True)
