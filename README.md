# 🏨 Tourism Data Collector

**AI-Powered Tourism Data Collection & Validation System for India**

A comprehensive Windows desktop application built with **Python Tkinter** that automates the collection, validation, and management of tourism data across India using lightweight AI models (61MB) and real-time internet verification.

---

## ✨ Key Features

### 🤖 Lightweight AI Model - AUTO DOWNLOAD (Under 500MB)
- **Model**: `sentence-transformers/paraphrase-MiniLM-L3-v2` **(Only 61MB!)**
- **Auto-downloads** from Hugging Face on first run
- Open-source, no API keys required
- Semantic duplicate detection with 85% similarity threshold
- Fast CPU inference (no GPU needed)
- Progress messages during download

### 🌐 Internet-Based Validation (Backend Only)
- **DuckDuckGo Search** (primary - privacy-focused, no tracking)
- **Google Search** (fallback for additional validation)
- **NO browser windows** - backend scraping only using `requests` + `BeautifulSoup`
- Real-time hotel rating extraction from search results
- Review sentiment analysis (positive/negative/neutral)
- Automatic price collection in INR (₹)
- Contact, email, and website validation

### 🗓️ Weekly Automatic Revalidation
- Automatically finds data older than 7 days
- Re-validates hotels via DuckDuckGo + Google
- Updates ratings, prices, and verification status
- Tracks validation history in audit log
- Configurable interval (default: 7 days)
- Manual revalidation button in UI

### 🗺️ Travel Routes Collection ("How to Reach")
- **By Air**: Nearest airports
- **By Train**: Railway stations
- **By Road**: Highway routes
- **Distances**: From major cities (in km)
- Stored with tourist places in database
- Scraped from internet search results

### 💰 Automated Price Updates
- Scrapes hotel pricing from multiple online sources
- Extracts min/max/average prices
- Currency: INR (₹)
- Validates range: ₹500 - ₹50,000
- Weekly automatic updates
- Timestamp tracking

### 🎨 Modern Tkinter UI (Built-in with Python)
- Clean, professional interface
- **4 Main Tabs**:
  1. **📊 Data Collection**: Automated scraping with progress tracking
  2. **👁️ View Data**: Browse/filter collected records with validation status
  3. **📤 Export Data**: Multi-format export (JSON/Excel/CSV/XML)
  4. **✍️ Manual Entry**: Add hotels with AI validation & duplicate check
- Real-time progress bars
- Status notifications
- No external UI framework dependencies

### 🛡️ AI-Powered Duplicate Detection
- Semantic similarity using sentence embeddings
- 85% similarity threshold (configurable)
- Shows similarity percentage for near-duplicates
- Prevents redundant data entry

### 💾 SQLite Database with Validation Tracking
- Lightweight embedded database
- Tables: Hotels, Tourist Places, Travel Services, Validation Log
- `last_validated_at` timestamp for each record
- `validation_source` tracking (DuckDuckGo/Google/Manual)
- Optimized indexes for fast queries

### 📤 Multi-Format Export
- **JSON**: Structured data with proper encoding
- **Excel (XLSX)**: Formatted spreadsheets
- **CSV**: Universal compatibility
- **XML**: Legacy system support
- Export log with timestamps

---

## 📋 System Requirements

- **OS**: Windows 10/11 (64-bit)
- **Python**: 3.8 or higher
- **RAM**: 4GB minimum (8GB recommended)
- **Disk Space**: 2GB (for AI model cache + data)
- **Internet**: Required for validation and AI model download

---

## 🚀 Quick Start Installation

### Step 1: Clone Repository
```bash
git clone https://github.com/david0154/TourismDataCollector.git
cd TourismDataCollector
```

### Step 2: Create Virtual Environment (Recommended)
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

**Note**: On first run, the 61MB AI model will download automatically from Hugging Face (one-time only).

### Step 4: Run Application
```bash
python main.py
```

**Expected Console Output**:
```
============================================================
🚀 Starting Tourism Data Collector
============================================================

✅ Database connected: data/tourism_data.db
✅ Auto-revalidation enabled (every 7 days)

📥 Loading AI Model (auto-download if needed)...

============================================================
🤖 Initializing AI Model: sentence-transformers/paraphrase-MiniLM-L3-v2
============================================================
📥 Model will download automatically if not present...
🌐 Source: Hugging Face (Open Source)
💾 Size: ~61MB (one-time download)
⏳ Please wait...

✅ AI Model loaded successfully!
✅ Model: sentence-transformers/paraphrase-MiniLM-L3-v2
✅ Size: 61MB
✅ Ready for duplicate detection!
============================================================

✅ All systems ready!
============================================================
```

---

## 📖 Usage Guide

### 1. 📊 Data Collection Tab

**Automated Scraping with AI Validation**:

1. Select **State** (or "All India")
2. Choose **City/Tourist Place** (or "All Places")
3. Select **Data Type** (Hotels/Tourist Places/Travel Services)
4. Click **🚀 Start Collection**
5. Monitor real-time progress:
   - 🔍 Searching
   - 🤖 AI validation
   - 🌐 DuckDuckGo verification
   - 💾 Database save

**Revalidate Old Data**:
- Click **🔄 Revalidate Old Data**
- System finds records older than 7 days
- Re-validates via DuckDuckGo + Google
- Updates ratings, prices, verification status

### 2. 👁️ View Data Tab

**Browse Collected Records**:
- Filter by **Data Type** (Hotels/Tourist Places/Travel Services)
- Filter by **State**
- Click **🔄 Refresh** to update table
- View columns:
  - ID, Name, City, State
  - Contact, Rating (⭐), Price (₹)
  - Verified Status (✓/✗)
  - Last Validated Date

### 3. 📤 Export Data Tab

**Export to Multiple Formats**:
1. Select **Export Format** (JSON/Excel/CSV/XML)
2. Choose **Data Type** to export
3. Click **💾 Export Data**
4. Choose save location
5. Review export log with timestamps

### 4. ✍️ Manual Entry Tab

**Add Hotels with AI Validation**:
1. Fill in hotel details:
   - Hotel Name, Address, City, State
   - Contact, Email, Website
   - Price (₹ per night)
2. Click **✅ Add with AI Validation**
3. System will:
   - Validate all fields (phone, email format)
   - Verify hotel via **DuckDuckGo**
   - Extract rating and reviews
   - Check for **duplicates using AI** (85% threshold)
   - Save to database with validation metadata

---

## 🤖 AI Model Details

### Lightweight Sentence Transformer

**Model**: `sentence-transformers/paraphrase-MiniLM-L3-v2`

| Specification | Value |
|--------------|-------|
| **Size** | 61MB (under 500MB ✅) |
| **Type** | Sentence embeddings |
| **Architecture** | 6-layer MiniLM |
| **Embedding Dimensions** | 384 |
| **Speed** | ~2000 sentences/sec (CPU) |
| **Source** | Hugging Face (MIT License) |
| **Download** | Automatic on first run |
| **GPU** | Not required |

**Use Cases**:
1. **Duplicate Detection**: Semantic comparison of hotel names, addresses, locations
2. **Similar Record Search**: Find related hotels across database
3. **Data Clustering**: Group similar tourism services

**Why This Model?**
- ✅ Extremely lightweight (61MB vs typical 400MB+ models)
- ✅ Runs efficiently on CPU without GPU
- ✅ Perfect for Windows desktop applications
- ✅ Open-source, no API costs
- ✅ Auto-downloads from Hugging Face

---

## 🌐 Internet Validation System

### Data Sources (Backend Only)

1. **DuckDuckGo HTML Search** (Primary)
   - Privacy-focused (no user tracking)
   - No API key required
   - Extracts ratings, reviews, prices from snippets
   - Regex pattern matching for data extraction

2. **Google Search** (Fallback)
   - Used when DuckDuckGo doesn't find results
   - More comprehensive data
   - Secondary validation

### Validation Workflow

```
User Input
    ↓
Field Validation (phone, email, URL formats)
    ↓
DuckDuckGo Search (hotel name + city + state)
    ↓
Extract: Rating, Reviews Count, Price Range
    ↓
If Not Found → Google Search Fallback
    ↓
Sentiment Analysis (positive/negative keywords)
    ↓
Travel Routes Extraction (how to reach)
    ↓
AI Duplicate Detection (semantic similarity)
    ↓
Database Save with Validation Metadata
```

### What Gets Verified?

- ✅ Hotel existence online
- ✅ Star rating (0.0 - 5.0)
- ✅ Review count
- ✅ Price range (₹ INR)
- ✅ Contact number format (Indian: 6-9 prefix, 10 digits)
- ✅ Email validity (RFC 5322 pattern)
- ✅ Website accessibility (HTTP status check)
- ✅ Review sentiment (positive/negative/neutral)
- ✅ Travel routes (air/train/road)

---

## 📁 Project Structure

```
TourismDataCollector/
├── main.py                         # Tkinter application entry point
├── config.py                       # All settings (AI, validation, revalidation)
├── requirements.txt                # Python dependencies
├── README.md                       # This documentation
├── LICENSE                         # MIT License
├── .gitignore                      # Git ignore rules
│
├── ai/
│   ├── __init__.py
│   ├── data_validator.py          # DuckDuckGo + Google validation
│   │                              # Travel routes, price scraping
│   │                              # Review analysis, revalidation checks
│   └── deduplicator.py            # AI model auto-download
│                                  # Semantic duplicate detection
│
├── database/
│   ├── __init__.py
│   └── db_manager.py              # SQLite operations
│                                  # Revalidation queries
│                                  # Validation logging
│
├── scrapers/
│   ├── __init__.py
│   └── web_scraper.py             # Backend scraping (no browser)
│                                  # Requests + BeautifulSoup
│
├── ui/
│   ├── __init__.py
│   └── main_window.py             # Complete Tkinter UI (4 tabs)
│                                  # Progress tracking
│                                  # Revalidation button
│
├── utils/
│   ├── __init__.py
│   ├── india_data.py              # 36 Indian states + tourist places
│   └── exporters.py               # JSON/Excel/CSV/XML exporters
│
├── data/
│   └── tourism_data.db            # SQLite database (auto-created)
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
    pincode TEXT,
    contact TEXT,
    email TEXT,
    website TEXT,
    rating REAL DEFAULT 0.0,
    price INTEGER DEFAULT 0,
    room_types TEXT,
    amenities TEXT,
    verified INTEGER DEFAULT 0,
    last_validated_at TEXT,              -- 🆕 For revalidation
    validation_source TEXT,              -- DuckDuckGo/Google/Manual
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
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
    latitude REAL,
    longitude REAL,
    how_to_reach_air TEXT,               -- 🆕 JSON array
    how_to_reach_train TEXT,             -- 🆕 JSON array
    how_to_reach_road TEXT,              -- 🆕 JSON array
    distances TEXT,                      -- 🆕 JSON object
    verified INTEGER DEFAULT 0,
    last_validated_at TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);
```

### Validation Log Table
```sql
CREATE TABLE validation_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    table_name TEXT NOT NULL,            -- hotels/tourist_places
    record_id INTEGER NOT NULL,
    validation_type TEXT,                -- initial/revalidation/manual
    result TEXT,                         -- success/failed/error
    validated_at TEXT DEFAULT CURRENT_TIMESTAMP
);
```

---

## ⚙️ Configuration

Edit `config.py` to customize:

```python
# AI Model - Auto Download
MODEL_NAME = "sentence-transformers/paraphrase-MiniLM-L3-v2"  # 61MB
SIMILARITY_THRESHOLD = 0.85
AUTO_DOWNLOAD_MODEL = True  # Download on first run

# Internet Validation
ENABLE_ONLINE_VERIFICATION = True
USE_DUCKDUCKGO = True  # Primary validation
USE_GOOGLE_SEARCH = True  # Fallback

# Scraping
REQUEST_TIMEOUT = 10
MAX_RETRIES = 3
SCRAPING_DELAY = 2  # Seconds between requests

# Weekly Revalidation
ENABLE_AUTO_REVALIDATION = True
REVALIDATION_INTERVAL_DAYS = 7  # Check data older than 7 days

# Travel Routes
COLLECT_TRAVEL_ROUTES = True
COLLECT_TRANSPORT_OPTIONS = True
COLLECT_DISTANCES = True

# Price Updates
AUTO_UPDATE_PRICES = True
PRICE_UPDATE_INTERVAL_DAYS = 7

# Database & Export
DB_PATH = "data/tourism_data.db"
EXPORT_FOLDER = "exports/"
```

---

## 🐛 Troubleshooting

### AI Model Download Issues

**Problem**: Model download fails

**Solution**:
1. Check internet connection
2. Ensure 2GB free disk space
3. Check firewall/antivirus settings
4. Try manual download:
   ```python
   from sentence_transformers import SentenceTransformer
   model = SentenceTransformer('paraphrase-MiniLM-L3-v2')
   ```

### Internet Verification Errors

**Problem**: "DuckDuckGo verification failed"

**Solution**:
1. Check internet connectivity
2. Verify firewall allows Python outbound connections
3. Try disabling temporarily:
   ```python
   # In config.py
   ENABLE_ONLINE_VERIFICATION = False
   ```

### Database Locked

**Problem**: "Database is locked"

**Solution**:
1. Close all instances of the application
2. Delete `data/tourism_data.db.lock` if exists
3. Restart application

### Tkinter Not Found

**Problem**: `ModuleNotFoundError: No module named 'tkinter'`

**Solution**:
- **Windows**: Reinstall Python with "tcl/tk and IDLE" option checked
- **Linux**: `sudo apt-get install python3-tk`
- Tkinter is built-in with Python on Windows

### Revalidation Not Working

**Problem**: Old data not being revalidated

**Solution**:
1. Check `config.py`:
   ```python
   ENABLE_AUTO_REVALIDATION = True
   REVALIDATION_INTERVAL_DAYS = 7
   ```
2. Click **🔄 Revalidate Old Data** button manually
3. Check console output for errors

---

## 📦 Dependencies

```txt
# AI Model (61MB - Auto-downloads)
sentence-transformers==2.2.2   # Lightweight embeddings
torch==2.1.2                   # CPU version
transformers==4.36.2           # Hugging Face library

# Web Scraping (Backend Only)
beautifulsoup4==4.12.2         # HTML parsing
requests==2.31.0               # HTTP requests
lxml==4.9.3                    # Fast XML/HTML parser

# Data Processing
pandas==2.1.4                  # DataFrames for export
numpy==1.26.2                  # Numerical arrays

# Export Formats
openpyxl==3.1.2                # Excel (.xlsx)
xlsxwriter==3.1.9              # Excel formatting

# Progress Bars
tqdm==4.66.1                   # Terminal progress

# UI Framework
tkinter                        # Built-in with Python
```

**Total Download Size**: ~200MB (including dependencies)

---

## 🎯 Complete Feature Checklist

| Feature | Status | Details |
|---------|--------|--------|
| **AI Model Auto-Download** | ✅ | 61MB from Hugging Face on first run |
| **Tkinter UI** | ✅ | 4 tabs, built-in framework |
| **DuckDuckGo Validation** | ✅ | Primary backend scraping |
| **Google Fallback** | ✅ | Secondary validation |
| **Backend Scraping Only** | ✅ | No browser windows |
| **Weekly Revalidation** | ✅ | Auto-check data > 7 days old |
| **Travel Routes** | ✅ | Air/Train/Road collection |
| **Price Collection** | ✅ | INR (₹) from web sources |
| **AI Duplicate Detection** | ✅ | 85% semantic similarity |
| **Rating Analysis** | ✅ | 0-5 stars from reviews |
| **Review Sentiment** | ✅ | Positive/negative/neutral |
| **Multi-Format Export** | ✅ | JSON/Excel/CSV/XML |
| **SQLite Database** | ✅ | With validation tracking |
| **Validation Logging** | ✅ | Audit trail table |
| **Manual Entry** | ✅ | With AI validation |
| **Progress Tracking** | ✅ | Real-time UI updates |
| **Indian States Data** | ✅ | 36 states + tourist places |

---

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create feature branch: `git checkout -b feature/AmazingFeature`
3. Commit changes: `git commit -m 'Add AmazingFeature'`
4. Push to branch: `git push origin feature/AmazingFeature`
5. Open Pull Request

---

## 📄 License

**MIT License**

Copyright (c) 2026 David - Nexuzy Tech Pvt Ltd

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED.

---

## 👨‍💻 Author

**David**  
**Nexuzy Tech Pvt Ltd**

- 📧 Email: support@davidk.online
- 🌐 Website: [davidk.online](https://davidk.online)
- 📍 Location: Kolkata, West Bengal, India
- 💼 Company: Nexuzy Tech

---

## 🙏 Acknowledgments

- **Sentence Transformers** by UKPLab (Hugging Face)
- **PyTorch** for AI inference
- **BeautifulSoup** for web scraping
- **Tkinter** for GUI framework
- **DuckDuckGo** for privacy-focused search
- Open-source community

---

## 📊 Project Stats

- **Version**: 1.0.0
- **Status**: ✅ Complete & Production Ready
- **Last Updated**: January 16, 2026
- **Python**: 3.8+ Required
- **Platform**: Windows 10/11
- **AI Model**: 61MB (Auto-download)
- **Database**: SQLite (Embedded)
- **UI**: Tkinter (Built-in)

---

## 🔮 Future Roadmap

- [ ] Multi-threading for faster collection
- [ ] Scheduled automatic revalidation
- [ ] Advanced data visualization dashboard
- [ ] REST API for external access
- [ ] Mobile app integration
- [ ] Cloud database sync option
- [ ] Advanced NLP for review analysis
- [ ] Image recognition for hotel photos

---

**⭐ Star this repository if you find it useful!**

**🐛 Report bugs or request features via [Issues](https://github.com/david0154/TourismDataCollector/issues)**

---

*Built with ❤️ for the Indian tourism industry*
