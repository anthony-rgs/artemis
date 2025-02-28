import re
from src.utils.logger import logger 
from src.config import SPOTIFY_PLAYLIST_TITLE_SELECTOR, SPOTIFY_ROW_COUNT_ATTR

# Extracts the raw playlist name from the Spotify webpage
def extract_playlist_name(driver):
  logger.info("🚀 Extracting playlist name...")

  try:
    playlist_name = driver.find_element("css selector", SPOTIFY_PLAYLIST_TITLE_SELECTOR).text

    if playlist_name:
      logger.info(f"✅ Playlist name: {playlist_name}\n")
      return playlist_name

  except Exception:
    logger.error("❌ Failed to extract playlist name", exc_info=True)
  return None

# Formats a playlist name by removing emojis and replacing spaces with hyphens
def format_playlist_name(name):
  logger.info("🚀 Formating playlist name...")

  emoji_pattern = re.compile(
    "["
    "\U0001F600-\U0001F64F"  # Emoticons  
    "\U0001F300-\U0001F5FF"  # Symbols & pictograms  
    "\U0001F680-\U0001F6FF"  # Transport & map symbols  
    "\U0001F700-\U0001F77F"  # Alchemical symbols  
    "\U0001F780-\U0001F7FF"  # Miscellaneous symbols  
    "\U0001F800-\U0001F8FF"  # More miscellaneous symbols  
    "\U0001F900-\U0001F9FF"  # Supplemental emojis  
    "\U0001FA00-\U0001FA6F"  # Additional symbols  
    "\U0001FA70-\U0001FAFF"  # More additional symbols  
    "\U00002702-\U000027B0"  # Dingbats  
    "\U000024C2-\U0001F251"  # Enclosed characters  
    "]+", flags=re.UNICODE
  )
    
  name_clean = emoji_pattern.sub(r'', name).strip()
  name_formatted = name_clean.replace(" ", "-").lower()

  logger.info(f"✅ Formatted name: {name_formatted}\n")

  return name_formatted

# Retrieve the total number of tracks in a Spotify playlist
def count_playlist_tracks(driver):
  logger.info("🚀 Retrieving number of musics...")

  try:
    row_count_element = driver.find_element("css selector", f"[{SPOTIFY_ROW_COUNT_ATTR}]")
    row_count = int(row_count_element.get_attribute(SPOTIFY_ROW_COUNT_ATTR)) - 1

    logger.info(f"✅ Tracks found: {row_count}\n")
    return row_count

  except Exception as e:
    logger.error("❌ Failed to retrieve number of musics", exc_info=True)
    return None