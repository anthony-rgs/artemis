import os
import time
import json

from src.config import COLLECTIONS_SPOTIFY_BILLION_CLUB_TRACKS_FOLDER, COLLECTIONS_SPOTIFY_BILLION_CLUB_ARTISTS_FOLDER

from src.utils.json_handler import get_latest_json_file, load_json_from_file

from src.utils.logger import logger

# Get artists from tracks file
def spotify_get_artists():
  logger.info("🚀 Creating artists JSON file...")

  # Start script timer
  start_updating_tracks = time.perf_counter()

  # Get last JSON file path
  folder = f"{COLLECTIONS_SPOTIFY_BILLION_CLUB_TRACKS_FOLDER}/"
  json_file_path = get_latest_json_file(folder)
  
  json_file = load_json_from_file(json_file_path)

  tracks = json_file.get("tracks", [])

  artists_dict = {}
  artist_id = 1

  for track in tracks:
    track_name = track["track_name"]
    play_count = track["play_count"]
    track_iframe = track["track_iframe"]

    album_name = track["album"]
    album_link = track["album_link"]
    album_img = track["track_img"]

    for idx, artist_name in enumerate(track.get("artists", [])):
      artist_link = track.get("artists_links", [None]*len(track["artists"]))[idx]

      # If the artist does not exist -> add it
      if artist_name not in artists_dict:
        artists_dict[artist_name] = {
          "artist_id": artist_id,
          "artist_name": artist_name,
          "artist_link": artist_link,
          "albums": [],
          "tracks": []
        }
        artist_id += 1

      artist_entry = artists_dict[artist_name]

      # Add album if does not exist
      album_entry = {
        "album_name": album_name,
        "album_link": album_link,
        "album_img": album_img
      }
      if album_entry not in artist_entry["albums"]:
        artist_entry["albums"].append(album_entry)

      # Add track if does not exist
      track_entry = {
        "track_name": track_name,
        "track_play_count": play_count,
        "track_iframe": track_iframe
      }
      if track_entry not in artist_entry["tracks"]:
        artist_entry["tracks"].append(track_entry)


  artists = list(artists_dict.values())

  file_name = f"artists_{int(time.time())}.json"
  file_path = os.path.join(COLLECTIONS_SPOTIFY_BILLION_CLUB_ARTISTS_FOLDER, file_name)

  try:
    # Json file creation
    with open(file_path, "w", encoding="utf-8") as file:
      json.dump(artists, file, indent=2, ensure_ascii=False)
      
    logger.info(f"✅ Artists JSON file created: {file_path}\n")
    return file_path

  except Exception as e:
    logger.error(f"❌ Error creating artists JSON file: {e}", exc_info=True)


  # End timer
  end_updating_tracks = time.perf_counter()
  updating_elapsed = end_updating_tracks - start_updating_tracks
  logger.info(f'⏰ Artists JSON file created in {updating_elapsed:.2f} seconds\n')

  logger.info("✅ Artists JSON created")
