import requests
from src.utils.logger import logger 

# Check if the collection URL is valid and identifies the platform and type (album/playlist)
def check_link(url):
  logger.info("🚀 Verifying the link...")

  # Check if the URL is reachable (status code 200)
  try:
    response = requests.get(url)
    # To many request can block, so we have to allow 200 and 429
    if response.status_code != 200 and response.status_code != 429:
      logger.error("❌ The site did not respond with a 200 status code\n")
      return False 
    
    if response.status_code == 429:
      logger.info("😬 The site respond with a 429 status code. Too many requests oups..\n")
  
  except requests.exceptions.RequestException:
    logger.error("❌ Error checking the link, please ensure the link is correct\n")
    return False
  
  # Determine the platform (spotify/deezer)
  if "spotify.com" in url:
    platform = "spotify"
  elif "deezer.com" in url:
    platform = "deezer"
  else:
    platform = None 
    logger.error("❌ Error determining platform, only Spotify and Deezer are allowed")

  # Determine the type (playlist/album)
  if "/playlist/" in url:
    content_type = "playlist"
  elif "/album/" in url:
    content_type = "album"
  else:
    content_type = None
    logger.error("❌ Error determining content type, only playlists and albums can be scraped")
  
  # Logs
  if platform and content_type: 
    logger.info(f"✅ The link is valid: {platform} & {content_type}\n")
  else: 
    logger.error("❌ The link is not correct, unable to proceed\n")
    return False

  return platform, content_type
