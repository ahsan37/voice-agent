import os
import logging
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

load_dotenv()

def main():
    
    # Retrieve a test environment variable (e.g., LIVEKIT_URL)
    livekit_url = os.getenv("LIVEKIT_URL")
    if not livekit_url:
        logging.error("LIVEKIT_URL is not set in the .env file!")
    else:
        logging.info(f"Successfully loaded LIVEKIT_URL: {livekit_url}")

    # You can add additional tests or log statements here as needed.
    logging.info("Project environment is set up correctly.")

if __name__ == "__main__":
    main()