import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

RATE_LIMIT = int(os.getenv("RATE_LIMIT", 2))  # Time between requests (seconds)