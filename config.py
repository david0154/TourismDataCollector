"""
Configuration settings for Tourism Data Collector
"""
import os

# Application Settings
APP_NAME = "Tourism Data Collector"
APP_VERSION = "1.0.0"

# Database Settings
DB_PATH = os.path.join(os.path.dirname(__file__), "data", "tourism_data.db")

# AI Model Settings - Lightweight model under 500MB
MODEL_NAME = "sentence-transformers/paraphrase-MiniLM-L3-v2"  # Only 61MB!
SIMILARITY_THRESHOLD = 0.85  # For duplicate detection

# Internet Search Settings
ENABLE_ONLINE_VERIFICATION = True
GOOGLE_SEARCH_ENABLED = True
MAX_SEARCH_RESULTS = 5

# Scraping Settings
REQUEST_TIMEOUT = 10
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
MAX_RETRIES = 3

# Rating & Review Settings
MIN_RATING = 0.0
MAX_RATING = 5.0
ENABLE_REVIEW_ANALYSIS = True

# Export Settings
EXPORT_FOLDER = os.path.join(os.path.dirname(__file__), "exports")

# Ensure directories exist
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
os.makedirs(EXPORT_FOLDER, exist_ok=True)
