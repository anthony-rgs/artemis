from src.utils.logger import logger 
from src.scraper.collection_handler import scrape_collection

logger.info("🎫 Dynamic script running...\n")

logger.info("🌐 Enter the URL: ")
url = input()

print("")

scrape_collection(url)