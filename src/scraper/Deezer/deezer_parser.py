from selenium.webdriver.common.by import By
from src.config import DEEZER_INFORMATIONS_SELECTOR, DEEZER_TOTAL_TRACKS_XPATH, DEEZER_TITLE_SELECTOR
from src.utils.logger import logger 
from src.scraper.driver import close_driver

# Retrieve the total number of tracks in a Deezer page
def deezer_count_tracks(driver, _):
  logger.info("🚀 Retrieving number of tracks...")

  try: 
    container_element = driver.find_element(By.CSS_SELECTOR, DEEZER_INFORMATIONS_SELECTOR)
    track_count_item = container_element.find_element(By.XPATH, DEEZER_TOTAL_TRACKS_XPATH)
    track_count = int(track_count_item.text.split()[0])

    if track_count:
      logger.info(f"✅ Deezer tracks found: {track_count}\n")
      return track_count
    

  except Exception:
    logger.error(f"❌ Failed to retrieve number of Deezer tracks. Is there any track available ?", exc_info=True)
    close_driver(driver)


# Extracts the name from the Deezer webpage
def deezer_extract_name(driver):
  logger.info("🚀 Extracting Deezer name...")

  try:
    container_element = driver.find_element(By.CSS_SELECTOR, DEEZER_INFORMATIONS_SELECTOR)
    name = container_element.find_element(By.CSS_SELECTOR, DEEZER_TITLE_SELECTOR).text

    if name:
      logger.info(f"✅ Deezer name: {name}\n")
      return name

  except Exception:
    logger.error("❌ Failed to extract Deezer name", exc_info=True)
