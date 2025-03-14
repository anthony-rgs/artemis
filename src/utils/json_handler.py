import json
import time
from src.config import COLLECTIONS_FOLDER
from src.utils.logger import logger

# Create a JSON file with collection data
def create_json(tracks, link, name, platform, content_type):
  logger.info(f"🚀 Creating JSON file...")

  length = len(tracks)
  timestamp = int(time.time())

  tracks = [
    {
      "track_name": track_name, 
      "artists": artists, 
      "album": album, 
      "album_link": album_link, 
      "track_link": track_link,
    } 
    for album, album_link, artists, track_name, track_link in tracks
  ]

  data = {
    "type": content_type,
    "name": name,
    "length": length,
    "link": link,
    "tracks": tracks
  }

  folder = f"{COLLECTIONS_FOLDER}/{platform}"

  file_path = f"{folder}/{content_type}_{timestamp}_{name}.json"

  try:
    # Json file creation
    with open(file_path, "w", encoding="utf-8") as file:
      json.dump(data, file, indent=2, ensure_ascii=False)
      
    logger.info(f"✅ JSON file created: {file_path}\n")
    return file_path

  except Exception as e:
    logger.error(f"❌ Error creating JSON file: {e}", exc_info=True)