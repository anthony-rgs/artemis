import os
from datetime import datetime

# =======================
# Logging Configuration
# =======================

LOG_FOLDER = "logs/"  # Folder where log files are saved
os.makedirs(LOG_FOLDER, exist_ok=True)  # Create folder if it doesn't exist

LOG_FILE = os.path.join(LOG_FOLDER, f"artemis_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log") # Log file name
SAVE_LOG = False  # Enables/disables logging to a file


# =======================
# Selenium Configuration
# =======================

SELENIUM_OPTIONS = {
  "headless": True,  # Run browser in headless mode (no UI)
  "disable_gpu": True,  # Disable GPU acceleration (fixes issues in headless mode)
  "no_sandbox": True,  # Required for running in some environments (e.g., Linux servers)
  "disable_dev_shm_usage": True,  # To prevent memory issues on Docker/Linux.
  "window_size": "2560,1440",  # Set window size for consistent rendering
  "implicit_wait": 5,  # Implicit wait for elements
}

SELENIUM_TIMEOUT = 10  # Explicit wait timeout (seconds)


# =======================
# Paths & File Handling
# =======================

COLLECTIONS_FOLDER = "collections"  # Folder where collections JSON files are saved
COLLECTIONS_SPOTIFY_FOLDER = os.path.join(COLLECTIONS_FOLDER, "spotify")
COLLECTIONS_DEEZER_FOLDER = os.path.join(COLLECTIONS_FOLDER, "deezer")
# Create folders if they doesn't exist
for folder in [COLLECTIONS_FOLDER, COLLECTIONS_SPOTIFY_FOLDER, COLLECTIONS_DEEZER_FOLDER]:
  os.makedirs(folder, exist_ok=True)


# =======================
# Scraping Configuration
# =======================

SCROLL_STEP = 500

# Spotify
SPOTIFY_BASE_URL = "https://open.spotify.com/"
SPOTIFY_BILLION_CLUB_URL = "https://open.spotify.com/playlist/37i9dQZF1DX7iB3RCnBnN4"
SPOTIFY_TITLE_SELECTOR = '[data-testid="entityTitle"]'  # Selector for title
SPOTIFY_ALBUM_TOTAL_TRACKS_XPATH = "//main/section/div[1]/div[2]/div[2]/div[1]/div[2]/span"  # ALBUM -> Xpath from main to total tacks span
SPOTIFY_PLAYLIST_TOTAL_TRACKS_ATTR = "aria-rowcount"  # PLAYLIST -> Attribute to fetch the total number of tracks
SPOTIFY_PLAY_COUNT_SELECTOR = '[data-testid="playcount"]'  # Selector for play count
SPOTIFY_TRACKLIST_ROW_SELECTOR = '[data-testid="tracklist-row"]'  # Selector for tracklist row
SPOTIFY_MUSIC_COLUMN_SELECTOR  = 'div[aria-colindex="2"]'  # Music data column
SPOTIFY_ALBUM_COLUMN_SELECTOR  = 'div[aria-colindex="3"]'  # Album data column
SPOTIFY_SCROLL_CONTAINER = '[data-overlayscrollbars-viewport]'  # Container for scrolling

# Deezer
DEEZER_INFORMATIONS_SELECTOR = '[data-testid="masthead"]'  # Selector for header information
DEEZER_TITLE_SELECTOR = 'h2'  # <h2> -> title
DEEZER_TOTAL_TRACKS_XPATH = '(//ul)[2]//li'  # Second <ul> and first <li>
DEEZER_SCROLL_CONTAINER = 'body'  # Container for scrolling


# =======================
# Error Handling & Retries
# =======================

MAX_RETRIES = 3  # Maximum number of function retries before failing
RETRY_WAIT_TIME = 3  # Wait time (seconds) before retrying a failed function
