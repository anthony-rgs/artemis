import sys
from src.utils.logger import logger 
from src.scraper.spotify.spotify_get_albums import spotify_get_albums

def albums_update_billion_club():
  # Scrape Billion club albums data
  logger.info("#######################################")
  logger.info("###           GET ALBUMS           ###")
  logger.info("#######################################\n")
  spotify_get_albums()

  logger.info('✨ Billion club album scraped\n')

  # Kill script
  sys.exit(0)

albums_update_billion_club()