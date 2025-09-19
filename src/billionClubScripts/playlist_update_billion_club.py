from src.utils.logger import logger 
from src.scraper.spotify.spotify_update_tracks_data import spotify_update_tracks_data


def playlist_update_billion_club():
  logger.info("#######################################")
  logger.info("###       UPDATE SPOTIFY DATA       ###")
  logger.info("#######################################\n")
  spotify_update_tracks_data(kill_script = True)

playlist_update_billion_club()