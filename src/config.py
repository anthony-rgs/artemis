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
    "window_size": "1920,1080",  # Set window size for consistent rendering
    "implicit_wait": 5,  # Implicit wait for elements
}

SELENIUM_TIMEOUT = 10  # Explicit wait timeout (seconds)
MAX_SCROLL_ATTEMPTS = 10  # Limit for scrolling retries


# =======================
# Paths & File Handling
# =======================

PLAYLISTS_FOLDER = "playlists/"  # Folder where playlist JSON files are saved
os.makedirs(PLAYLISTS_FOLDER, exist_ok=True)  # Create folder if it doesn't exist


# =======================
# Scraping Configuration
# =======================

SPOTIFY_BASE_URL = "https://open.spotify.com/"
SPOTIFY_PLAYLIST_TITLE_SELECTOR = '[data-testid="entityTitle"]'  # Selector for playlist title
SPOTIFY_TRACKLIST_SELECTOR = '[data-testid="tracklist-row"]'  # Selector for tracklist
SPOTIFY_ROW_COUNT_ATTR = "aria-rowcount"  # Attribute to fetch the total number of tracks
SPOTIFY_SCROLL_CONTAINER = '[data-overlayscrollbars-viewport]'  # Container for scrolling


# =======================
# Error Handling & Retries
# =======================

MAX_RETRIES = 3  # Maximum number of function retries before failing
RETRY_WAIT_TIME = 2  # Wait time (seconds) before retrying a failed function
