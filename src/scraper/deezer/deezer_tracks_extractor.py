import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from src.config import DEEZER_TRACKLIST_ROW_SELECTOR, DEEZER_INFORMATIONS_SELECTOR, DEEZER_TITLE_SELECTOR, DEEZER_ALBUM_ARTIST_NAME_SELECTOR, DEEZER_TRACKLIST_ROW_TRACK_SELECTOR, DEEZER_TRACKLIST_ROW_TRACK_SELECTOR, DEEZER_PLAYLIST_ALBUM_SELECTOR, DEEZER_TRACKLIST_ROW_ARTIST_SELECTOR

# Clean Deezer page tracks 
def get_clean_page_tracks(driver, tracks):
  # Waiting for elements
  WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, DEEZER_TRACKLIST_ROW_SELECTOR)))

  # Get all page tracks
  page_tracks = driver.find_elements(By.CSS_SELECTOR, DEEZER_TRACKLIST_ROW_SELECTOR)

  # Convert tracks list to a set of tuples for fast lookup
  existing_tracks = {tuple(track) for track in tracks}

  return page_tracks, existing_tracks


# Extract Deezer album tracks
def deezer_extract_album_tracks(driver, tracks, _):
  page_tracks, existing_tracks = get_clean_page_tracks(driver, tracks)
  
  # Album informations
  top_container_informations = driver.find_element(By.CSS_SELECTOR, DEEZER_INFORMATIONS_SELECTOR)
  album_name = top_container_informations.find_element(By.CSS_SELECTOR, DEEZER_TITLE_SELECTOR).text
  album_artist_name = driver.find_element(By.CSS_SELECTOR, DEEZER_ALBUM_ARTIST_NAME_SELECTOR).text  # Artist who created the album
  album_link = driver.current_url
  
  # Remove the default wait time for the driver
  # The artist cell in the track row may be empty
  driver.implicitly_wait(0) 
  
  for page_track in page_tracks:
    try:
      # Deezer doesn't include the album artist in the track row
      artists = [album_artist_name] # Add album artist name on a empty array

      first_div = page_track.find_element(By.TAG_NAME, "div")
    
      # Get and clean track name : 1. Delilah (pull me out of this) -> Delilah (pull me out of this)
      # ^    → Start of the string  
      # \d+  → Remove one or more digits (track number)  
      # \.   → Removes the first literal dot (the backslash \ is used to escape the dot, as dot normally means "any character" in regex)
      # \s*  → Remove any spaces after the dot  
      track_name = first_div.find_element(By.CSS_SELECTOR, DEEZER_TRACKLIST_ROW_TRACK_SELECTOR)
      track_name_cleaned = re.sub(r"^\d+\.\s*", "", track_name.text)

      # Get featured artists
      featured_artists = first_div.find_elements(By.CSS_SELECTOR, DEEZER_TRACKLIST_ROW_ARTIST_SELECTOR)
      if featured_artists:
        for featured_artist in featured_artists:
          artists.append(featured_artist.text)
      
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
  
  # Reset driver.implicitly_wait to its default setting
  driver.implicitly_wait(10)
  return tracks


# Extract Deezer playlist tracks
def deezer_extract_playlist_tracks(driver, tracks, _):
  page_tracks, existing_tracks = get_clean_page_tracks(driver, tracks)

  for page_track in page_tracks:
    try:
      first_div = page_track.find_element(By.TAG_NAME, "div")
      artists = first_div.find_elements(By.CSS_SELECTOR, DEEZER_TRACKLIST_ROW_ARTIST_SELECTOR)
      album = first_div.find_element(By.CSS_SELECTOR, DEEZER_PLAYLIST_ALBUM_SELECTOR)
      track_name = first_div.find_element(By.CSS_SELECTOR, DEEZER_TRACKLIST_ROW_TRACK_SELECTOR)
      
      # Check if there are data
      if not (album and artists and track_name):
        continue  

      # Extract track informations
      track_info = (
        album.text,  # Album name
        album.get_attribute('href'),  # Album link
        tuple(artist.text for artist in artists if artist.text.strip()),  # Artists (as tuple)
        track_name.text,  # Track name
        "",  # No track link...
      )

      # Add only if not already in the set
      if track_info not in existing_tracks:
        tracks.append(track_info)
        existing_tracks.add(track_info)  # Update the set

    except Exception:
      pass
      
  return tracks