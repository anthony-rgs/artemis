import time

from src.config import COLLECTIONS_SPOTIFY_BILLION_CLUB_FOLDER, MAX_RETRIES, RETRY_WAIT_TIME

from src.utils.retry import retry_function
from src.utils.logger import logger 
from src.utils.json_handler import get_latest_json_file, load_json_from_file, update_json_file, move_json_file

from src.scraper.playwright import launch_playwright, close_playwright
from src.scraper.spotify.spotify_parser import spotify_scrap_more_track_data


# Update Spotify tracks data from a JSON file
def spotify_update_tracks_data(collection_json):
  # Start script timer
  start_updating_tracks = time.perf_counter()

  # Move last JSON file
  if collection_json:
    file_source = collection_json
    file_destination = COLLECTIONS_SPOTIFY_BILLION_CLUB_FOLDER
    move_json_file(file_source, file_destination)

  # Get last JSON file path
  folder = f"{COLLECTIONS_SPOTIFY_BILLION_CLUB_FOLDER}/"
  json_file_path = get_latest_json_file(folder)

  # Init playwright
  page, browser, playwright = retry_function(launch_playwright)
  
  if page: 
    logger.info("🚀 Fetching new tracks data...")

    while True:
      logger.disabled = True  # Disable logger
      # Load JSON file and return it as a Python dictionary
      json_file = load_json_from_file(json_file_path)
      logger.disabled = False  # Enable logger

      # Checks 
      tracks_with_play_count = [track for track in json_file["tracks"] if "play_count" in track]
      tracks_without_play_count = [track for track in json_file["tracks"] if "play_count" not in track]
      other_tracks = tracks_without_play_count[1:]
      logger.info(f"📊 Tracks updated : {len(tracks_with_play_count)}/{len(json_file["tracks"])}")

      if not tracks_without_play_count:
        logger.info("✅ New tracks data fetched\n")
        break

      try:
        logger.disabled = True  # Disable logger
        track = tracks_without_play_count[0] # Select the first track
        
        # Scrap more Spotify track data
        track_link =  track["track_link"]
        album_link = track["album_link"]
        track_updated = spotify_scrap_more_track_data(page, track_link, album_link)    
        
        # Merge track data and new track data
        new_track_data = {**track, **track_updated}

        # Update the JSON one entry at a time. It's not the most optimized approach, but it's the safest
        # Updating in batches (e.g., 10 by 10) risks failing mid-way, potentially requiring a restart and losing already retrieved data
        json_file['tracks'] = tracks_with_play_count + [new_track_data] + other_tracks
        update_json_file(json_file_path, json_file)  # Update the JSON file
        
        logger.disabled = False  # Enable logger

      except Exception as e:
        logger.error(f"❌ Error during track extraction attempt : {e}", exc_info=True)

    # End timer
    end_updating_tracks = time.perf_counter()
    updating_elapsed = end_updating_tracks - start_updating_tracks
    logger.info(f'⏰ Tracks data updating completed in {updating_elapsed:.2f} seconds\n')

    logger.info(f"🎉 You rock, Artémis !\n")

    close_playwright(page, browser, playwright)