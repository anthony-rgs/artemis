# Default imports
import time
import re
import json
# Selenium imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
# Webdrive import
from webdriver_manager.chrome import ChromeDriverManager

# Start driver
def start_driver(playlist_link):
  driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
  driver.get(playlist_link)
  time.sleep(5) # Wait 5 seconds for loading page
  return driver

# Get playlist name formatted and clean
def get_playlist_name(driver):
  # Regex to remove emojis  
  emoji_pattern = re.compile(
    "["
    "\U0001F600-\U0001F64F"  # Emoticons  
    "\U0001F300-\U0001F5FF"  # Symbols & pictograms  
    "\U0001F680-\U0001F6FF"  # Transport & map symbols  
    "\U0001F700-\U0001F77F"  # Alchemical symbols  
    "\U0001F780-\U0001F7FF"  # Miscellaneous symbols  
    "\U0001F800-\U0001F8FF"  # More miscellaneous symbols  
    "\U0001F900-\U0001F9FF"  # Supplemental emojis  
    "\U0001FA00-\U0001FA6F"  # Additional symbols  
    "\U0001FA70-\U0001FAFF"  # More additional symbols  
    "\U00002702-\U000027B0"  # Dingbats  
    "\U000024C2-\U0001F251"  # Enclosed characters  
    "]+", flags=re.UNICODE
  )
    
  playlist_name = driver.find_element("css selector", '[data-testid="entityTitle"]').text
  playlist_name_formatted = playlist_name.replace(" ", "-").lower()

  return emoji_pattern.sub(r'', playlist_name_formatted)


# Create a json file with playlist data
def create_json(playlist_musics, playlist_link, playlist_name):
  playlist_length = len(playlist_musics)
  timestamp = int(time.time())

  musics = [
    {
      "music_name": music_name, 
      "artists": artists, 
      "album": album, 
      "cover_img": cover_img,
      "music_link": music_link,
      "album_link": album_link, 
    } for album, album_link, artists, cover_img, music_name, music_link in playlist_musics]

  data = {
      "name": playlist_name,
      "length": playlist_length,
      "link": playlist_link,
      "musics": musics
  }

  file_path = f"playlists/{playlist_name}_{timestamp}.json"

  # Création et écriture dans un fichier JSON
  with open(file_path, "w", encoding="utf-8") as file:
    json.dump(data, file, indent=2, ensure_ascii=False)
    print(f"💾 {playlist_name}.json has been created")


# Check and display message at the end of the scrap
def checks(playlist_musics, row_count):
  length = int(len(playlist_musics))
  completed = row_count == length

  if completed:
    print("✅ You rock Artémis")
    print(f"🎧 {length} musics have been recovered")
  elif length > row_count:
    duplicates = length - row_count 
    print(f"❌ There are {duplicates} duplicates")
  else:
    missing_tracks = row_count - length
    print(f"❌ There are missing {missing_tracks} musics")
  
  return completed

# Check spotify link
def check_link(link):
  if "open.spotify.com" not in link:
    print("Ce n'est pas un lien Spotify")
    return False

  if "playlist" not in link:
    print("Ce n'est pas un lien de playlist")
    return False

  return True

# Get playlist music's
def get_musics(driver, playlist_musics):
  # Attendre que les tracks apparaissent (timeout de 10 secondes)
  WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="tracklist-row"]')))

  # Récupérer tous les tracks
  tracks = driver.find_elements(By.CSS_SELECTOR, '[data-testid="tracklist-row"]')

  for track in tracks:
    artists_array = []
    music_elements = track.find_element(By.CSS_SELECTOR, 'div[aria-colindex="2"]')
    album_elements = track.find_element(By.CSS_SELECTOR, 'div[aria-colindex="3"]')

    if music_elements and album_elements:
      music_links = music_elements.find_elements(By.TAG_NAME, 'a')
      cover_link = music_elements.find_elements(By.TAG_NAME, 'img')
      album_links = album_elements.find_elements(By.TAG_NAME, 'a')

      
      for i, link in enumerate(music_links):
        if i > 0: # Remove first element
          artists_array.append(link.text)

      album = album_links[0].text
      album_link = album_links[0].get_attribute("href")
      artists = artists_array
      cover_img = cover_link[0].get_attribute("src")
      music_name = music_links[0].text
      music_link = music_links[0].get_attribute("href")

      track_info = [album, album_link, artists, cover_img, music_name, music_link]

      if track_info not in playlist_musics:
        playlist_musics.append(track_info)
      
  return playlist_musics


# Scroll in the page
def scroll(driver, playlist_musics, row_count):
  
  last_scroll = 0

  # Trouver le conteneur avec l'attribut `data-overlayscrollbars-viewport`
  container = driver.find_elements(By.CSS_SELECTOR, '[data-overlayscrollbars-viewport]')[1] # "1" is the container with all music rows

  while True:
    # Completion
    percent_completion = 100 * len(playlist_musics) / row_count
    print(f"{round(percent_completion, 1)}%")

    # Scroll vers le bas par petits pas
    driver.execute_script("arguments[0].scrollTop += arguments[1];", container, 400)

    # Vérifier si le scroll avance toujours
    new_scroll = driver.execute_script("return arguments[0].scrollTop;", container)

    if new_scroll == last_scroll or percent_completion >= 100:
      break 
    
    get_musics(driver, playlist_musics)

    last_scroll = new_scroll
  
  return playlist_musics


# Fetch playlist
def fetch_playlit(playlist_link, options = {"checks": True, "json": True }):
  completed = "idle" # Waiting for bool
  playlist_musics = []

  # start driver
  driver = start_driver(playlist_link)
  
  # Get the number of musics
  row_count_element = driver.find_element("css selector", '[aria-rowcount]')
  row_count = int(row_count_element.get_attribute("aria-rowcount")) - 1
  
  # scroll in the page to load data and fetch musics
  scroll(driver, playlist_musics, row_count)

  if options["checks"]:
    # Run checks
    completed = checks(playlist_musics, row_count)

  if options["json"]:

    if completed or completed == "idle":
      # Save playlist data
      playlist_name = get_playlist_name(driver)
      create_json(playlist_musics, playlist_link, playlist_name)
      if completed == "idle":
        print("⚠ Data saved, but no checks done")
    else:
      print("❌ There are missing musics, data not saved")
      
  # Close driver
  driver.quit()

  return playlist_musics