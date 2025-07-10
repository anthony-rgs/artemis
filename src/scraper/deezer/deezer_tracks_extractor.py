import re
from src.config import DEEZER_TRACKLIST_ROW_SELECTOR, DEEZER_INFORMATIONS_SELECTOR, DEEZER_TITLE_SELECTOR, DEEZER_ALBUM_ARTIST_NAME_SELECTOR, DEEZER_TRACKLIST_ROW_TRACK_SELECTOR, DEEZER_TRACKLIST_ROW_TRACK_SELECTOR, DEEZER_PLAYLIST_ALBUM_SELECTOR, DEEZER_TRACKLIST_ROW_ARTIST_SELECTOR

# Clean Deezer page tracks 
def get_clean_page_tracks(page, tracks):
  # Waiting for elements
  page.wait_for_selector(DEEZER_TRACKLIST_ROW_SELECTOR, timeout=10_000)

  # Get all page tracks
  page_tracks = page.query_selector_all(DEEZER_TRACKLIST_ROW_SELECTOR)

  # Convert tracks list to a set of tuples for fast lookup
  existing_tracks = {tuple(track) for track in tracks}

  return page_tracks, existing_tracks


# Extract Deezer album tracks
def deezer_extract_album_tracks(page, tracks, _):
  page_tracks, existing_tracks = get_clean_page_tracks(page, tracks)
  
  # Album informations
  top_container_informations = page.query_selector(DEEZER_INFORMATIONS_SELECTOR)
  album_name = top_container_informations.query_selector(DEEZER_TITLE_SELECTOR).text_content()
  album_artist_name = page.query_selector(DEEZER_ALBUM_ARTIST_NAME_SELECTOR).text_content()
  album_link = page.url
  
  # Remove the default wait time for Playwright
  # The artist cell in the track row may be empty
  page.set_default_timeout(0)  

  for page_track in page_tracks:
    try:
      # Deezer doesn't include the album artist in the track row
      artists = [album_artist_name] # Start array with album artist name

      first_div = page_track.query_selector("div")
    
      # Get and clean track name : 1. Delilah (pull me out of this) -> Delilah (pull me out of this)
      # ^    → Start of the string  
      # \d+  → Remove one or more digits (track number)  
      # \.   → Removes the first literal dot (the backslash \ is used to escape the dot, as dot normally means "any character" in regex)
      # \s*  → Remove any spaces after the dot  
      track_name_element = page_track.query_selector(DEEZER_TRACKLIST_ROW_TRACK_SELECTOR)
      track_name_text = track_name_element.text_content()
      track_name_cleaned = re.sub(r"^\d+\.\s*", "", track_name_text)

      # Get featured artists
      featured_artists = first_div.query_selector_all(DEEZER_TRACKLIST_ROW_ARTIST_SELECTOR)

      if featured_artists:
        for featured_artist in featured_artists:
          artists.append(featured_artist.text_content())
      
      # Extract track informations
      track_info = (
        album_name,  # Album name
        album_link,  # Album link
        tuple(artist for artist in artists if artist.strip()),  # Artists (as tuple)
        track_name_cleaned,  # Track name
        "",  # No track link...
      )

      # Add only if not already in the set
      if track_info not in existing_tracks:
        tracks.append(track_info)
        existing_tracks.add(track_info)  # Update the set

    except Exception:
      pass
  
  # Reset Playwright wait to its default setting
  page.set_default_timeout(10000)
  return tracks


# Extract Deezer playlist tracks
def deezer_extract_playlist_tracks(page, tracks, _):
  page_tracks, existing_tracks = get_clean_page_tracks(page, tracks)

  for page_track in page_tracks:
    try:
      first_div = page_track.query_selector("div")
      artists = first_div.query_selector_all(DEEZER_TRACKLIST_ROW_ARTIST_SELECTOR)
      album = first_div.query_selector(DEEZER_PLAYLIST_ALBUM_SELECTOR)
      track_name = first_div.query_selector(DEEZER_TRACKLIST_ROW_TRACK_SELECTOR)
      
      # Check if there are data
      if not (album and artists and track_name):
        continue  

      # Extract track informations
      track_info = (
        album.text_content(),  # Album name
        album.get_attribute('href'),  # Album link
        tuple(artist.text_content() for artist in artists if artist.text_content().strip()),  # Artists (as tuple)
        track_name.text_content(),  # Track name
        "",  # No track link...
      )

      # Add only if not already in the set
      if track_info not in existing_tracks:
        tracks.append(track_info)
        existing_tracks.add(track_info)  # Update the set

    except Exception:
      pass
      
  return tracks