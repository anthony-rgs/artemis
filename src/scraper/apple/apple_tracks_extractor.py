from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.config import APPLE_TRACKLIST_ROW_SELECTOR, APPLE_TITLE_SELECTOR, APPLE_SUBTITLE_SELECTOR, APPLE_TRACK_COLUMN_SELECTOR, APPLE_ARTIST_COLUMN_SELECTOR, APPLE_ALBUM_COLUMN_SELECTOR


# Clean Apple page tracks 
def get_clean_page_tracks(driver, tracks):
  # Waiting for elements
  WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, APPLE_TRACKLIST_ROW_SELECTOR)))

  # Get all page tracks
  page_tracks = driver.find_elements(By.CSS_SELECTOR, APPLE_TRACKLIST_ROW_SELECTOR)

  # Convert tracks list to a set of tuples for fast lookup
  existing_tracks = {tuple(track) for track in tracks}

  return page_tracks, existing_tracks


# Extract Apple album tracks
def apple_extract_album_tracks(driver, tracks, _):
  page_tracks, existing_tracks = get_clean_page_tracks(driver, tracks)
  
  # Album informations
  album_name = driver.find_element(By.CSS_SELECTOR, APPLE_TITLE_SELECTOR)
  album_artists_element = driver.find_element(By.CSS_SELECTOR, APPLE_SUBTITLE_SELECTOR)
  album_artists_name = album_artists_element.find_elements(By.CSS_SELECTOR, 'a')
  album_link = driver.current_url

  for page_track in page_tracks:
    try:
      track_element = page_track.find_element(By.CSS_SELECTOR, APPLE_TRACK_COLUMN_SELECTOR)
      track_link = track_element.find_element(By.CSS_SELECTOR, 'a')
      track_name = track_element.find_element(By.CSS_SELECTOR, 'div')

      # Extract track informations
      track_info = (
        album_name.text,  # Album name
        album_link,  # Album link
        tuple(artist.text for artist in album_artists_name if artist.text.strip()),  # Artists (as tuple)
        track_name.text,  # Track name
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
def apple_extract_playlist_tracks(driver, tracks, _):
  page_tracks, existing_tracks = get_clean_page_tracks(driver, tracks)

  for page_track in page_tracks:
    try:

      artists_element = page_track.find_element(By.CSS_SELECTOR, APPLE_ARTIST_COLUMN_SELECTOR)
      artists = artists_element.find_elements(By.CSS_SELECTOR, "span")
     
      album = page_track.find_element(By.CSS_SELECTOR, APPLE_ALBUM_COLUMN_SELECTOR).find_element(By.CSS_SELECTOR, 'a')

      track_element = page_track.find_element(By.CSS_SELECTOR, APPLE_TRACK_COLUMN_SELECTOR)
      track_link = track_element.find_element(By.CSS_SELECTOR, 'a')
      track_name = track_element.find_element(By.CSS_SELECTOR, 'div')

      # Check if there are data
      if not (album and artists and track_link and track_name):
        continue  

      # Extract track informations
      track_info = (
        album.text,  # Album name
        album.get_attribute('href'),  # Album link
        tuple(artist.text for artist in artists if artist.text.strip()),  # Artists (as tuple)
        track_name.text,  # Track name
        track_link.get_attribute('href'),  # Track link
      )


      # Add only if not already in the set
      if track_info not in existing_tracks:
        tracks.append(track_info)
        existing_tracks.add(track_info)  # Update the set

    except Exception:
      pass
      
  return tracks