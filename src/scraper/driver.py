from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from src.config import SELENIUM_OPTIONS, SELENIUM_TIMEOUT 
from src.utils.logger import logger 

# Initializes and returns a Selenium WebDriver instance with the options defined in config.py
def init_driver():
  try:
    logger.info("🚀 Init WebDriver started")

    # Configuration of browser options
    options = webdriver.ChromeOptions()

    if SELENIUM_OPTIONS["headless"]:
      options.add_argument("--headless=new") 
    if SELENIUM_OPTIONS["disable_gpu"]:
      options.add_argument("--disable-gpu")
    if SELENIUM_OPTIONS["no_sandbox"]:
      options.add_argument("--no-sandbox")
    if SELENIUM_OPTIONS.get("disable_dev_shm_usage"):
      options.add_argument("--disable-dev-shm-usage")
    if SELENIUM_OPTIONS['window_size']:
      options.add_argument(f"--window-size={SELENIUM_OPTIONS['window_size']}")
    
    # Driver initialization
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.implicitly_wait(SELENIUM_TIMEOUT) # Waiting for driver

    logger.info("✅ WebDriver successfully launched\n")
    return driver

  except Exception as e:
    logger.error(f"❌ Error during browser initialization: {e}")
    return None
  
# Close the connection with the driver
def close_driver(driver):
  driver.quit()
  logger.info("💤 Closing the connection with the driver\n")
