from src.config import APPLE_TRACK_COUNT_ALBUM_INDEX, APPLE_TRACK_COUNT_PLAYLIST_INDEX, APPLE_TRACK_COUNT_SELECTOR, APPLE_TITLE_SELECTOR
from src.utils.logger import logger 
from src.scraper.playwright import close_playwright


# Retrieve the total number of tracks in a Apple page
def apple_count_tracks(page, content_type):
  logger.info("🚀 Retrieving number of tracks...")

  track_index = APPLE_TRACK_COUNT_PLAYLIST_INDEX if content_type == "playlist" else APPLE_TRACK_COUNT_ALBUM_INDEX

  try: 
    page.wait_for_selector(APPLE_TRACK_COUNT_SELECTOR, timeout=10_000)

    container_element = page.query_selector(APPLE_TRACK_COUNT_SELECTOR)
    track_count = int(container_element.text_content().split()[track_index])
    
    if track_count:
      logger.info(f"✅ Apple tracks found: {track_count}\n")
      return track_count
    
  except Exception:
    logger.error(f"❌ Failed to retrieve number of Apple tracks. Is there any track available ?", exc_info=True)
    close_playwright(page)


# Extracts the name from the Apple webpage
def apple_extract_name(page):
  logger.info("🚀 Extracting Apple name...")

  try:
    container_element = page.query_selector(APPLE_TITLE_SELECTOR)
    name = container_element.text_content()

    if name:
      logger.info(f"✅ Apple name: {name}\n")
      return name

  except Exception:
    logger.error("❌ Failed to extract Apple name", exc_info=True)
