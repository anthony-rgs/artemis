import time
import sys

from src.config import SPOTIFY_BILLION_CLUB_URL

from src.utils.logger import logger 

from src.scraper.collection_handler import scrape_collection
from src.scraper.spotify.spotify_update_tracks_data import spotify_update_tracks_data


# Billion club script
def billion_club():
  # Start timer
  start_billion_club_script = time.perf_counter()

  # If "y" -> run both scripts; else -> update last billion club JSON file data
  create_new_json = input("Create a new JSON ? (y) ").strip().lower()
  print("")

  # Variables
  url = SPOTIFY_BILLION_CLUB_URL
  collection_json = False

  logger.info("💎 Billion club script running...\n")

  # Scrape Billion club playlist
  if create_new_json == "y":
    logger.info("#######################################")
    logger.info("###        SCRAPE COLLECTION        ###")
    logger.info("#######################################\n")
    tracks, collection_json = scrape_collection(url, kill_script = False)

  # Update Billion club playlist data
  logger.info("#######################################")
  logger.info("###       UPDATE SPOTIFY DATA       ###")
  logger.info("#######################################\n")
  spotify_update_tracks_data(collection_json)

  # End Timer
  end_billion_club_script = time.perf_counter()
  billion_club_elapsed = end_billion_club_script - start_billion_club_script
  logger.info(f'⏰ Billion club script completed in {billion_club_elapsed:.2f} seconds\n')

  # Kill script
  sys.exit(1)


billion_club()