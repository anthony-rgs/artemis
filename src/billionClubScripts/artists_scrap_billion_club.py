import sys
from src.utils.logger import logger 
from src.scraper.spotify.spotify_get_artists import spotify_get_artists


def artists_scrap_billion_club():
  logger.info("#######################################")
  logger.info("###       SCRAP ARTISTS DATA       ###")
  logger.info("#######################################\n")
  spotify_get_artists()

  logger.info('✨ Billion club artists scraped\n')

  # Kill script
  sys.exit(0)
  
artists_scrap_billion_club()