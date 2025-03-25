import time

from src.config import URL_APPLE_PLAYLIST, URL_APPLE_ALBUM, URL_APPLE_ALBUM_DISCS, URL_DEEZER_PLAYLIST, URL_DEEZER_ALBUM, URL_DEEZER_ALBUM_DISCS, URL_SPOTIFY_PLAYLIST, URL_SPOTIFY_ALBUM, URL_SPOTIFY_ALBUM_DISCS
from src.utils.logger import logger
from src.scraper.collection_handler import scrape_collection


# Urls
urls = [
  {
    "plateform": "Apple",
    "collection": "playlist",
    "url": URL_APPLE_PLAYLIST
  },
  {
    "plateform": "Apple",
    "collection": "album",
    "url": URL_APPLE_ALBUM
  },
  {
    "plateform": "Apple",
    "collection": "album (discs)",
    "url": URL_APPLE_ALBUM_DISCS
  },
  {
    "plateform": "Deezer",
    "collection": "playlist",
    "url": URL_DEEZER_PLAYLIST
  },
  {
    "plateform": "Deezer",
    "collection": "album",
    "url": URL_DEEZER_ALBUM
  },
  {
    "plateform": "Deezer",
    "collection": "album (discs)",
    "url": URL_DEEZER_ALBUM_DISCS
  },
  {
    "plateform": "Spotify",
    "collection": "playlist",
    "url": URL_SPOTIFY_PLAYLIST
  },
  {
    "plateform": "Spotify",
    "collection": "album",
    "url": URL_SPOTIFY_ALBUM
  },
  {
    "plateform": "Spotify",
    "collection": "album (discs)",
    "url": URL_SPOTIFY_ALBUM_DISCS
  }
]


# Check urls script
def check_urls():
  urls_checked = []
  
  # Start timer
  start_check_urls_script = time.perf_counter()

  logger.info("🔄 Check urls script running...\n")
 
  # Check urls
  for url in urls:
    logger.info("####################################\n")
    logger.info(f"🧑‍💻 {url['plateform']} {url['collection']} 🧑‍💻\n")
    
    url_checked = "✅" if scrape_collection(url["url"], json_save=False, kill_script=False) else "❌"
    urls_checked.append(f"{url_checked} {url['plateform']} - {url['collection']}")


  # End Timer
  end_check_urls_script = time.perf_counter()
  check_urls_elapsed = end_check_urls_script - start_check_urls_script
  logger.info(f'⏰ Check urls script completed in {check_urls_elapsed:.2f} seconds\n')
 
  # Log check urls results
  logger.info(f'✨ Check urls results')
  for url_checked in urls_checked:
    logger.info(url_checked)


check_urls()