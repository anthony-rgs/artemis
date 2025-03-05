from src.config import MAX_RETRIES
from src.utils.logger import logger 
from src.utils.json_handler import create_json 
from src.utils.retry import retry_function
from src.utils.validator import check_scraped_data
from src.utils.url_handler import check_link
from src.utils.string_utils import format_name
from src.scraper.driver import init_driver, close_driver
from src.scraper.platform_extractors import PLATFORM_FUNCTIONS
from src.scraper.scroll_manager import retry_and_check_tracks

# Scrapes a collection from the given platform
def scrape_collection(tracks_url, json_save = True ):
  check_url = check_link(tracks_url)

  if check_url:
    platform, content_type = check_url

    driver = retry_function(init_driver)

    if not driver:
      return None

    logger.info(f"🌍 Navigating to {platform} tracks...\n")

    driver.get(tracks_url)

    # Select platform-specific functions
    count_tracks = PLATFORM_FUNCTIONS[platform]["count_tracks"]
    extract_name = PLATFORM_FUNCTIONS[platform]["extract_name"]
    get_scroll_container = PLATFORM_FUNCTIONS[platform]["get_scroll_container"]
    extract_tracks = PLATFORM_FUNCTIONS[platform]["extract_tracks"]

    total_tracks = retry_function(count_tracks, driver)

    scroll_container = get_scroll_container(driver)
    
    tracks = retry_function(retry_and_check_tracks, driver, total_tracks, scroll_container, extract_tracks)

    if not tracks:
      logger.error(f"💀 Tracks scraping failed after multiple retries... \n")
      close_driver(driver)
      return None
    
    else:
      # Save in Json
      if json_save:
        logger.info("💾 Saving data in JSON file...\n")  

        name = retry_function(extract_name, driver)
        formatted_name = retry_function(format_name, name)
        create_json(tracks, tracks_url, formatted_name)

      logger.info(f"🎉 You rock, Artémis !\n")

      close_driver(driver)

      return tracks