"""
Configuration settings for Tourism Data Collector
"""
import os

# Application Settings
APP_NAME = "Tourism Data Collector"
APP_VERSION = "1.0.0"

# Database Settings
DB_PATH = os.path.join(os.path.dirname(__file__), "data", "tourism_data.db")

# AI Model Settings
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"  # Lightweight open-source model
SIMILARITY_THRESHOLD = 0.85  # For duplicate detection

# Scraping Settings
REQUEST_TIMEOUT = 10
USER_AGENT = "TourismDataCollector/1.0"
MAX_RETRIES = 3

# Export Settings
EXPORT_FOLDER = os.path.join(os.path.dirname(__file__), "exports")

# Ensure directories exist
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
os.makedirs(EXPORT_FOLDER, exist_ok=True)
