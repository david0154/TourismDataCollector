# 🏨 Tourism Data Collector

**AI-Powered Tourism Data Collection & Validation System for India**

A comprehensive Windows desktop application built with **Python Tkinter** that automates the collection, validation, and management of tourism data across India using a lightweight 61MB AI model and real-time backend internet verification.

---

## ✨ Key Features

### 🤖 Lightweight AI Model (61MB)
- **Model**: `sentence-transformers/paraphrase-MiniLM-L3-v2` **(Only 61MB!)**
- ✅ **Auto-downloads on first run** from Hugging Face
- Open-source sentence transformer
- Semantic duplicate detection with 85% similarity threshold
- Fast CPU inference (no GPU required)
- Cached in `~/.cache/torch/sentence_transformers/`

### 🌐 Backend Internet Verification (No Visible Browser)
- ✅ **All verification happens in background** - no visible browser windows
- Real-time online verification of hotel/place existence
- Google Search integration for data accuracy
- Automatic rating collection from search results
- Review sentiment analysis using keyword extraction
- Price scraping from multiple online sources
- Contact number, email, and website validation

### 🗺️ How To Reach Data Collection
- Automatically extracts directions and location information
- Searches for "how to reach", "directions", "by road", "by train" keywords
- Collects nearest airport/railway station information
- Stores formatted directions in database

### ⭐ AI-Powered Rating & Review Analysis
- Sentiment analysis of hotel/place reviews
- AI-calculated ratings (0-5 stars) based on online reviews
- Positive/negative keyword detection (excellent, great vs poor, bad)
- Review count aggregation
- Price category classification (budget/moderate/expensive)

### 💰 Automated Price Collection & Tracking
- Scrapes hotel pricing from search results
- Extracts min/max/average prices in INR (₹)
- Identifies room types and rates
- Price range validation (₹500 - ₹100,000)
- Tracks price changes over time

### 🔄 Re-validation of Old Data
- **Dedicated Re-validation Tab** to update old records
- Finds records older than X days (configurable)
- Re-verifies data with current internet sources
- Updates ratings, prices, and verification status
- Maintains last_verified timestamp

### 🎨 Modern Tkinter UI (5 Tabs)
- ✅ **Built-in with Python** - no external UI frameworks needed
- Clean, professional interface
- **5 Main Tabs:**
  1. **📊 Data Collection**: Automated scraping with progress tracking
  2. **👁️ View Data**: Browse and filter collected records
  3. **📤 Export Data**: Multi-format export (JSON/Excel/CSV/XML)
  4. **✍️ Manual Entry**: Add records with AI validation
  5. **🔄 Re-validation**: Update old/unverified data
- Real-time progress bars and status updates

### 🛡️ Duplicate Detection
- Semantic similarity using AI embeddings
- Prevents redundant data entry
- Shows similarity percentage for near-duplicates
- Configurable threshold (default 85%)

### 💾 SQLite Database
- Lightweight embedded database
- Tables: Hotels, Tourist Places, Travel Services
- Fields include: how_to_reach, price_min/max/avg, timings, entry_fee
- Timestamped records with last_verified field

### 📤 Multi-Format Export
- **JSON**: Clean structured data
- **Excel (XLSX)**: Formatted spreadsheets
- **CSV**: Universal compatibility
- **XML**: Legacy system support

---

## 📋 System Requirements

- **OS**: Windows 10/11 (64-bit)
- **Python**: 3.8 or higher
- **RAM**: 4GB minimum (8GB recommended)
- **Disk Space**: 2GB (for AI model cache)
- **Internet**: Required for online verification and model download

---

## 🚀 Installation

### Step 1: Clone Repository
```bash
git clone https://github.com/david0154/TourismDataCollector.git
cd TourismDataCollector
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
venv\\Scripts\\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

**Note**: First run will auto-download the 61MB AI model from Hugging Face.

### Step 4: Run Application
```bash
python main.py
```

**On first run**, you'll see:
```
🤖 Initializing AI Model: sentence-transformers/paraphrase-MiniLM-L3-v2
📥 Downloading model if not cached (61MB - one-time only)...
✅ AI Model loaded successfully!
```

---

## 📖 Usage Guide

### Tab 1: 📊 Data Collection

**Automated Data Scraping with Backend Verification**:

1. Select **State** (or "All India")
2. Choose **City/Tourist Place** (or "All Places")
3. Select **Data Type** (Hotels/Tourist Places/etc.)
4. Click **🚀 Start Collection**
5. Monitor progress - backend verification runs invisibly

**What Happens During Collection**:
- Searches Google in background (no visible browser)
- Extracts ratings, reviews, prices
- Collects "how to reach" information
- Validates data using AI
- Checks for duplicates
- Saves to database with verification timestamp

### Tab 2: 👁️ View Data

**Browse Collected Records**:
- Filter by **Data Type** (Hotels/Tourist Places/etc.)
- Filter by **State**
- View details in sortable table:
  - ID, Name, City, State
  - Contact, Rating, Price (Min/Max/Avg)
  - Verified Status, Last Verified Date
- See total record count

### Tab 3: 📤 Export Data

**Export to Multiple Formats**:
1. Select **Export Format** (JSON/Excel/CSV/XML)
2. Choose **Data Type** to export
3. Click **💾 Export Data**
4. Choose save location
5. Review export log

### Tab 4: ✍️ Manual Entry

**Add Records Manually with AI Validation**:
1. Fill in details:
   - Hotel/Place Name
   - Address, City, State
   - Contact, Email, Website
   - Price (for hotels)
2. Click **✅ Add with AI Validation**
3. System will:
   - Validate all fields
   - Verify online using backend
   - Check for duplicates using AI
   - Collect rating and pricing
   - Scrape "how to reach" info
   - Save to database

### Tab 5: 🔄 Re-validation

**Update Old/Unverified Data**:
1. Set **Days threshold** (e.g., 30 days)
2. Click **🔍 Find Old Records**
3. View list of records needing re-validation
4. Click **🔄 Re-validate Selected** or **Re-validate All**
5. System will:
   - Re-verify each record online
   - Update ratings and prices
   - Refresh "how to reach" information
   - Update last_verified timestamp

---

## 🤖 AI Model Details

### Lightweight Sentence Transformer
**Model**: `sentence-transformers/paraphrase-MiniLM-L3-v2`

**Specifications**:
- **Size**: 61MB (well under 500MB requirement ✅)
- **Type**: Sentence embeddings
- **Architecture**: 6-layer MiniLM
- **Dimensions**: 384
- **Speed**: ~2000 sentences/second on CPU
- **Source**: [Hugging Face](https://huggingface.co/sentence-transformers/paraphrase-MiniLM-L3-v2)
- **License**: Apache 2.0 (Open Source)

**Use Cases**:
1. **Duplicate Detection**: Semantic comparison of hotel names/addresses
2. **Similarity Matching**: Find near-duplicate records
3. **Data Clustering**: Group similar records

**Auto-Download Process**:
- On first run, downloads from Hugging Face
- Cached in `~/.cache/torch/sentence_transformers/`
- No manual download required
- Shows progress during download

---

## 🌐 Backend Internet Verification

### How It Works

**No Visible Browser**:
- All HTTP requests happen in background
- Uses `requests` library with session management
- No Selenium or browser automation
- Fast and lightweight

### Data Sources
1. **Google Search**: Hotel/place existence and ratings
2. **Web Scraping**: Review sentiment and pricing
3. **Pattern Matching**: Extract structured data

### Verification Process
```
Input → Google Search (Backend) → Parse HTML → Extract Data →
Rating Analysis → Price Scraping → How To Reach → Sentiment Analysis →
Validate → Save to Database
```

### What Gets Verified
- ✅ Entity existence online
- ✅ Star rating (0-5 from reviews)
- ✅ Price range in INR (₹ min/max/avg)
- ✅ Contact number format (Indian)
- ✅ Email validity
- ✅ Website accessibility
- ✅ Review sentiment (positive/negative/neutral)
- ✅ How to reach / directions
- ✅ Entry fees (for tourist places)
- ✅ Timings (for tourist places)
- ✅ Best season to visit

---

## 📁 Project Structure

```
TourismDataCollector/
├── main.py                    # Tkinter application entry
├── config.py                  # Settings (model, thresholds)
├── requirements.txt           # Dependencies
├── README.md                  # This file
├── LICENSE                    # MIT License
├── .gitignore                # Git ignore rules
│
├── database/
│   ├── __init__.py
│   ├── db_manager.py         # SQLite with re-validation
│   └── models.py             # Data models
│
├── scrapers/
│   ├── __init__.py
│   ├── web_scraper.py        # BeautifulSoup utilities
│   └── data_collector.py     # Collection logic
│
├── ai/
│   ├── __init__.py
│   ├── data_validator.py     # Backend internet verification
│   └── deduplicator.py       # AI duplicate detection (61MB)
│
├── ui/
│   ├── __init__.py
│   └── main_window.py        # Tkinter UI (5 tabs)
│
├── utils/
│   ├── __init__.py
│   ├── india_data.py         # 36 states + tourist places
│   └── exporters.py          # JSON/Excel/CSV/XML
│
├── data/
│   └── tourism_data.db       # SQLite database (auto-created)
│
└── exports/
    └── (exported files)
```

---

## 🗃️ Database Schema

### Hotels Table
```sql
CREATE TABLE hotels (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    address TEXT,
    city TEXT NOT NULL,
    state TEXT NOT NULL,
    contact TEXT,
    email TEXT,
    website TEXT,
    rating REAL DEFAULT 0.0,
    price_min INTEGER DEFAULT 0,
    price_max INTEGER DEFAULT 0,
    price_avg INTEGER DEFAULT 0,
    room_types TEXT,
    amenities TEXT,
    verified INTEGER DEFAULT 0,
    last_verified TIMESTAMP,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

### Tourist Places Table
```sql
CREATE TABLE tourist_places (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    city TEXT NOT NULL,
    state TEXT NOT NULL,
    category TEXT,
    entry_fee INTEGER,
    timings TEXT,
    best_season TEXT,
    how_to_reach TEXT,
    nearby_attractions TEXT,
    latitude REAL,
    longitude REAL,
    verified INTEGER DEFAULT 0,
    last_verified TIMESTAMP,
    created_at TIMESTAMP
);
```

---

## ⚙️ Configuration

Edit `config.py`:

```python
# AI Model (Must be under 500MB)
MODEL_NAME = "sentence-transformers/paraphrase-MiniLM-L3-v2"  # 61MB
SIMILARITY_THRESHOLD = 0.85  # Duplicate detection threshold

# Internet Verification
ENABLE_ONLINE_VERIFICATION = True
GOOGLE_SEARCH_ENABLED = True
MAX_SEARCH_RESULTS = 5

# Scraping
REQUEST_TIMEOUT = 10
MAX_RETRIES = 3
USER_AGENT = "Mozilla/5.0..."

# Rating & Reviews
MIN_RATING = 0.0
MAX_RATING = 5.0
ENABLE_REVIEW_ANALYSIS = True

# Database
DB_PATH = "data/tourism_data.db"

# Export
EXPORT_FOLDER = "exports/"
```

---

## 🐛 Troubleshooting

### AI Model Download Issues
**Problem**: Model download fails

**Solution**:
- Check internet connection
- Ensure 2GB free disk space
- Try manually: `python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('sentence-transformers/paraphrase-MiniLM-L3-v2')"`
- Check Hugging Face status: https://status.huggingface.co/

### Internet Verification Fails
**Problem**: "Backend verification failed"

**Solution**:
- Check internet connectivity
- Verify firewall/proxy settings
- Google may block excessive requests - add delays
- Try disabling temporarily: `ENABLE_ONLINE_VERIFICATION = False`

### Tkinter Not Found
**Problem**: "No module named 'tkinter'"

**Solution**:
- Tkinter is built-in with Python
- Reinstall Python with "tcl/tk" checkbox enabled
- Windows: Usually pre-installed
- Linux: `sudo apt-get install python3-tk`

### Database Locked
**Problem**: "Database is locked"

**Solution**:
- Close all app instances
- Delete `tourism_data.db.lock` if exists
- Restart application

---

## 🎯 Features Checklist

| Feature | Status | Details |
|---------|--------|---------|
| UI Framework | ✅ Tkinter | Built-in with Python |
| AI Model Size | ✅ 61MB | Under 500MB limit |
| Auto Model Download | ✅ First Run | From Hugging Face |
| Backend Verification | ✅ Enabled | No visible browser |
| Rating Analysis | ✅ AI-Powered | Sentiment from reviews |
| Price Collection | ✅ Automated | Min/Max/Avg in INR |
| How To Reach | ✅ Collected | Directions from web |
| Re-validation | ✅ Dedicated Tab | Update old data |
| Duplicate Detection | ✅ AI-Based | 85% similarity |
| Export Formats | ✅ 4 Types | JSON/Excel/CSV/XML |
| Database | ✅ SQLite | Embedded |
| Tourist Places | ✅ Supported | Timings, fees, seasons |

---

## 📦 Dependencies

```txt
# AI Model (61MB)
sentence-transformers==2.2.2
torch==2.1.2
transformers==4.36.2

# Web Scraping (Backend)
beautifulsoup4==4.12.2
requests==2.31.0
lxml==4.9.3

# Data Processing
pandas==2.1.4
numpy==1.26.2

# Validation
validators==0.22.0

# Export
openpyxl==3.1.2
xlsxwriter==3.1.9

# UI
tkinter  # Built-in with Python
```

---

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create feature branch (`git checkout -b feature/NewFeature`)
3. Commit changes (`git commit -m 'Add NewFeature'`)
4. Push to branch (`git push origin feature/NewFeature`)
5. Open Pull Request

---

## 📄 License

**MIT License** - See [LICENSE](LICENSE) file

---

## 👨‍💻 Author

**David**  
**Nexuzy Tech Pvt Ltd**

- 📧 Email: support@davidk.online
- 🌐 Website: [davidk.online](https://davidk.online)
- 📍 Location: Kolkata, West Bengal, India
- 💼 GitHub: [@david0154](https://github.com/david0154)

---

## 🙏 Acknowledgments

- **Sentence Transformers** by UKPLab
- **PyTorch** for AI inference
- **BeautifulSoup** for web scraping
- **Tkinter** for GUI
- **Hugging Face** for model hosting
- Open-source community

---

## 📊 Project Stats

- **Version**: 1.0.0
- **Status**: ✅ Active Development
- **Last Updated**: January 2026
- **Python**: 3.8+ Required
- **Platform**: Windows 10/11
- **AI Model**: 61MB (paraphrase-MiniLM-L3-v2)
- **Database**: SQLite
- **UI**: Tkinter (5 Tabs)

---

**⭐ Star this repo if you find it useful!**

**📢 Report bugs or request features via [Issues](https://github.com/david0154/TourismDataCollector/issues)**

---

*Built with ❤️ for the Indian tourism industry*
