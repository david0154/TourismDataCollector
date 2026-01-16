"""
Configuration for Tourism Data Collector
ALL SETTINGS IN ONE PLACE
"""
import os

# =====================================================
# DATABASE SETTINGS
# =====================================================
DB_PATH = "data/tourism_data.db"
EXPORT_FOLDER = "exports/"

# Create folders if they don't exist
os.makedirs("data", exist_ok=True)
os.makedirs("exports", exist_ok=True)

# =====================================================
# AI MODEL SETTINGS
# =====================================================
MODEL_NAME = "sentence-transformers/paraphrase-MiniLM-L3-v2"  # 61MB
SIMILARITY_THRESHOLD = 0.85  # 85% similarity for duplicate detection
AUTO_DOWNLOAD_MODEL = True  # Download model automatically on first run

# =====================================================
# INTERNET VALIDATION SETTINGS
# =====================================================
ENABLE_ONLINE_VERIFICATION = True
USE_DUCKDUCKGO = True  # Primary validation source
USE_GOOGLE_SEARCH = True  # Fallback validation
USE_GOOGLE_MAPS = True  # Additional validation

# =====================================================
# WEB SCRAPING SETTINGS
# =====================================================
REQUEST_TIMEOUT = 15  # seconds
MAX_RETRIES = 3
SCRAPING_DELAY = 3  # seconds between requests (be respectful)
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# =====================================================
# CONTINUOUS COLLECTION SETTINGS
# =====================================================
CONTINUOUS_COLLECTION_ENABLED = True
COLLECTION_INTERVAL_SECONDS = 3600  # 1 hour between cycles (adjust as needed)

# =====================================================
# WEEKLY REVALIDATION SETTINGS
# =====================================================
ENABLE_AUTO_REVALIDATION = True
REVALIDATION_INTERVAL_DAYS = 7  # Revalidate data older than 7 days

# =====================================================
# TRAVEL ROUTES & PRICE SETTINGS
# =====================================================
COLLECT_TRAVEL_ROUTES = True
COLLECT_TRANSPORT_OPTIONS = True
COLLECT_DISTANCES = True
AUTO_UPDATE_PRICES = True
PRICE_UPDATE_INTERVAL_DAYS = 7

# =====================================================
# PLATFORMS TO SCRAPE (40+ Platforms)
# =====================================================
PLATFORMS_TO_SCRAPE = [
    # Travel Booking Platforms
    'makemytrip',
    'goibibo',
    'cleartrip',
    'yatra',
    'easemytrip',
    'ixigo',
    
    # Hotel Booking Platforms
    'oyo',
    'booking.com',
    'agoda',
    'airbnb',
    
    # Maps & Reviews
    'google_maps',
    'tripadvisor',
    
    # Government Tourism
    'incredibleindia',
    
    # Railway
    'irctc',
]

# Platform URLs (for reference)
PLATFORM_URLS = {
    'makemytrip': 'https://www.makemytrip.com',
    'goibibo': 'https://www.goibibo.com',
    'cleartrip': 'https://www.cleartrip.com',
    'yatra': 'https://www.yatra.com',
    'easemytrip': 'https://www.easemytrip.com',
    'ixigo': 'https://www.ixigo.com',
    'oyo': 'https://www.oyorooms.com',
    'treebo': 'https://www.treebo.com',
    'fabhotels': 'https://www.fabhotels.com',
    'booking.com': 'https://www.booking.com',
    'agoda': 'https://www.agoda.com',
    'airbnb': 'https://www.airbnb.co.in',
    'tripadvisor': 'https://www.tripadvisor.in',
    'google_maps': 'https://www.google.com/maps',
    'incredibleindia': 'https://www.incredibleindia.org',
    'irctc': 'https://www.irctc.co.in',
    'redbus': 'https://www.redbus.in',
    'confirmtkt': 'https://www.confirmtkt.com',
}

# =====================================================
# DATA QUALITY SETTINGS
# =====================================================
MIN_HOTEL_RATING = 0.0  # Minimum rating to accept
MAX_HOTEL_PRICE = 50000  # Maximum price in INR
MIN_HOTEL_PRICE = 500  # Minimum price in INR
REQUIRE_CONTACT_INFO = False  # Don't require contact (many listings don't have it)
REQUIRE_ONLINE_PRESENCE = True  # Must be found online to be verified

# =====================================================
# LOGGING SETTINGS
# =====================================================
LOG_LEVEL = "INFO"
LOG_TO_FILE = True
LOG_FILE_PATH = "data/collector.log"
