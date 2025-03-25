from src.utils.logger import logger 
from src.scraper.collection_handler import scrape_collection

# Dynamic scraper script
def dynamic_scaper():
  logger.info("🎫 Dynamic script running...\n")

  logger.info("🌐 Enter the URL: ")
  url = input()

  print("")

  scrape_collection(url)


dynamic_scaper()