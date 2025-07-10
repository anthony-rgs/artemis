from src.config import SPOTIFY_SCROLL_CONTAINER
from src.utils.logger import logger 


# Retrieves the Spotify scroll container that holds the track list
def get_spotify_scroll_container(page):
  logger.info("🚀 Starting retrieval of scroll container...")

  try:
    page.wait_for_selector(SPOTIFY_SCROLL_CONTAINER, timeout=10000, state="attached")

    # Récupérer la liste des éléments correspondant au sélecteur CSS
    containers = page.query_selector_all(SPOTIFY_SCROLL_CONTAINER)
    
    if len(containers) < 2:
      logger.error("❌ Scroll container not found or incomplete")
      return None

    logger.info("✅ Scroll container retrieved\n")
    return containers[2]  # The third container holds the track list

  except Exception as e:
    logger.error(f"❌ Error retrieving the scroll container: {e}", exc_info=True)
    return None
