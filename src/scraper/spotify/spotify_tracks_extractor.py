from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from src.config import SPOTIFY_TRACKLIST_ROW_SELECTOR, SPOTIFY_MUSIC_COLUMN_SELECTOR, SPOTIFY_ALBUM_COLUMN_SELECTOR

# Extract all Spotify tracks in a page
def spotify_extract_tracks(driver, tracks):
  # Waiting for elements
  WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, SPOTIFY_TRACKLIST_ROW_SELECTOR)))

  # Get all page tracks
  page_tracks = driver.find_elements(By.CSS_SELECTOR, SPOTIFY_TRACKLIST_ROW_SELECTOR)

  # Convert tracks list to a set of tuples for fast lookup
  existing_tracks = {tuple(track) for track in tracks}
  
  for page_track in page_tracks:
    try:
      elements = {
        "album": page_track.find_element(By.CSS_SELECTOR, SPOTIFY_ALBUM_COLUMN_SELECTOR),
        "music": page_track.find_element(By.CSS_SELECTOR, SPOTIFY_MUSIC_COLUMN_SELECTOR)
      }

      # Links
      album_links = elements["album"].find_elements(By.TAG_NAME, 'a')
      music_links = elements["music"].find_elements(By.TAG_NAME, 'a')

      # Check if there are data
      if not (music_links and album_links):
        continue  

      # Extract track informations
      track_info = (
        album_links[0].text,  # Album name
        album_links[0].get_attribute("href"),  # Album link
        tuple(link.text for link in music_links[1:] if link.text.strip()),  # Artists (as tuple)
        music_links[0].text,  # Music name
        music_links[0].get_attribute("href"),  # Music link
      )

      # Add only if not already in the set
      if track_info not in existing_tracks:
        tracks.append(track_info)
        existing_tracks.add(track_info)  # Update the set

    except Exception:
      pass
      
  return tracks