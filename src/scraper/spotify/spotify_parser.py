import re

from src.config import SPOTIFY_TITLE_SELECTOR, SPOTIFY_PLAYLIST_IMAGE_ARTIST_TEXT, SPOTIFY_PLAYLIST_IMAGE_SELECTOR, SPOTIFY_RELEASE_DATE_SELECTOR, SPOTIFY_ALBUM_TOTAL_TRACKS_XPATH, SPOTIFY_PLAYLIST_TOTAL_TRACKS_ATTR, SPOTIFY_PLAY_COUNT_SELECTOR, SPOTIFY_TRACK_IMAGE_XPATH

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
  

# Get spotify extrack playlist cover
def spotify_extrack_playlist_cover(page):
  logger.info("🚀 Extracting playlist cover...")
    
  try:
    # Get image src
    page.wait_for_selector(SPOTIFY_PLAYLIST_IMAGE_SELECTOR, timeout=5000)
    img_element = page.query_selector(f"{SPOTIFY_PLAYLIST_IMAGE_SELECTOR} img")
    
    if img_element:
      img_url = img_element.evaluate('node => node.getAttribute("src")')
    else:
      logger.error("❌ Playlist cover image not found")
      return None 

    # Get artist name 
    artist_name = ""
    try:
      artist_element = page.locator(f"text={SPOTIFY_PLAYLIST_IMAGE_ARTIST_TEXT}")
      artist_element_text = artist_element.inner_text()

      if artist_element_text: 
        artist_name = artist_element_text.replace(SPOTIFY_PLAYLIST_IMAGE_ARTIST_TEXT, "").strip()

    except Exception as e:
      logger.error(f"❌ Failed to extract artist name: {e}")
      artist_name = ""

    logger.info(f"✅ Playlist cover extracted: {artist_name}\n")    
    return img_url, artist_name

  except Exception as e:
    logger.error(f"❌ Failed to extract playlist cover: {e}")
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
  

# Scrap artist data
def spotify_scrap_artist_data(page, artist_link, artist_name):
  try:
    # Open track page
    page.goto(artist_link)

    artist_img_url = ""
    escaped_artist_name = artist_name.replace("\\", "\\\\").replace('"', '\\"') # Fuck u Axwell /\

    # Artist with description section
    try:
      selector = f'button[aria-label="{escaped_artist_name}"]'
      artist_img_btn = page.wait_for_selector(selector, timeout=10000)
      artist_bg_img = artist_img_btn.evaluate("el => getComputedStyle(el).backgroundImage")
      artist_img_url =  re.search(r'url\(["\']?(.*?)["\']?\)', artist_bg_img)
      if artist_img_url and artist_img_url.group(1):
        artist_img_url =  artist_img_url.group(1)
    except TimeoutError:
      pass

    # Artist without description section
    if not artist_img_url:
      try:
        selector = f'figure[title="{escaped_artist_name}"] img'
        wait_for_artist_img = page.wait_for_selector(selector, timeout=10000)
        if wait_for_artist_img: 
          artist_imgs = page.query_selector_all(selector)
          artist_img_url = artist_imgs[-1].get_attribute("src")
      except TimeoutError:
        pass
        
    # Get artist monthly listeners
    artist_listeners_span = page.wait_for_selector('span:has-text("monthly listeners")')
    artist_listeners_text = artist_listeners_span.inner_text()
    artist_monthly_listeners_string = artist_listeners_text.replace("monthly listeners", "").strip()
    artist_monthly_linsteners = int(artist_monthly_listeners_string.replace(",", ""))
    
    # New artist data
    new_artist_data = {
      'artist_img': artist_img_url,
      'track_listeners': artist_monthly_linsteners
    }

    logger.info("✅ Artist data updated\n")

    return new_artist_data

  except Exception:
    logger.error(f"❌ Failed to update Artist track data\n", exc_info=True)
    return None