from src.config import SPOTIFY_BILLION_CLUB_URL
from src.utils.logger import logger 
from src.scraper.collection_handler import scrape_collection

url = SPOTIFY_BILLION_CLUB_URL

logger.info("💎 Billion club script running...\n")

scrape_collection(url)