from src.config import APPLE_SCROLL_CONTAINER, APPLE_TRACKS_CONTAINER
from src.utils.logger import logger 


# Retrieves the Apple scroll container that holds the track list
def get_apple_scroll_container(page):
  logger.info("🚀 Starting retrieval of scroll container...")

  try:
    page.wait_for_selector(APPLE_SCROLL_CONTAINER, timeout=10_000)
    page.wait_for_selector(APPLE_TRACKS_CONTAINER, timeout=10_000)

    container = page.query_selector(APPLE_SCROLL_CONTAINER)
      
    logger.info("✅ Scroll container retrieved\n")
    return container

  except Exception as e:
    logger.error(f"❌ Error retrieving the scroll container: {e}", exc_info=True)
    return None
