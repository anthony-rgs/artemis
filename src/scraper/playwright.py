import sys

from playwright.sync_api import sync_playwright

from src.config import PLAYWRIGHT_OPTIONS, PLAYWRIGHT_TIMEOUT
from src.utils.logger import logger

# Initialize and return a Playwright page, along with the browser and Playwright context
def launch_playwright():
  try:
    logger.info("🚀 Init Playwright started")

    # Start Playwright (context management)
    playwright = sync_playwright().start()

    # Prepare Chromium arguments according to configured options
    args = []
    if PLAYWRIGHT_OPTIONS.get("disable_gpu"):
      args.append("--disable-gpu")
    if PLAYWRIGHT_OPTIONS.get("no_sandbox"):
      args.append("--no-sandbox")
    if PLAYWRIGHT_OPTIONS.get("disable_dev_shm_usage"):
      args.append("--disable-dev-shm-usage")
    if PLAYWRIGHT_OPTIONS.get("window_size"):
      args.append(f"--window-size={PLAYWRIGHT_OPTIONS['window_size']}")

    # Launch the Chromium browser
    browser = playwright.chromium.launch(
      headless=PLAYWRIGHT_OPTIONS.get("headless", True),
      args=args
    )

    # Create a new page (tab)
    page = browser.new_page()

    # Set the default timeout for all actions (in ms)
    page.set_default_timeout(PLAYWRIGHT_TIMEOUT * 1000)  # Convert seconds to ms

    logger.info("✅ Playwright browser launched\n")

    # Return the page, browser, and Playwright context (to allow proper closing)
    return page, browser, playwright

  except Exception as e:
    logger.error(f"❌ Error during Playwright initialization: {e}", exc_info=True)
    return None, None, None


# Close the connection with the Playwright browser
def close_playwright(page, browser, playwright, kill_script=True):
  try:
    if page:
      page.close()
    if browser:
      browser.close()
    if playwright:
      playwright.stop()
      
    logger.info("💤 Playwright browser closed properly\n")

  except Exception as e:
      logger.error(f"❌ Error closing Playwright: {e}", exc_info=True)

  if kill_script:
    sys.exit(1)  # kill script


# Create new context and page 
def create_context_and_page(browser):
  context = browser.new_context()
  page = context.new_page()
  return context, page


# Close context and page 
def close_context_and_page(context, page):
  context.close()
  page.close()