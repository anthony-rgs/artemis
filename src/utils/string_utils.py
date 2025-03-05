import re
from src.utils.logger import logger

# Formats a collection name by removing emojis and replacing spaces with hyphens
def format_name(name):
  logger.info("🚀 Formating name...")

  emoji_pattern = re.compile(
    "["
    "\U0001F600-\U0001F64F"  # Emoticons  
    "\U0001F300-\U0001F5FF"  # Symbols & pictograms  
    "\U0001F680-\U0001F6FF"  # Transport & map symbols  
    "\U0001F700-\U0001F77F"  # Alchemical symbols  
    "\U0001F780-\U0001F7FF"  # Miscellaneous symbols  
    "\U0001F800-\U0001F8FF"  # More miscellaneous symbols  
    "\U0001F900-\U0001F9FF"  # Supplemental emojis  
    "\U0001FA00-\U0001FA6F"  # Additional symbols  
    "\U0001FA70-\U0001FAFF"  # More additional symbols  
    "\U00002702-\U000027B0"  # Dingbats  
    "\U000024C2-\U0001F251"  # Enclosed characters  
    "]+", flags=re.UNICODE
  )
    
  name_clean = emoji_pattern.sub(r'', name).strip()
  name_formatted = name_clean.replace(" ", "-").lower()
  
  if len(name_formatted) == 0:
    name_formatted = "no-collection-name"

  logger.info(f"✅ Formatted name: {name_formatted}\n")

  return name_formatted