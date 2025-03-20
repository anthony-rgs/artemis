from selenium.webdriver.common.by import By

from src.config import SPOTIFY_TITLE_SELECTOR, SPOTIFY_ALBUM_TOTAL_TRACKS_XPATH, SPOTIFY_PLAYLIST_TOTAL_TRACKS_ATTR, SPOTIFY_PLAY_COUNT_SELECTOR, SPOTIFY_TRACK_IMAGE_XPATH

from src.utils.logger import logger 
from src.utils.spotify import create_spotify_embed, create_spotify_iframe

from src.scraper.driver import close_driver


# Retrieve the total number of tracks in a Spotify page
def spotify_count_tracks(driver, content_type):
  logger.info("🚀 Retrieving number of tracks...")

  try: 
    if content_type == "album":
      # Find_element -> take the first element
      row_count_element = driver.find_element(By.XPATH, SPOTIFY_ALBUM_TOTAL_TRACKS_XPATH).text
      row_count = int(row_count_element.split()[0])
    
    elif content_type == "playlist":
      row_count_element = driver.find_element(By.CSS_SELECTOR, f"[{SPOTIFY_PLAYLIST_TOTAL_TRACKS_ATTR}]")
      row_count = int(row_count_element.get_attribute(SPOTIFY_PLAYLIST_TOTAL_TRACKS_ATTR)) - 1

    if row_count:
      logger.info(f"✅ Spotify tracks found: {row_count}\n")
      return row_count

  except Exception:
    logger.error(f"❌ Failed to retrieve number of Spotify tracks. Is there any track available ?", exc_info=True)
    close_driver(driver)


# Extracts the name from the Spotify webpage
def spotify_extract_name(driver):
  logger.info("🚀 Extracting Spotify name...")

  try:
    name = driver.find_element(By.CSS_SELECTOR, SPOTIFY_TITLE_SELECTOR).text

    if name:
      logger.info(f"✅ Spotify name: {name}\n")
      return name

  except Exception:
    logger.error("❌ Failed to extract Spotify name", exc_info=True)


# Get spotify play count from a Spotify music page
def spotify_extract_play_count(driver):
  logger.info("🚀 Extracting Spotify track play count...")
  
  try:
    track_play_count = driver.find_element(By.CSS_SELECTOR, f"{SPOTIFY_PLAY_COUNT_SELECTOR}").text
    track_play_count_formatted = int(track_play_count.replace(",", ""))

    if track_play_count_formatted:
      logger.info(f"✅ Track play count extracted: {track_play_count_formatted}\n")
      
      return track_play_count_formatted

  except Exception:
    logger.error("❌ Failed to extract Spotify track play count\n")
    return None


# Update a Spotify track data
def spotify_scrap_more_track_data(driver, track_link, album_link):
  try:
    # Track embed & iframe
    track_embed = create_spotify_embed(track_link)
    track_iframe = create_spotify_iframe(track_embed)
    
    # Album embed & iframe
    album_embed = create_spotify_embed(album_link)
    album_iframe = create_spotify_iframe(track_embed)

    # Open track page
    driver.get(track_link)

    # Get track count
    track_play_count = spotify_extract_play_count(driver)

    # Get track image src
    track_img_src = driver.find_element(By.XPATH, SPOTIFY_TRACK_IMAGE_XPATH).get_attribute('src')

    # New track data
    new_track_data = {
      'play_count': track_play_count,
      'track_img': track_img_src,
      'track_embed': track_embed,
      'track_iframe': track_iframe,
      'album_embed': album_embed,
      'album_iframe': album_iframe
    }
    
    logger.info("✅ Track data updated\n")

    return new_track_data

  except Exception:
    logger.error(f"❌ Failed to update Spotify track data\n", exc_info=True)
    return None