from selenium.webdriver.common.by import By
from src.config import SPOTIFY_TITLE_SELECTOR, SPOTIFY_ALBUM_TOTAL_TRACKS_XPATH, SPOTIFY_PLAYLIST_TOTAL_TRACKS_ATTR
from src.utils.logger import logger 
from src.scraper.driver import close_driver

# Retrieve the total number of tracks in a Spotify page
def spotify_count_tracks(driver, content_type):
  logger.info("🚀 Retrieving number of musics...")

  try: 
    if content_type == "album":
      # Find_element -> take the first element
      row_count_element = driver.find_element(By.XPATH, SPOTIFY_ALBUM_TOTAL_TRACKS_XPATH).text
      row_count = int(row_count_element.split()[0])
    
    elif content_type == "playlist":
      row_count_element = driver.find_element("css selector", f"[{SPOTIFY_PLAYLIST_TOTAL_TRACKS_ATTR}]")
      row_count = int(row_count_element.get_attribute(SPOTIFY_PLAYLIST_TOTAL_TRACKS_ATTR)) - 1

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
