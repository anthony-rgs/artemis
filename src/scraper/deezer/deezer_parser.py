from src.config import DEEZER_INFORMATIONS_SELECTOR, DEEZER_TOTAL_TRACKS_XPATH, DEEZER_TITLE_SELECTOR
from src.utils.logger import logger 
from src.scraper.playwright import close_playwright

# Retrieve the total number of tracks in a Deezer page
def deezer_count_tracks(page, _):
  logger.info("🚀 Retrieving number of tracks...")

  try: 
    container_element = page.wait_for_selector(DEEZER_INFORMATIONS_SELECTOR, timeout=10000)
    track_count_item = container_element.query_selector(f"xpath={DEEZER_TOTAL_TRACKS_XPATH}")
    track_count = int(track_count_item.text_content().split()[0])

    if track_count:
      logger.info(f"✅ Deezer tracks found: {track_count}\n")
      return track_count
    
  except Exception:
    logger.error(f"❌ Failed to retrieve number of Deezer tracks. Is there any track available ?", exc_info=True)
    close_playwright(page)


# Extracts the name from the Deezer webpage
def deezer_extract_name(page):
  logger.info("🚀 Extracting Deezer name...")

  try:
    container_element = page.query_selector(DEEZER_INFORMATIONS_SELECTOR)
    name = container_element.query_selector(DEEZER_TITLE_SELECTOR).text_content()

    if name:
      logger.info(f"✅ Deezer name: {name}\n")
      return name

  except Exception:
    logger.error("❌ Failed to extract Deezer name", exc_info=True)
