from src.utils.logger import logger 
from src.scraper.driver import close_driver
from src.config import DEEZER_INFORMATIONS_SELECTOR, DEEZER_TOTAL_TRACKS_XPATH, DEEZER_TITLE_SELECTOR

# Retrieve the total number of tracks in a Deezer page
def deezer_count_tracks(driver, _):
  logger.info("🚀 Retrieving number of musics...")

  try: 
    container_element = driver.find_element("css selector", DEEZER_INFORMATIONS_SELECTOR)
    track_count_item = container_element.find_element("xpath", DEEZER_TOTAL_TRACKS_XPATH)
    track_count = int(track_count_item.text.split()[0])

    if track_count:
      logger.info(f"✅ Deezer tracks found: {track_count}\n")
      return track_count
    

  except Exception:
    logger.error(f"❌ Failed to retrieve number of Deezer musics. Is there any music available ?", exc_info=True)
    close_driver(driver)


# Extracts the name from the Deezer webpage
def deezer_extract_name(driver):
  logger.info("🚀 Extracting Deezer name...")

  try:
    container_element = driver.find_element("css selector", DEEZER_INFORMATIONS_SELECTOR)
    name = container_element.find_element("css selector", DEEZER_TITLE_SELECTOR).text

    if name:
      logger.info(f"✅ Deezer name: {name}\n")
      return name

  except Exception:
    logger.error("❌ Failed to extract Deezer name", exc_info=True)
