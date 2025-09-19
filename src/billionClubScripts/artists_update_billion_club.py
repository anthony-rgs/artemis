from src.utils.logger import logger 
from src.scraper.spotify.spotify_update_artists_data import spotify_update_artists_data

def artists_update_billion_club():
  logger.info("#######################################")
  logger.info("###       UPDATE ARTISTS DATA       ###")
  logger.info("#######################################\n")
  spotify_update_artists_data(kill_script= True)


artists_update_billion_club()