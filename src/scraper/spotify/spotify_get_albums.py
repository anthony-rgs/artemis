import os
import time
import json

from src.config import COLLECTIONS_SPOTIFY_BILLION_CLUB_TRACKS_FOLDER, COLLECTIONS_SPOTIFY_BILLION_CLUB_ARTISTS_FOLDER, COLLECTIONS_SPOTIFY_BILLION_CLUB_ALBUMS_FOLDER

from src.utils.json_handler import get_latest_json_file, load_json_from_file

from src.utils.logger import logger


# Get artists from tracks file
def spotify_get_albums():
  logger.info("🚀 Creating artists JSON file...")

  # Start script timer
  start_updating_tracks = time.perf_counter()

  # Load json file
  tracks_folder = f"{COLLECTIONS_SPOTIFY_BILLION_CLUB_TRACKS_FOLDER}/"
  tracks_json_file_path = get_latest_json_file(tracks_folder)
  tracks_json_file = load_json_from_file(tracks_json_file_path)
  tracks = tracks_json_file.get("tracks", [])

  albums_dict = {}
  album_id = 1

  for track in tracks:
    album_name = track["album"]

    if album_name not in albums_dict:
      albums_dict[album_name] = {
        "album_id": album_id,
        "album_name": album_name,
        "artists_names": track["artists"],
        "artists_links": track["artists_links"],
        "album_year": track["track_year"],
        "album_img": track["track_img"],
        "tracks": []
      }
      album_id += 1


    albums_dict[album_name]["tracks"].append({
      "track_name": track["track_name"],
      "track_artists": track["artists"],
      "track_play_count": track["play_count"],
      "track_iframe": track["track_iframe"],
      "track_time": track["track_time"]
    })
    

  albums = list(albums_dict.values())

  # Load artists file
  artists_folder = f"{COLLECTIONS_SPOTIFY_BILLION_CLUB_ARTISTS_FOLDER}/"
  artists_json_file_path = get_latest_json_file(artists_folder)
  artists = load_json_from_file(artists_json_file_path)

  # Map artist name → image URL ("" if missing)
  artist_index = {artist["artist_name"]: artist.get("artist_img", "") for artist in artists}

  # Add artist image if only one artist
  for album in albums:
    album_artists = album.get("artists_names", [])
    if len(album_artists) == 1:
      album["artist_img"] = artist_index.get(album_artists[0], "")
    else:
      album["artist_img"] = ""

  file_name = f"albums_{int(time.time())}.json"
  file_path = os.path.join(COLLECTIONS_SPOTIFY_BILLION_CLUB_ALBUMS_FOLDER, file_name)

  try:
    # Json file creation
    with open(file_path, "w", encoding="utf-8") as file:
      json.dump(albums, file, indent=2, ensure_ascii=False)
      
    logger.info(f"✅ Albums JSON file created: {file_path}\n")
    return file_path

  except Exception as e:
    logger.error(f"❌ Error creating albums JSON file: {e}", exc_info=True)


  # End timer
  end_updating_tracks = time.perf_counter()
  updating_elapsed = end_updating_tracks - start_updating_tracks
  logger.info(f'⏰ Albums JSON file created in {updating_elapsed:.2f} seconds\n')

  logger.info("✅ Albums JSON created")
