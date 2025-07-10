from src.config import BASE_SPOTIFY_URL, SPOTIFY_TRACKLIST_ROW_SELECTOR, SPOTIFY_TRACK_COLUMN_SELECTOR, SPOTIFY_ALBUM_COLUMN_SELECTOR, SPOTIFY_TITLE_SELECTOR
from src.utils.logger import logger


# Clean Spotify page tracks 
def get_clean_page_tracks(page, tracks, total_tracks):
  # Waiting for elements
  page.wait_for_selector(SPOTIFY_TRACKLIST_ROW_SELECTOR, timeout=10_000, state="attached")

  # Get all page tracks
  page_tracks = page.query_selector_all(SPOTIFY_TRACKLIST_ROW_SELECTOR)

  # Convert tracks list to a set of tuples for fast lookup
  existing_tracks = {tuple(track) for track in tracks}
  
  # If too many tracks are retrieved, it means recommended tracks were included, so we trim the list.
  # This only triggers for small playlists with fewer than 25 tracks.
  if len(page_tracks) > total_tracks:
    page_tracks = page_tracks[0:total_tracks]  # Reset the list length to match the original playlist size.
    logger.info(f"🔪 More tracks scraped than the actual playlist size, list trimmed")

  return page_tracks, existing_tracks


# Extract Spotify album tracks
def spotify_extract_album_tracks(page, tracks, total_tracks):
  page_tracks, existing_tracks = get_clean_page_tracks(page, tracks, total_tracks)
  
  # The albums contain few tracks, so it's not an issue to load their data here, within the scroll loop
  album_name = page.locator(SPOTIFY_TITLE_SELECTOR).text_content()
  album_link = page.url
  
  for page_track in page_tracks:
    try:
      # Element
      track_element = page_track.query_selector(SPOTIFY_TRACK_COLUMN_SELECTOR)
      track_links = track_element.query_selector_all("a")
      
      # Check if there are data
      if not track_links:
        continue  

      # Extract track informations
      track_info = (
        album_name,  # Album name
        album_link,  # Album link
        tuple(link.text_content().strip() for link in track_links[1:] if link.text_content().strip()),  # Artists (as tuple)
        track_links[0].text_content(),  # Track name
        BASE_SPOTIFY_URL + track_links[0].get_attribute("href"),  # Track link
      )

      # Add only if not already in the set
      if track_info not in existing_tracks:
        tracks.append(track_info)
        existing_tracks.add(track_info)  # Update the set

    except Exception:
      pass
      
  return tracks


# Extract Spotify playlist tracks
def spotify_extract_playlist_tracks(page, tracks, total_tracks):
  page_tracks, existing_tracks = get_clean_page_tracks(page, tracks, total_tracks)

  for page_track in page_tracks:
    try:
      # Elements
      elements = {
          "album": page_track.query_selector(SPOTIFY_ALBUM_COLUMN_SELECTOR),
          "track": page_track.query_selector(SPOTIFY_TRACK_COLUMN_SELECTOR)
      }
      album_links = elements["album"].query_selector_all('a')
      track_links = elements["track"].query_selector_all('a')

      # Check if there are data
      if not (track_links and album_links):
        continue  

      # Extract track informations
      track_info = (
        album_links[0].inner_text(),  # Album name
        BASE_SPOTIFY_URL + album_links[0].get_attribute("href"),  # Album link
        tuple(link.inner_text() for link in track_links[1:] if link.inner_text().strip()),  # Artists (as tuple)
        track_links[0].inner_text(),  # Track name
        BASE_SPOTIFY_URL + track_links[0].get_attribute("href"),  # Track link
      )

      # Add only if not already in the set
      if track_info not in existing_tracks:
        tracks.append(track_info)
        existing_tracks.add(track_info)  # Update the set

    except Exception:
      pass
      
  return tracks