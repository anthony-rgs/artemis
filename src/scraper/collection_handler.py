import time

from src.utils.retry import retry_function
from src.utils.logger import logger 
from src.utils.url_handler import check_link
from src.utils.json_handler import create_json_file 
from src.utils.string_utils import format_name

from src.scraper.driver import init_driver, close_driver
from src.scraper.scroll_manager import retry_and_check_tracks
from src.scraper.insert_custom_div import insert_custom_div
from src.scraper.platform_extractors import PLATFORM_FUNCTIONS


# Scrapes a collection from the given platform
def scrape_collection(tracks_url, json_save = True, kill_script = True ):
  # Start script timer
  start_scraping = time.perf_counter()

  check_url = check_link(tracks_url)

  if check_url:
    platform, content_type = check_url

    # Init driver
    driver = retry_function(init_driver)

    if not driver:
      return None

    logger.info(f"🌍 Navigating to {platform} tracks...\n")
    
    # Load page with url 
    driver.get(tracks_url)

    # Insert custom div
    insert_custom_div(driver)

    # Select platform-specific functions
    count_tracks = PLATFORM_FUNCTIONS[platform]["count_tracks"]
    extract_name = PLATFORM_FUNCTIONS[platform]["extract_name"]
    get_scroll_container = PLATFORM_FUNCTIONS[platform]["get_scroll_container"]
    extract_tracks = PLATFORM_FUNCTIONS[platform]["extract_tracks"][content_type]

    # Get total tracks
    total_tracks = retry_function(count_tracks, driver, content_type)

    # Get scroll container
    scroll_container = get_scroll_container(driver)
    
    # Start scrolling timer
    start_scrolling = time.perf_counter()

    # Retrieve all tracks on the page and retry if the tracks are incomplete
    tracks = retry_function(retry_and_check_tracks, driver, total_tracks, scroll_container, extract_tracks)  # Get tracks
    
    # End scrolling timer
    end_scrolling = time.perf_counter()
    scrolling_elapsed = end_scrolling - start_scrolling
    logger.info(f'⏰ Scrolling completed in {scrolling_elapsed:.2f} seconds\n')

    if tracks:
      collection_json = ""
      
      # Save in Json
      if json_save:
        logger.info("💾 Saving data in JSON file...\n")  

        name = retry_function(extract_name, driver)
        formatted_name = retry_function(format_name, name)
        collection_json = create_json_file(tracks, tracks_url, formatted_name, platform, content_type)

      # End global timer
      end_scraping = time.perf_counter()
      scraping_elapsed = end_scraping - start_scraping
      logger.info(f'⏰ Scraping completed in {scraping_elapsed:.2f} seconds\n')

      logger.info(f"🎉 You rock, Artémis !\n")

      # Close driver
      close_driver(driver, kill_script)

      return tracks, collection_json
    
    else:
      logger.error(f"💀 Tracks scraping failed after multiple retries... \n")
      close_driver(driver)
      return None, None
    
  return None, None