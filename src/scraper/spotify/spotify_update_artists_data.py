import time
from src.config import COLLECTIONS_SPOTIFY_BILLION_CLUB_ARTISTS_FOLDER

from src.utils.retry import retry_function
from src.utils.logger import logger 
from src.utils.json_handler import get_latest_json_file, load_json_from_file, update_json_file

from src.scraper.playwright import launch_playwright, close_playwright, create_context_and_page, close_context_and_page
from src.scraper.spotify.spotify_parser import spotify_scrap_artist_data


def spotify_update_artists_data(kill_script = True):
  # Start script timer
  start_updating_tracks = time.perf_counter()

  # Get last JSON file path
  folder = f"{COLLECTIONS_SPOTIFY_BILLION_CLUB_ARTISTS_FOLDER}/"
  json_file_path = get_latest_json_file(folder)

  # Init playwright
  page, browser, playwright = retry_function(launch_playwright)

  if page: 
    logger.info("🚀 Fetching new artists data...")

    while True:
      logger.disabled = True  # Disable logger

      # Load JSON file and return it as a Python dictionary
      json_file = load_json_from_file(json_file_path)
      logger.disabled = False  # Enable logger

      # Checks 
      artists_with_image = [artist for artist in json_file if artist.get("artist_img")]
      artists_without_image = [artist for artist in json_file if not artist.get("artist_img")]
      other_artists = artists_without_image[1:]
      logger.info(f"📊 Artists updated : {len(artists_with_image)}/{len(json_file)}")

      if not artists_without_image:
        logger.info("✅ New artists data fetched\n")
        break

      try:
        logger.disabled = True  # Disable logger
        artist = artists_without_image[0] # Select the first artist
        artist_link = artist["artist_link"]
        artist_name = artist["artist_name"]

        # Create new context and page
        context, page = create_context_and_page(browser)
        
        # Scrap more Spotify artist data
        artist_updated = spotify_scrap_artist_data(page, artist_link, artist_name)  


        # Close context and page
        close_context_and_page(context, page)
        
        # Merge artist data and new artist data
        new_artist_data = {**artist, **artist_updated}


        # Update the JSON one entry at a time. It's not the most optimized approach, but it's the safest
        # Updating in batches (e.g., 10 by 10) risks failing mid-way, potentially requiring a restart and losing already retrieved data
        json_file = artists_with_image + [new_artist_data] + other_artists
        update_json_file(json_file_path, json_file)  # Update the JSON file
        
        logger.disabled = False  # Enable logger

      except Exception as e:
        logger.error(f"❌ Error during artist extraction attempt : {e}", exc_info=True)

    # End timer
    end_updating_tracks = time.perf_counter()
    updating_elapsed = end_updating_tracks - start_updating_tracks
    logger.info(f'⏰ Artists data updating completed in {updating_elapsed:.2f} seconds\n')

    logger.info(f"🎉 You rock, Artémis !\n")

    close_playwright(page, browser, playwright, kill_script)