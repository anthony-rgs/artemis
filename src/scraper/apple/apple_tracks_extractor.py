from src.config import APPLE_TRACKLIST_ROW_SELECTOR, APPLE_TITLE_SELECTOR, APPLE_SUBTITLE_SELECTOR, APPLE_TRACK_COLUMN_SELECTOR, APPLE_ARTIST_COLUMN_SELECTOR, APPLE_ALBUM_COLUMN_SELECTOR


# Clean Apple page tracks 
def get_clean_page_tracks(page, tracks):
  # Waiting for elements
  page.wait_for_selector(APPLE_TRACKLIST_ROW_SELECTOR, timeout=10_000)

  # Get all page tracks
  page_tracks = page.query_selector_all(APPLE_TRACKLIST_ROW_SELECTOR)

  # Convert tracks list to a set of tuples for fast lookup
  existing_tracks = {tuple(track) for track in tracks}

  return page_tracks, existing_tracks


# Extract Apple album tracks
def apple_extract_album_tracks(page, tracks, _):
  page_tracks, existing_tracks = get_clean_page_tracks(page, tracks)
  
  # Album informations
  album_name = page.query_selector(APPLE_TITLE_SELECTOR).text_content()
  album_artists_element = page.query_selector(APPLE_SUBTITLE_SELECTOR)
  album_artists_name = [a.text_content() for a in album_artists_element.query_selector_all('a')]
  album_link = page.url

  for page_track in page_tracks:
    try:
      track_element = page_track.query_selector(APPLE_TRACK_COLUMN_SELECTOR)
      track_link = track_element.query_selector('a')
      track_name = track_element.query_selector('div')

      track_info = (
        album_name,  # Album name
        album_link,  # Album link
        tuple(artist for artist in album_artists_name if artist.strip()),  # Artists (as tuple)
        track_name.text_content(),  # Track name
        track_link.get_attribute('href'),  # Track link
      )

      # Add only if not already in the set
      if track_info not in existing_tracks:
        tracks.append(track_info)
        existing_tracks.add(track_info)  # Update the set

    except Exception:
      pass

  return tracks


# Extract Apple playlist tracks
def apple_extract_playlist_tracks(page, tracks, _):
  page_tracks, existing_tracks = get_clean_page_tracks(page, tracks)

  for page_track in page_tracks:
    try:
      artists_element = page_track.query_selector(APPLE_ARTIST_COLUMN_SELECTOR)
      artists = artists_element.query_selector_all("span")

      album = page_track.query_selector(f"{APPLE_ALBUM_COLUMN_SELECTOR} a")

      track_element = page_track.query_selector(APPLE_TRACK_COLUMN_SELECTOR)
      track_link = track_element.query_selector('a')
      track_name = track_element.query_selector('div')
      
      # Check if there are data
      if not (album and artists and track_link and track_name):
        continue  

      # Extract track informations
      track_info = (
        album.text_content(),  # Album name
        album.get_attribute('href'),  # Album link
        tuple(artist.text_content().strip() for artist in artists if artist.text_content().strip()),  # Artists (as tuple)
        track_name.text_content(),  # Track name
        track_link.get_attribute('href'),  # Track link
      )

      # Add only if not already in the set
      if track_info not in existing_tracks:
        tracks.append(track_info)
        existing_tracks.add(track_info)  # Update the set

    except Exception:
      pass
      
  return tracks