import sys
from src.utils.logger import logger 
from src.scraper.collection_handler import scrape_collection
from src.config import SPOTIFY_BILLION_CLUB_URL


def playlist_scrap_billion_club():
  url = SPOTIFY_BILLION_CLUB_URL

  logger.info("#######################################")
  logger.info("###        SCRAPE COLLECTION        ###")
  logger.info("#######################################\n")
  tracks, collection_json = scrape_collection(url, kill_script = False)

  logger.info('✨ Billion club playlist scraped\n')

  # Kill script
  sys.exit(0)

playlist_scrap_billion_club()