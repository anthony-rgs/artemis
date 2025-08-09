import glob
import json
import os
import time
import shutil

from src.config import COLLECTIONS_FOLDER

from src.utils.logger import logger


# Create a JSON file with collection data
def create_json_file(tracks, link, name, platform, content_type):
  logger.info("🚀 Creating JSON file...")

  length = len(tracks)
  timestamp = int(time.time())

  tracks = [
    {
      "track_name": track_name, 
      "artists": artists, 
      "artists_links": artists_links, 
      "album": album, 
      "album_link": album_link, 
      "track_link": track_link,
      "track_time": track_time
    } 
    for album, album_link, artists, artists_links, track_name, track_link,
      track_time in tracks
  ]

  data = {
    "type": content_type,
    "platform": platform,
    "name": name,
    "length": length,
    "link": link,
    "tracks": tracks,
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


# Get lastest json file
def get_latest_json_file(folder):
  logger.info("🚀 Getting the latest JSON file from the folder...")

  try: 
     # Find the most recently modified JSON file in the folder
    latest_file = max(glob.glob(f"{folder}*"), key=os.path.getmtime) 
    logger.info("✅ Latest JSON file retrieved\n")

    return latest_file
  
  except Exception:
    logger.error("❌ Error retrieving the latest JSON file\n")
    return None


# Reads and loads JSON data from a file
def load_json_from_file(json_path):
  logger.info("🚀 Opening JSON file...")

  try:
    with open(json_path, "r", encoding="utf-8") as f:
      json_data = json.load(f)  # file is now a dictionary
    
    logger.info("✅ JSON file opened\n")
    return json_data
  
  except Exception:
    logger.error("❌ Error opening JSON file\n")
    return None


# Update data from a Json file
def update_json_file(file_path, file_data):
  logger.info("🚀 Updating JSON file...")

  try:
    with open(file_path, 'w', encoding="utf-8") as file:
      json.dump(file_data, file, indent=2, ensure_ascii=False)
    
    logger.info("✅ JSON file updated\n")
  
  except Exception:
    logger.error("❌ Error updating JSON file\n")


# Move a JSON file from source path to destination path
def move_json_file(source, destination):
  logger.info("🚀 Moving JSON file...")

  try:
    shutil.move(source, destination)
    logger.info(f"✅ JSON file moved to: {destination}\n")
    return True
  
  except Exception:
    logger.error("❌ Error moving JSON file\n")
    return False
