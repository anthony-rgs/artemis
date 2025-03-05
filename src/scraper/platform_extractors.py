from src.scraper.spotify.spotify_parser import spotify_extract_name, spotify_count_tracks
from src.scraper.spotify.spotify_tracks_extractor import spotify_extract_tracks
from src.scraper.spotify.spotify_scroll_container import get_spotify_scroll_container


PLATFORM_FUNCTIONS = {
  "spotify": {
    "count_tracks": spotify_count_tracks,
    "extract_name": spotify_extract_name,
    "get_scroll_container": get_spotify_scroll_container,
    "extract_tracks": spotify_extract_tracks,
  },
  "deezer": {
    "count_tracks": "",
    "extract_name": "",
    "get_scroll_container": "",
    "extract_tracks": "",
  }
}
