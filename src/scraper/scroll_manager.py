import time
from src.config import CUSTOM_OVERLAY_ID, MAX_RETRIES, RETRY_WAIT_TIME, SCROLL_ITERATIONS
from src.utils.logger import logger
from src.utils.validator import check_scraped_data
from src.scraper.playwright import close_playwright

# Scrolls to the top of the page
def scroll_to_top(container):
  container.press("Home")


# Scrolls down the page
def scroll_page(container):
  for _ in range(SCROLL_ITERATIONS):  # 1 scroll iteration corresponds to one visible line on the page
    container.press("ArrowDown")


# Get the current position of the custom div relative to the container and the global scroll offset
def get_scroll_position(page, container):
  try:
    custom_div = page.query_selector(f"#{CUSTOM_OVERLAY_ID}")
    scroll_position = page.evaluate("""
      ({customDiv, container}) => {
        const rect = customDiv.getBoundingClientRect();
        const containerRect = container.getBoundingClientRect();
        return rect.top + window.scrollY - containerRect.top + container.scrollTop;
      }
      """,
      {"customDiv": custom_div, "container": container}
    )

    return scroll_position
  
  except Exception as e:
    logger.error(f"❌ Failed to retrieve scroll position: {e}", exc_info=True)
    return None


# Scrolls through the track list and extracts all tracks
def load_all_tracks(page, total_tracks, container, extract_tracks):
  last_scroll = 0
  progress = 0
  tracks = []

  logger.info("🚀 Starting scrolling...")

  while True:    
    # Track scrolling progress
    percent_completion = round(100 * len(tracks) / total_tracks, 1)
    if percent_completion != progress:
      logger.info(f"📊 Progress: {percent_completion}%")
      progress = percent_completion

    # Simulate a scroll action
    scroll_page(container)
    
    # Check if scrolling is still progressing
    new_scroll = get_scroll_position(page, container)

    if new_scroll is None or percent_completion >= 100  or new_scroll == last_scroll:
      logger.info("✅ Scrolling completed\n")
      break

    # Extract tracks safely
    try:
      extract_tracks(page, tracks, total_tracks)
    except Exception as e:
      logger.error(f"❌ Error during track extraction: {e}", exc_info=True)

    last_scroll = new_scroll

  return tracks


# Attempts to extract a list of tracks from a webpage by scrolling and checking the data
def retry_and_check_tracks(page, total_tracks, scroll_container, extract_tracks):
  retry_attempts = 0
  data_checked = False
  
  while retry_attempts < MAX_RETRIES and not data_checked:
    try:
      if retry_attempts != 0:
        logger.info(f"🔄 Attempt {retry_attempts + 1} to fetch tracks\n")

      tracks = load_all_tracks(page, total_tracks, scroll_container, extract_tracks)
      
      # Check the extracted data
      data_checked = check_scraped_data(tracks, total_tracks)

      if data_checked:
        return tracks

      # If data is incorrect, scroll back to the top of the page
      scroll_to_top(scroll_container)
      time.sleep(RETRY_WAIT_TIME)

    except Exception as e:
      logger.error(f"❌ Error during track extraction attempt {retry_attempts + 1}: {e}", exc_info=True)

    retry_attempts += 1
    
  if not data_checked:
    logger.error(f"💀 Tracks scraping failed after multiple retries, aborting... \n")
    close_playwright(page)