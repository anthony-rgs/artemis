from src.utils.logger import logger 

# Check if the number of retrieved tracks matches the expected count
def check_scraped_data(tracks, count_tracks):
  logger.info("🚀 Checking scraped data...")  
  total_tracks = len(tracks)
  
  if total_tracks == count_tracks:
    logger.info(f"✅ Total tracks extracted: {total_tracks}\n")
    return True

  if total_tracks > count_tracks:
    duplicates = total_tracks - count_tracks
    logger.error(f"❌ There are {duplicates} duplicate tracks\n")
  else:
    missing_tracks = count_tracks - total_tracks
    logger.error(f"❌ {missing_tracks} tracks are missing\n")

  return False