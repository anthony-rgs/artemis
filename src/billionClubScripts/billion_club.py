import time
import sys

from src.config import SPOTIFY_BILLION_CLUB_URL

from src.utils.logger import logger 

from src.scraper.collection_handler import scrape_collection
from src.scraper.spotify.spotify_get_artists import spotify_get_artists
from src.scraper.spotify.spotify_get_albums import spotify_get_albums
from src.scraper.spotify.spotify_update_artists_data import spotify_update_artists_data
from src.scraper.spotify.spotify_update_tracks_data import spotify_update_tracks_data

# Billion club script
def billion_club():
  # Start timer
  start_billion_club_script = time.perf_counter()

  # Variables
  url = SPOTIFY_BILLION_CLUB_URL
  collection_json = False

  logger.info("💎 Billion club script running...\n")

  # Scrape Billion club playlist
  logger.info("#######################################")
  logger.info("###        SCRAPE COLLECTION        ###")
  logger.info("#######################################\n")
  tracks, collection_json = scrape_collection(url, kill_script = False)

  # Update Billion club playlist data
  logger.info("#######################################")
  logger.info("###       UPDATE SPOTIFY DATA       ###")
  logger.info("#######################################\n")
  spotify_update_tracks_data(collection_json, kill_script = False)

  # Scrape Billion club artists
  logger.info("#######################################")
  logger.info("###       SCRAPE ARTISTS DATA       ###")
  logger.info("#######################################\n")
  spotify_get_artists()

  # Update Billion club artists data
  logger.info("#######################################")
  logger.info("###       UPDATE ARTISTS DATA       ###")
  logger.info("#######################################\n")
  spotify_update_artists_data(kill_script = False)
  
  # Scrape Billion club albums data
  logger.info("#######################################")
  logger.info("###           GET ALBUMS           ###")
  logger.info("#######################################\n")
  spotify_get_albums()


  # End Timer
  end_billion_club_script = time.perf_counter()
  billion_club_elapsed = end_billion_club_script - start_billion_club_script
  logger.info(f'⏰ Billion club script completed in {billion_club_elapsed:.2f} seconds\n')

  # Kill script
  sys.exit(0)


billion_club()