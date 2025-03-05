from src.config import SPOTIFY_TITLE_SELECTOR, SPOTIFY_ROW_COUNT_ATTR
from src.utils.logger import logger 
from src.scraper.driver import close_driver

# Retrieve the total number of tracks in a Spotify page
def spotify_count_tracks(driver):
  logger.info("🚀 Retrieving number of musics...")

  try:
    row_count_element = driver.find_element("css selector", f"[{SPOTIFY_ROW_COUNT_ATTR}]")
    row_count = int(row_count_element.get_attribute(SPOTIFY_ROW_COUNT_ATTR)) - 1

    if row_count:
      logger.info(f"✅ Spotify tracks found: {row_count}\n")
      return row_count

  except Exception:
    logger.error(f"❌ Failed to retrieve number of Spotify musics. Is there any music available ?", exc_info=True)
    close_driver(driver)


# Extracts the name from the Spotify webpage
def spotify_extract_name(driver):
  logger.info("🚀 Extracting Spotify name...")

  try:
    name = driver.find_element("css selector", SPOTIFY_TITLE_SELECTOR).text

    if name:
      logger.info(f"✅ Spotify name: {name}\n")
      return name

  except Exception:
    logger.error("❌ Failed to extract Spotify name", exc_info=True)
