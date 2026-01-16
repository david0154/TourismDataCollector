"""
Configuration settings for Tourism Data Collector
AI model auto-downloads on first run
"""
import os

# Application Settings
APP_NAME = "Tourism Data Collector"
APP_VERSION = "1.0.0"

# Database Settings
DB_PATH = os.path.join(os.path.dirname(__file__), "data", "tourism_data.db")

# AI Model Settings - AUTO DOWNLOAD ON FIRST RUN
MODEL_NAME = "sentence-transformers/paraphrase-MiniLM-L3-v2"  # 61MB
SIMILARITY_THRESHOLD = 0.85
AUTO_DOWNLOAD_MODEL = True  # Automatically download model on first run

# Internet Validation - DuckDuckGo + Google
ENABLE_ONLINE_VERIFICATION = True
USE_DUCKDUCKGO = True  # DuckDuckGo for privacy-focused validation
USE_GOOGLE_SEARCH = True  # Google as fallback
MAX_SEARCH_RESULTS = 5

# Scraping Settings
REQUEST_TIMEOUT = 10
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
MAX_RETRIES = 3
SCRAPING_DELAY = 2  # Delay between requests in seconds

# Data Revalidation Settings
ENABLE_AUTO_REVALIDATION = True
REVALIDATION_INTERVAL_DAYS = 7  # Revalidate old data every 7 days
REVALIDATION_ON_STARTUP = False  # Set True to revalidate on every startup

# Rating & Review Settings
MIN_RATING = 0.0
MAX_RATING = 5.0
ENABLE_REVIEW_ANALYSIS = True

# Travel & Destination Data
COLLECT_TRAVEL_ROUTES = True  # How to reach destinations
COLLECT_TRANSPORT_OPTIONS = True  # Bus, train, flight info
COLLECT_DISTANCES = True  # Distance from major cities

# Price Update Settings
AUTO_UPDATE_PRICES = True  # Update prices from internet
PRICE_UPDATE_INTERVAL_DAYS = 7  # Update prices weekly

# Export Settings
EXPORT_FOLDER = os.path.join(os.path.dirname(__file__), "exports")

# Ensure directories exist
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
os.makedirs(EXPORT_FOLDER, exist_ok=True)
