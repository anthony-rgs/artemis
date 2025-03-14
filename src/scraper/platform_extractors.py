# Spotify
from src.scraper.spotify.spotify_parser import spotify_extract_name, spotify_count_tracks
from src.scraper.spotify.spotify_tracks_extractor import spotify_extract_album_tracks, spotify_extract_playlist_tracks
from src.scraper.spotify.spotify_scroll_container import get_spotify_scroll_container
# Deezer
from src.scraper.deezer.deezer_parser import deezer_extract_name, deezer_count_tracks
from src.scraper.deezer.deezer_tracks_extractor import deezer_extract_album_tracks, deezer_extract_playlist_tracks
from src.scraper.deezer.deezer_scroll_container import get_deezer_scroll_container


PLATFORM_FUNCTIONS = {
  "spotify": {
    "count_tracks": spotify_count_tracks,
    "extract_name": spotify_extract_name,
    "get_scroll_container": get_spotify_scroll_container,
    "extract_tracks": {
      "album": spotify_extract_album_tracks,
      "playlist": spotify_extract_playlist_tracks
    }
  },
  "deezer": {
    "count_tracks": deezer_count_tracks,
    "extract_name": deezer_extract_name,
    "get_scroll_container": get_deezer_scroll_container,
    "extract_tracks": {
      "album": deezer_extract_album_tracks,
      "playlist": deezer_extract_playlist_tracks
    },
  }
}
