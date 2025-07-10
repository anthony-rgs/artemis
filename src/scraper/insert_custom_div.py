from src.config import CUSTOM_OVERLAY_ID
from src.utils.logger import logger 

# Insert custom div just after body
# The objective is to have a reference div to calculate the scroll position
def insert_custom_div(page):
  logger.info("🚀 Inserting custom div...")

  try:
    page.evaluate("""
      (custom_id) => {
          let body = document.body;
          let div = document.createElement('div');

          div.id = custom_id;
          div.style.position = 'relative';
          div.style.width = '10px';
          div.style.height = '10px';
          div.style.zIndex = '9999';

          body.insertBefore(div, body.firstChild);
      }
      """, 
    CUSTOM_OVERLAY_ID)

    logger.info("✅ Custom div inserted\n")

  except Exception as e:
    logger.error(f"❌ Failed to insert custom div: {e}", exc_info=True)
