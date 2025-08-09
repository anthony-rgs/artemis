from src.utils.logger import logger

# Create a Spotify embed from a Spotify URL
def create_spotify_embed(url):
  logger.info("🚀 Creating Spotify embed URL...")

  try: 
    # .rstrip('/') removes trailing slashes to avoid empty split elements
    url_splited = url.rstrip('/').split('/')
    url_type, url_id = url_splited[-2], url_splited[-1]
    embed = f"https://open.spotify.com/embed/{url_type}/{url_id}?theme=0"  # Theme = 0 -> dark mode
    
    logger.info("✅ Spotify embed created\n")
    return embed
  
  except Exception:
    logger.error("❌ Failed to create Spotify embed\n")
    return None


# Create a Spotify iframe from a Spotify embed URL
def create_spotify_iframe(embed_url):
  logger.info(f"🚀 Creating Spotify iframe...")

  try: 
    iframe = f"<iframe style='border-radius:12px' src='{embed_url}' width='100%' height='110' frameBorder='0' allowfullscreen='' allow='autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture' loading='lazy'></iframe>"
    
    logger.info("✅ Spotify iframe created\n")
    return iframe
  
  except Exception:
    logger.error("❌ Failed to create Spotify iframe\n")
    return None