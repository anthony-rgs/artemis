import json
import time
from src.config import COLLECTIONS_FOLDER
from src.utils.logger import logger

# Create a JSON file with collection data
def create_json(tracks, link, name):
  logger.info(f"🚀 Creating JSON file...")

  length = len(tracks)
  timestamp = int(time.time())

  musics = [
    {
      "music_name": music_name, 
      "artists": artists, 
      "album": album, 
      "music_link": music_link,
      "album_link": album_link, 
    } 
    for album, album_link, artists, music_name, music_link in tracks
  ]

  data = {
    "name": name,
    "length": length,
    "link": link,
    "musics": musics
  }

  file_path = f"{COLLECTIONS_FOLDER}{name}_{timestamp}.json"

  try:
    # Json file creation
    with open(file_path, "w", encoding="utf-8") as file:
      json.dump(data, file, indent=2, ensure_ascii=False)
      
    logger.info(f"✅ JSON file created: {file_path}\n")

  except Exception as e:
    logger.error(f"❌ Error creating JSON file: {e}", exc_info=True)