from src.config import SPOTIFY_TITLE_SELECTOR, SPOTIFY_RELEASE_DATE_SELECTOR, SPOTIFY_ALBUM_TOTAL_TRACKS_XPATH, SPOTIFY_PLAYLIST_TOTAL_TRACKS_ATTR, SPOTIFY_PLAY_COUNT_SELECTOR, SPOTIFY_TRACK_IMAGE_XPATH

from src.utils.logger import logger 
from src.utils.spotify import create_spotify_embed, create_spotify_iframe

from src.scraper.playwright import close_playwright


# Retrieve the total number of tracks in a Spotify page
def spotify_count_tracks(page, content_type):
  logger.info("🚀 Retrieving number of tracks...")

  try: 
    if content_type == "album":
      # Find_element -> take the first element
      row_count_element = page.locator(SPOTIFY_ALBUM_TOTAL_TRACKS_XPATH).first.text_content()
      row_count = int(row_count_element.split()[0]) if row_count_element else 0


    elif content_type == "playlist":
      page.wait_for_function(
        f'document.querySelectorAll("[{SPOTIFY_PLAYLIST_TOTAL_TRACKS_ATTR}]").length >= 2',
        timeout=10_000
      )

      row_count_elements = page.query_selector_all(f"[{SPOTIFY_PLAYLIST_TOTAL_TRACKS_ATTR}]")
      row_count_element = row_count_elements[1]  # 1 -> second element
      row_count = int(row_count_element.get_attribute(SPOTIFY_PLAYLIST_TOTAL_TRACKS_ATTR)) - 1

    if row_count:
      logger.info(f"✅ Spotify tracks found: {row_count}\n")
      return row_count

  except Exception:
    logger.error(f"❌ Failed to retrieve number of Spotify tracks. Is there any track available ?", exc_info=True)
    close_playwright(page)


# Extracts the name from the Spotify webpage
def spotify_extract_name(page):
  logger.info("🚀 Extracting Spotify name...")

  try:
    name = page.query_selector(SPOTIFY_TITLE_SELECTOR).inner_text()

    if name:
      logger.info(f"✅ Spotify name: {name}\n")
      return name

  except Exception:
    logger.error("❌ Failed to extract Spotify name", exc_info=True)


# Get spotify play count from a Spotify music page
def spotify_extract_play_count(page):
  logger.info("🚀 Extracting Spotify track play count...")
  
  try:
    page.wait_for_selector(SPOTIFY_PLAY_COUNT_SELECTOR, timeout=5000)

    track_play_count = page.query_selector(SPOTIFY_PLAY_COUNT_SELECTOR).inner_text()
    track_play_count_formatted = int(track_play_count.replace(",", ""))

    if track_play_count_formatted:
      logger.info(f"✅ Track play count extracted: {track_play_count_formatted}\n")
      
      return track_play_count_formatted

  except Exception:
    logger.error("❌ Failed to extract Spotify track play count\n")
    return None

# Get spotify release date from a Spotify music page
def spotify_extract_release_date(page):
  logger.info("🚀 Extracting release date...")
  
  try:
    page.wait_for_selector(SPOTIFY_RELEASE_DATE_SELECTOR, timeout=5000)

    release_date = page.query_selector(SPOTIFY_RELEASE_DATE_SELECTOR).inner_text()

    if release_date:
      logger.info(f"✅ Track release date extracted: {release_date}\n")
      
      return release_date

  except Exception:
    logger.error("❌ Failed to extract Spotify track release date\n")
    return None

# Update a Spotify track data
def spotify_scrap_more_track_data(page, track_link, album_link):
  try:
    # Track embed & iframe
    track_embed = create_spotify_embed(track_link)
    track_iframe = create_spotify_iframe(track_embed)
    
    # Album embed & iframe
    album_embed = create_spotify_embed(album_link)
    album_iframe = create_spotify_iframe(track_embed)

    # Open track page
    page.goto(track_link)

    # Get track count
    track_play_count = spotify_extract_play_count(page)

    # Get release date
    release_date = spotify_extract_release_date(page)
    
    # Get track image src
    track_img_src = page.query_selector(f'xpath={SPOTIFY_TRACK_IMAGE_XPATH}').get_attribute('src')

    # New track data
    new_track_data = {
      'play_count': track_play_count,
      'track_img': track_img_src,
      'track_embed': track_embed,
      'track_iframe': track_iframe,
      'album_embed': album_embed,
      'album_iframe': album_iframe,
      'track_year': release_date
    }
    
    logger.info("✅ Track data updated\n")

    return new_track_data

  except Exception:
    logger.error(f"❌ Failed to update Spotify track data\n", exc_info=True)
    return None