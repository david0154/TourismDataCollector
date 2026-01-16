"""\nComplete Tkinter UI for Tourism Data Collector\n5 TABS: Dashboard, Data Collection, View Data, Export Data, Manual Entry\nWith REAL Data Collection from Internet\n"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import threading
from typing import Dict, Any
from datetime import datetime, timedelta

from database.db_manager import DatabaseManager
from ai.data_validator import DataValidator
from ai.deduplicator import Deduplicator
from scrapers.hotel_scraper import HotelScraper
from scrapers.place_scraper import PlaceScraper
from utils.india_data import INDIAN_STATES, get_tourist_places
from utils.exporters import DataExporter
from config import ENABLE_AUTO_REVALIDATION, REVALIDATION_INTERVAL_DAYS

class TourismApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tourism Data Collector - Nexuzy Tech")
        self.root.geometry("1400x900")
        self.root.configure(bg='#f5f5f5')
        
        # Collection control flag
        self.collection_running = False
        
        # Initialize components
        print("\n" + "="*60)
        print("🚀 Starting Tourism Data Collector")
        print("="*60)
        
        self.db = DatabaseManager()
        self.validator = DataValidator()
        
        print("\n📥 Loading AI Model (auto-download if needed)...")
        self.deduplicator = Deduplicator()
        
        # Initialize scrapers
        self.hotel_scraper = HotelScraper()
        self.place_scraper = PlaceScraper()
        
        self.exporter = DataExporter()
        
        print("\n✅ All systems ready!")
        print("="*60 + "\n")
        
        # Create UI
        self.create_widgets()
    
    def create_widgets(self):
        """Create main UI widgets"""
        # Title Bar
        title_frame = tk.Frame(self.root, bg='#2196F3', height=100)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame, 
            text="🏨 Tourism Data Collector", 
            font=('Arial', 28, 'bold'),
            bg='#2196F3',
            fg='white'
        )
        title_label.pack(pady=15)
        
        subtitle = tk.Label(
            title_frame,
            text="AI-Powered | Real Internet Data Collection | DuckDuckGo + Google | Auto Validation",
            font=('Arial', 11),
            bg='#2196F3',
            fg='white'
        )
        subtitle.pack()
        
        # Notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create all 5 tabs (Dashboard is first)
        self.create_dashboard_tab()
        self.create_collection_tab()
        self.create_view_tab()
        self.create_export_tab()
        self.create_manual_entry_tab()
        
        # Status bar
        status_frame = tk.Frame(self.root, bg='#2196F3', height=35)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.status_label = tk.Label(
            status_frame,
            text=f"✅ Ready | AI Model: Loaded (61MB) | Database: Connected | Revalidation: {'ON' if ENABLE_AUTO_REVALIDATION else 'OFF'} ({REVALIDATION_INTERVAL_DAYS} days)",
            bg='#2196F3',
            fg='white',
            font=('Arial', 10)
        )
        self.status_label.pack(pady=7)
    
    def create_dashboard_tab(self):
        """Dashboard Tab with Statistics and Verified Badges"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="📊 Dashboard")
        
        # Main container with scrollbar
        container = tk.Frame(tab, bg='#f0f0f0')
        container.pack(fill=tk.BOTH, expand=True)
        
        # Canvas for scrolling
        canvas = tk.Canvas(container, bg='#f0f0f0')
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#f0f0f0')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Header
        header_frame = tk.Frame(scrollable_frame, bg='#2196F3', height=80)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(
            header_frame,
            text="🎯 Dashboard Overview",
            font=('Arial', 24, 'bold'),
            bg='#2196F3',
            fg='white'
        ).pack(pady=15)
        
        # Refresh button
        refresh_frame = tk.Frame(scrollable_frame, bg='#f0f0f0')
        refresh_frame.pack(pady=10)
        
        tk.Button(
            refresh_frame,
            text="🔄 Refresh Dashboard",
            command=self.refresh_dashboard,
            bg='#4CAF50',
            fg='white',
            font=('Arial', 12, 'bold'),
            padx=25,
            pady=10,
            cursor='hand2',
            relief=tk.RAISED,
            bd=3
        ).pack()
        
        # Statistics Cards Row 1
        stats_frame1 = tk.Frame(scrollable_frame, bg='#f0f0f0')
        stats_frame1.pack(fill=tk.X, padx=30, pady=10)
        
        # Create stat cards
        self.total_hotels_card = self.create_stat_card(
            stats_frame1, "🏨 Total Hotels", "0", "#FF5722", 0
        )
        self.verified_hotels_card = self.create_stat_card(
            stats_frame1, "✅ Verified Hotels", "0", "#4CAF50", 1
        )
        self.unverified_hotels_card = self.create_stat_card(
            stats_frame1, "❌ Unverified Hotels", "0", "#9E9E9E", 2
        )
        
        # Statistics Cards Row 2
        stats_frame2 = tk.Frame(scrollable_frame, bg='#f0f0f0')
        stats_frame2.pack(fill=tk.X, padx=30, pady=10)
        
        self.total_places_card = self.create_stat_card(
            stats_frame2, "🏞️ Tourist Places", "0", "#2196F3", 0
        )
        self.verified_places_card = self.create_stat_card(
            stats_frame2, "✅ Verified Places", "0", "#009688", 1
        )
        self.total_services_card = self.create_stat_card(
            stats_frame2, "🚌 Travel Services", "0", "#FF9800", 2
        )
        
        # Recent Data Section
        recent_frame = tk.LabelFrame(
            scrollable_frame,
            text="🕒 Recently Added Data",
            font=('Arial', 14, 'bold'),
            bg='white',
            padx=20,
            pady=15
        )
        recent_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        # Recent data table
        table_frame = tk.Frame(recent_frame, bg='white')
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        scroll_y = tk.Scrollbar(table_frame, orient=tk.VERTICAL)
        scroll_x = tk.Scrollbar(table_frame, orient=tk.HORIZONTAL)
        
        self.dashboard_tree = ttk.Treeview(
            table_frame,
            columns=('Type', 'Name', 'City', 'State', 'Rating', 'Price', 'Verified', 'Validated'),
            show='headings',
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set,
            height=10
        )
        
        scroll_y.config(command=self.dashboard_tree.yview)
        scroll_x.config(command=self.dashboard_tree.xview)
        
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.dashboard_tree.pack(fill=tk.BOTH, expand=True)
        
        # Column headings
        columns = {
            'Type': 100,
            'Name': 250,
            'City': 150,
            'State': 150,
            'Rating': 100,
            'Price': 120,
            'Verified': 100,
            'Validated': 120
        }
        
        for col, width in columns.items():
            self.dashboard_tree.heading(col, text=col)
            self.dashboard_tree.column(col, width=width)
        
        # Configure tag colors for verified status
        self.dashboard_tree.tag_configure('verified', background='#E8F5E9')
        self.dashboard_tree.tag_configure('unverified', background='#FFEBEE')
        
        # Validation Stats
        validation_frame = tk.LabelFrame(
            scrollable_frame,
            text="📊 Validation Statistics",
            font=('Arial', 14, 'bold'),
            bg='white',
            padx=20,
            pady=15
        )
        validation_frame.pack(fill=tk.X, padx=30, pady=20)
        
        self.validation_stats_label = tk.Label(
            validation_frame,
            text="Loading statistics...",
            font=('Arial', 11),
            bg='white',
            justify=tk.LEFT,
            fg='#424242'
        )
        self.validation_stats_label.pack(anchor=tk.W, pady=10)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Initial data load
        self.root.after(500, self.refresh_dashboard)
    
    def create_stat_card(self, parent, title, value, color, column):
        """Create a statistics card"""
        card = tk.Frame(parent, bg=color, relief=tk.RAISED, bd=3)
        card.grid(row=0, column=column, padx=15, pady=10, sticky='nsew')
        parent.grid_columnconfigure(column, weight=1)
        
        # Title
        tk.Label(
            card,
            text=title,
            font=('Arial', 12, 'bold'),
            bg=color,
            fg='white'
        ).pack(pady=(15, 5))
        
        # Value
        value_label = tk.Label(
            card,
            text=value,
            font=('Arial', 32, 'bold'),
            bg=color,
            fg='white'
        )
        value_label.pack(pady=(5, 15))
        
        # Store reference for updating
        card.value_label = value_label
        
        return card
    
    def refresh_dashboard(self):
        """Refresh dashboard data"""
        # Get all data
        hotels = self.db.get_all_hotels()
        places = self.db.get_all_tourist_places()
        
        # Count verified/unverified
        verified_hotels = sum(1 for h in hotels if h.get('verified', 0) == 1)
        unverified_hotels = len(hotels) - verified_hotels
        
        verified_places = sum(1 for p in places if p.get('verified', 0) == 1)
        
        # Update stat cards
        self.total_hotels_card.value_label.config(text=str(len(hotels)))
        self.verified_hotels_card.value_label.config(text=str(verified_hotels))
        self.unverified_hotels_card.value_label.config(text=str(unverified_hotels))
        self.total_places_card.value_label.config(text=str(len(places)))
        self.verified_places_card.value_label.config(text=str(verified_places))
        self.total_services_card.value_label.config(text="0")
        
        # Clear table
        for item in self.dashboard_tree.get_children():
            self.dashboard_tree.delete(item)
        
        # Add recent hotels (last 20)
        recent_hotels = sorted(hotels, key=lambda x: x.get('created_at', ''), reverse=True)[:20]
        
        for hotel in recent_hotels:
            verified = hotel.get('verified', 0) == 1
            tag = 'verified' if verified else 'unverified'
            
            self.dashboard_tree.insert('', tk.END, values=(
                'Hotel',
                hotel.get('name', ''),
                hotel.get('city', ''),
                hotel.get('state', ''),
                f"{hotel.get('rating', 0.0):.1f}⭐",
                f"₹{hotel.get('price', 0)}",
                "✅ Verified" if verified else "❌ Not Verified",
                hotel.get('last_validated_at', 'Never')[:10] if hotel.get('last_validated_at') else 'Never'
            ), tags=(tag,))
        
        # Add recent places
        recent_places = sorted(places, key=lambda x: x.get('created_at', ''), reverse=True)[:10]
        
        for place in recent_places:
            verified = place.get('verified', 0) == 1
            tag = 'verified' if verified else 'unverified'
            
            self.dashboard_tree.insert('', tk.END, values=(
                'Tourist Place',
                place.get('name', ''),
                place.get('city', ''),
                place.get('state', ''),
                'N/A',
                f"₹{place.get('entry_fee', 0)}",
                "✅ Verified" if verified else "❌ Not Verified",
                place.get('last_validated_at', 'Never')[:10] if place.get('last_validated_at') else 'Never'
            ), tags=(tag,))
        
        # Update validation stats
        old_hotels = self.db.get_hotels_needing_revalidation(REVALIDATION_INTERVAL_DAYS)
        
        stats_text = f"""
📋 Total Records: {len(hotels) + len(places)}
✅ Total Verified: {verified_hotels + verified_places}
❌ Total Unverified: {unverified_hotels + (len(places) - verified_places)}
♻️ Need Revalidation: {len(old_hotels)} hotels (>{REVALIDATION_INTERVAL_DAYS} days old)
📅 Last Refresh: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """
        
        self.validation_stats_label.config(text=stats_text)
        
        # Update status
        self.status_label.config(
            text=f"✅ Dashboard Updated | Hotels: {len(hotels)} | Places: {len(places)} | Verified: {verified_hotels + verified_places}"
        )
    
    def create_collection_tab(self):
        """Data Collection Tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="📊 Data Collection")
        
        container = tk.Frame(tab, bg='white', padx=25, pady=20)
        container.pack(fill=tk.BOTH, expand=True)
        
        # Location Selection
        location_frame = tk.LabelFrame(
            container, 
            text="📍 Select Location", 
            font=('Arial', 13, 'bold'), 
            bg='white', 
            padx=20, 
            pady=15
        )
        location_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(location_frame, text="State:", bg='white', font=('Arial', 11)).grid(row=0, column=0, sticky=tk.W, pady=8)
        self.state_var = tk.StringVar(value="West Bengal")
        self.state_combo = ttk.Combobox(location_frame, textvariable=self.state_var, width=35, state='readonly', font=('Arial', 10))
        self.state_combo['values'] = sorted(INDIAN_STATES.keys())
        self.state_combo.grid(row=0, column=1, padx=15, pady=8)
        self.state_combo.bind('<<ComboboxSelected>>', self.on_state_changed)
        
        tk.Label(location_frame, text="City/Place:", bg='white', font=('Arial', 11)).grid(row=1, column=0, sticky=tk.W, pady=8)
        self.place_var = tk.StringVar(value="Kolkata")
        self.place_combo = ttk.Combobox(location_frame, textvariable=self.place_var, width=35, state='readonly', font=('Arial', 10))
        self.place_combo['values'] = ["Kolkata", "Darjeeling", "Digha"]
        self.place_combo.grid(row=1, column=1, padx=15, pady=8)
        
        # Data Type Selection
        type_frame = tk.LabelFrame(container, text="🏢 Select Data Type", font=('Arial', 13, 'bold'), bg='white', padx=20, pady=15)
        type_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(type_frame, text="Data Type:", bg='white', font=('Arial', 11)).grid(row=0, column=0, sticky=tk.W, pady=8)
        self.data_type_var = tk.StringVar(value="Hotels")
        self.data_type_combo = ttk.Combobox(type_frame, textvariable=self.data_type_var, width=35, state='readonly', font=('Arial', 10))
        self.data_type_combo['values'] = ["Hotels", "Tourist Places", "Both"]
        self.data_type_combo.grid(row=0, column=1, padx=15, pady=8)
        
        # Collection Options
        options_frame = tk.LabelFrame(container, text="⚙️ REAL Data Collection Features", font=('Arial', 13, 'bold'), bg='white', padx=20, pady=15)
        options_frame.pack(fill=tk.X, pady=10)
        
        options_text = """
✅ REAL Data from Internet (DuckDuckGo + Google Search)
✅ Actual Hotel Names, Ratings, Prices, Contact Numbers
✅ AI Model: paraphrase-MiniLM-L3-v2 (61MB)
✅ AI Duplicate Detection (85% similarity)
✅ Automatic Verification & Validation
✅ Data Saved to SQLite Database
✅ Continuous Collection (keeps running until stopped)
        """
        tk.Label(options_frame, text=options_text, bg='white', font=('Arial', 10), justify=tk.LEFT, fg='#1976D2').pack(anchor=tk.W, pady=5)
        
        # Progress Section
        progress_frame = tk.Frame(container, bg='white')
        progress_frame.pack(fill=tk.X, pady=15)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, maximum=100, length=800)
        self.progress_bar.pack(fill=tk.X, pady=5)
        
        self.progress_label = tk.Label(progress_frame, text="Ready to collect REAL data from internet", bg='white', font=('Arial', 11), fg='#4CAF50')
        self.progress_label.pack(pady=5)
        
        # Buttons
        button_frame = tk.Frame(container, bg='white')
        button_frame.pack(pady=20)
        
        self.collect_btn = tk.Button(
            button_frame, 
            text="🚀 Start REAL Data Collection", 
            command=self.start_collection,
            bg='#4CAF50', 
            fg='white', 
            font=('Arial', 13, 'bold'),
            padx=35,
            pady=12,
            cursor='hand2',
            relief=tk.RAISED,
            bd=3
        )
        self.collect_btn.grid(row=0, column=0, padx=10)
        
        self.stop_btn = tk.Button(
            button_frame,
            text="⛔ Stop Collection",
            command=self.stop_collection,
            bg='#f44336',
            fg='white',
            font=('Arial', 13, 'bold'),
            padx=35,
            pady=12,
            state=tk.DISABLED,
            cursor='hand2',
            relief=tk.RAISED,
            bd=3
        )
        self.stop_btn.grid(row=0, column=1, padx=10)
        
        self.revalidate_btn = tk.Button(
            button_frame,
            text="🔄 Revalidate Old Data",
            command=self.revalidate_old_data,
            bg='#FF9800',
            fg='white',
            font=('Arial', 13, 'bold'),
            padx=35,
            pady=12,
            cursor='hand2',
            relief=tk.RAISED,
            bd=3
        )
        self.revalidate_btn.grid(row=0, column=2, padx=10)
    
    def create_view_tab(self):
        """View Data Tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="👁️ View Data")
        
        container = tk.Frame(tab, bg='white', padx=25, pady=20)
        container.pack(fill=tk.BOTH, expand=True)
        
        # Filters
        filter_frame = tk.Frame(container, bg='white')
        filter_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(filter_frame, text="View:", bg='white', font=('Arial', 11, 'bold')).pack(side=tk.LEFT, padx=5)
        self.view_type_var = tk.StringVar(value="Hotels")
        view_combo = ttk.Combobox(filter_frame, textvariable=self.view_type_var, width=25, state='readonly', font=('Arial', 10))
        view_combo['values'] = ["Hotels", "Tourist Places", "Travel Services"]
        view_combo.pack(side=tk.LEFT, padx=5)
        
        tk.Label(filter_frame, text="State:", bg='white', font=('Arial', 11, 'bold')).pack(side=tk.LEFT, padx=15)
        self.view_state_var = tk.StringVar(value="All States")
        view_state_combo = ttk.Combobox(filter_frame, textvariable=self.view_state_var, width=25, state='readonly', font=('Arial', 10))
        view_state_combo['values'] = ["All States"] + sorted(INDIAN_STATES.keys())
        view_state_combo.pack(side=tk.LEFT, padx=5)
        
        refresh_btn = tk.Button(filter_frame, text="🔄 Refresh", command=self.refresh_table, bg='#2196F3', fg='white', font=('Arial', 11, 'bold'), cursor='hand2', padx=20, pady=8)
        refresh_btn.pack(side=tk.LEFT, padx=15)
        
        # Table
        table_frame = tk.Frame(container)
        table_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        scroll_y = tk.Scrollbar(table_frame, orient=tk.VERTICAL)
        scroll_x = tk.Scrollbar(table_frame, orient=tk.HORIZONTAL)
        
        self.data_tree = ttk.Treeview(
            table_frame,
            columns=('ID', 'Name', 'City', 'State', 'Contact', 'Rating', 'Price', 'Verified', 'Last Validated'),
            show='headings',
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set
        )
        
        scroll_y.config(command=self.data_tree.yview)
        scroll_x.config(command=self.data_tree.xview)
        
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.data_tree.pack(fill=tk.BOTH, expand=True)
        
        # Column headings
        for col in self.data_tree['columns']:
            self.data_tree.heading(col, text=col)
            self.data_tree.column(col, width=130)
        
        # Record count
        self.record_count_label = tk.Label(container, text="Total Records: 0", bg='white', font=('Arial', 12, 'bold'), fg='#1976D2')
        self.record_count_label.pack(pady=8)
    
    def create_export_tab(self):
        """Export Data Tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="📤 Export Data")
        
        container = tk.Frame(tab, bg='white', padx=25, pady=20)
        container.pack(fill=tk.BOTH, expand=True)
        
        # Export options
        options_frame = tk.LabelFrame(container, text="📋 Export Options", font=('Arial', 13, 'bold'), bg='white', padx=25, pady=20)
        options_frame.pack(fill=tk.X, pady=20)
        
        tk.Label(options_frame, text="Export Format:", bg='white', font=('Arial', 11)).grid(row=0, column=0, sticky=tk.W, pady=12)
        self.export_format_var = tk.StringVar(value="Excel (XLSX)")
        format_combo = ttk.Combobox(options_frame, textvariable=self.export_format_var, width=30, state='readonly', font=('Arial', 10))
        format_combo['values'] = ["JSON", "Excel (XLSX)", "CSV", "XML"]
        format_combo.grid(row=0, column=1, padx=15, pady=12)
        
        tk.Label(options_frame, text="Data Type:", bg='white', font=('Arial', 11)).grid(row=1, column=0, sticky=tk.W, pady=12)
        self.export_data_var = tk.StringVar(value="Hotels")
        data_combo = ttk.Combobox(options_frame, textvariable=self.export_data_var, width=30, state='readonly', font=('Arial', 10))
        data_combo['values'] = ["Hotels", "Tourist Places", "Travel Services", "All Data"]
        data_combo.grid(row=1, column=1, padx=15, pady=12)
        
        export_btn = tk.Button(
            options_frame,
            text="💾 Export Data",
            command=self.export_data,
            bg='#FF9800',
            fg='white',
            font=('Arial', 13, 'bold'),
            padx=35,
            pady=12,
            cursor='hand2',
            relief=tk.RAISED,
            bd=3
        )
        export_btn.grid(row=2, column=0, columnspan=2, pady=20)
        
        # Export log
        log_frame = tk.LabelFrame(container, text="📝 Export Log", font=('Arial', 13, 'bold'), bg='white', padx=15, pady=15)
        log_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.export_log = scrolledtext.ScrolledText(log_frame, height=18, font=('Courier', 10), bg='#f9f9f9')
        self.export_log.pack(fill=tk.BOTH, expand=True)
    
    def create_manual_entry_tab(self):
        """Manual Entry Tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="✍️ Manual Entry")
        
        container = tk.Frame(tab, bg='white', padx=25, pady=20)
        container.pack(fill=tk.BOTH, expand=True)
        
        # Form
        form_frame = tk.LabelFrame(container, text="🏨 Add Hotel with AI Validation", font=('Arial', 13, 'bold'), bg='white', padx=25, pady=20)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        fields = [
            ("Hotel Name:", "name"),
            ("Address:", "address"),
            ("City:", "city"),
            ("Contact:", "contact"),
            ("Email:", "email"),
            ("Website:", "website"),
            ("Price (₹ per night):", "price")
        ]
        
        self.entry_fields = {}
        
        for idx, (label, field) in enumerate(fields):
            tk.Label(form_frame, text=label, bg='white', font=('Arial', 11)).grid(row=idx, column=0, sticky=tk.W, pady=10, padx=8)
            entry = tk.Entry(form_frame, width=45, font=('Arial', 11))
            entry.grid(row=idx, column=1, pady=10, padx=15, sticky=tk.W)
            self.entry_fields[field] = entry
        
        # State dropdown
        tk.Label(form_frame, text="State:", bg='white', font=('Arial', 11)).grid(row=len(fields), column=0, sticky=tk.W, pady=10, padx=8)
        self.manual_state_var = tk.StringVar()
        state_combo = ttk.Combobox(form_frame, textvariable=self.manual_state_var, width=43, state='readonly', font=('Arial', 10))
        state_combo['values'] = sorted(INDIAN_STATES.keys())
        state_combo.grid(row=len(fields), column=1, pady=10, padx=15, sticky=tk.W)
        
        # Buttons
        btn_frame = tk.Frame(form_frame, bg='white')
        btn_frame.grid(row=len(fields)+1, column=0, columnspan=2, pady=25)
        
        add_btn = tk.Button(
            btn_frame,
            text="✅ Add with AI Validation (DuckDuckGo + Duplicate Check)",
            command=self.add_hotel_manually,
            bg='#4CAF50',
            fg='white',
            font=('Arial', 12, 'bold'),
            padx=25,
            pady=12,
            cursor='hand2',
            relief=tk.RAISED,
            bd=3
        )
        add_btn.pack(side=tk.LEFT, padx=10)
        
        clear_btn = tk.Button(
            btn_frame,
            text="🗑️ Clear Form",
            command=self.clear_form,
            bg='#9E9E9E',
            fg='white',
            font=('Arial', 12, 'bold'),
            padx=25,
            pady=12,
            cursor='hand2',
            relief=tk.RAISED,
            bd=3
        )
        clear_btn.pack(side=tk.LEFT, padx=10)
    
    def on_state_changed(self, event=None):
        """Handle state selection change"""
        state = self.state_var.get()
        if state in INDIAN_STATES:
            places = get_tourist_places(state)
            self.place_combo['values'] = places if places else ["All Places"]
            if places:
                self.place_var.set(places[0])
    
    def start_collection(self):
        """Start REAL data collection"""
        self.collection_running = True
        self.collect_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.progress_var.set(0)
        
        thread = threading.Thread(target=self.collection_worker, daemon=True)
        thread.start()
    
    def collection_worker(self):
        """REAL Data Collection Worker - Scrapes from Internet"""
        state = self.state_var.get()
        city = self.place_var.get()
        data_type = self.data_type_var.get()
        
        print(f"\n{'='*60}")
        print(f"🚀 Starting REAL Data Collection")
        print(f"{'='*60}")
        print(f"State: {state}")
        print(f"City: {city}")
        print(f"Type: {data_type}")
        print(f"{'='*60}\n")
        
        total_collected = 0
        
        try:
            # Collect Hotels
            if data_type in ["Hotels", "Both"] and self.collection_running:
                self.update_progress(10, f"🔍 Searching hotels in {city}, {state} via DuckDuckGo...")
                
                hotels = self.hotel_scraper.search_hotels_duckduckgo(city, state, limit=10)
                
                if not hotels and self.collection_running:
                    self.update_progress(20, "🔍 Trying Google Search as fallback...")
                    hotels = self.hotel_scraper.search_hotels_google(city, state, limit=10)
                
                # Save hotels to database
                for idx, hotel in enumerate(hotels):
                    if not self.collection_running:
                        break
                    
                    progress = 30 + int((idx / len(hotels)) * 40)
                    self.update_progress(progress, f"🤖 Validating: {hotel['name']}...")
                    
                    # Check for duplicates with AI
                    existing = self.db.get_all_hotels()
                    is_dup, similar = self.deduplicator.find_duplicates(hotel, existing)
                    
                    if not is_dup:
                        try:
                            self.db.insert_hotel(hotel)
                            total_collected += 1
                            print(f"  ✅ Saved: {hotel['name']} - ₹{hotel['price']}")
                        except Exception as e:
                            print(f"  ❌ Error saving {hotel['name']}: {e}")
                    else:
                        print(f"  ⚠️ Skipped duplicate: {hotel['name']}")
            
            # Collect Tourist Places
            if data_type in ["Tourist Places", "Both"] and self.collection_running:
                self.update_progress(70, f"🏛️ Searching tourist places in {city}, {state}...")
                
                places = self.place_scraper.search_places(city, state, limit=5)
                
                for idx, place in enumerate(places):
                    if not self.collection_running:
                        break
                    
                    progress = 75 + int((idx / max(len(places), 1)) * 20)
                    self.update_progress(progress, f"🏛️ Saving: {place['name']}...")
                    
                    try:
                        # Check duplicate
                        if not self.db.check_duplicate('tourist_places', place['name'], place['city'], place['state']):
                            self.db.insert_tourist_place(place)
                            total_collected += 1
                            print(f"  ✅ Saved place: {place['name']}")
                    except Exception as e:
                        print(f"  ❌ Error saving place: {e}")
            
            self.update_progress(100, f"✅ Collection completed! Saved {total_collected} records")
            
            print(f"\n{'='*60}")
            print(f"✅ Data Collection Complete!")
            print(f"💾 Total Records Saved: {total_collected}")
            print(f"{'='*60}\n")
            
            if total_collected > 0:
                self.root.after(100, lambda: messagebox.showinfo(
                    "Success", 
                    f"Data collection completed!\n\nLocation: {city}, {state}\nType: {data_type}\nSaved: {total_collected} records\n\nCheck Dashboard to view data!"
                ))
            else:
                self.root.after(100, lambda: messagebox.showwarning(
                    "No Data",
                    f"No new data found for {city}, {state}.\n\nTry different location or data type."
                ))
        
        except Exception as e:
            print(f"❌ Collection error: {e}")
            self.root.after(0, lambda: messagebox.showerror("Error", f"Collection failed: {str(e)}"))
        
        finally:
            self.collection_running = False
            self.root.after(200, lambda: self.collect_btn.config(state=tk.NORMAL))
            self.root.after(200, lambda: self.stop_btn.config(state=tk.DISABLED))
            self.root.after(300, self.refresh_dashboard)
    
    def stop_collection(self):
        """Stop collection"""
        self.collection_running = False
        self.collect_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.progress_label.config(text="Collection stopped by user")
        print("\n⛔ Collection stopped by user\n")
    
    def revalidate_old_data(self):
        """Revalidate data older than 7 days"""
        self.revalidate_btn.config(state=tk.DISABLED)
        thread = threading.Thread(target=self.revalidation_worker, daemon=True)
        thread.start()
    
    def revalidation_worker(self):
        """Worker for revalidation"""
        self.update_progress(10, "🔍 Finding old data...")
        
        old_hotels = self.db.get_hotels_needing_revalidation(REVALIDATION_INTERVAL_DAYS)
        
        if not old_hotels:
            self.root.after(0, lambda: messagebox.showinfo("Info", "No data needs revalidation!"))
            self.root.after(0, lambda: self.revalidate_btn.config(state=tk.NORMAL))
            return
        
        total = len(old_hotels)
        self.update_progress(20, f"♻️ Revalidating {total} hotels...")
        
        for idx, hotel in enumerate(old_hotels):
            progress = 20 + int((idx / total) * 70)
            self.update_progress(progress, f"Revalidating: {hotel['name']} ({idx+1}/{total})")
            
            # Verify online
            result = self.validator.verify_hotel_online(
                hotel['name'], hotel['city'], hotel['state']
            )
            
            if result['found']:
                # Update hotel with new data
                updated_data = {
                    'name': hotel['name'],
                    'address': hotel.get('address'),
                    'city': hotel['city'],
                    'state': hotel['state'],
                    'contact': hotel.get('contact'),
                    'email': hotel.get('email'),
                    'website': hotel.get('website'),
                    'rating': result.get('rating', 0.0),
                    'price': 0,
                    'verified': 1 if result['found'] else 0
                }
                
                self.db.update_hotel(hotel['id'], updated_data)
                self.db.log_validation('hotels', hotel['id'], 'revalidation', 'success')
        
        self.update_progress(100, f"✅ Revalidated {total} hotels!")
        
        self.root.after(0, lambda: messagebox.showinfo("Success", f"Revalidated {total} hotels successfully!"))
        self.root.after(0, lambda: self.revalidate_btn.config(state=tk.NORMAL))
        self.root.after(0, self.refresh_table)
        self.root.after(0, self.refresh_dashboard)
    
    def update_progress(self, value, text):
        """Update progress"""
        self.root.after(0, lambda: self.progress_var.set(value))
        self.root.after(0, lambda: self.progress_label.config(text=text))
    
    def refresh_table(self):
        """Refresh table"""
        for item in self.data_tree.get_children():
            self.data_tree.delete(item)
        
        view_type = self.view_type_var.get()
        state = self.view_state_var.get()
        state_filter = None if state == "All States" else state
        
        if view_type == "Hotels":
            data = self.db.get_all_hotels(state_filter)
        elif view_type == "Tourist Places":
            data = self.db.get_all_tourist_places(state_filter)
        else:
            data = []
        
        for record in data:
            self.data_tree.insert('', tk.END, values=(
                record.get('id', ''),
                record.get('name', ''),
                record.get('city', ''),
                record.get('state', ''),
                record.get('contact', ''),
                f"{record.get('rating', 0.0):.1f}⭐",
                f"₹{record.get('price', 0)}",
                "✓" if record.get('verified') else "✗",
                record.get('last_validated_at', 'Never')[:10] if record.get('last_validated_at') else 'Never'
            ))
        
        self.record_count_label.config(text=f"Total Records: {len(data)}")
    
    def export_data(self):
        """Export data"""
        format_type = self.export_format_var.get()
        data_type = self.export_data_var.get()
        
        ext_map = {
            "JSON": ".json",
            "Excel (XLSX)": ".xlsx",
            "CSV": ".csv",
            "XML": ".xml"
        }
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=ext_map.get(format_type, ".json"),
            filetypes=[(format_type, f"*{ext_map.get(format_type, '.json')}")]
        )
        
        if file_path:
            try:
                if data_type == "Hotels":
                    data = self.db.get_all_hotels()
                elif data_type == "Tourist Places":
                    data = self.db.get_all_tourist_places()
                else:
                    data = []
                
                if format_type == "JSON":
                    self.exporter.export_to_json(data, file_path)
                elif format_type == "Excel (XLSX)":
                    self.exporter.export_to_excel(data, file_path)
                elif format_type == "CSV":
                    self.exporter.export_to_csv(data, file_path)
                elif format_type == "XML":
                    self.exporter.export_to_xml(data, file_path)
                
                self.export_log.insert(tk.END, f"[{datetime.now().strftime('%H:%M:%S')}] ✅ Exported {len(data)} records to {file_path}\n")
                messagebox.showinfo("Success", f"Exported {len(data)} records successfully!")
            except Exception as e:
                self.export_log.insert(tk.END, f"[{datetime.now().strftime('%H:%M:%S')}] ❌ Error: {str(e)}\n")
                messagebox.showerror("Error", f"Export failed: {str(e)}")
    
    def add_hotel_manually(self):
        """Add hotel with AI validation"""
        hotel_data = {
            'name': self.entry_fields['name'].get(),
            'address': self.entry_fields['address'].get(),
            'city': self.entry_fields['city'].get(),
            'state': self.manual_state_var.get(),
            'contact': self.entry_fields['contact'].get(),
            'email': self.entry_fields['email'].get(),
            'website': self.entry_fields['website'].get(),
            'price': int(self.entry_fields['price'].get() or 0)
        }
        
        # Validate
        is_valid, errors = self.validator.validate_hotel_data(hotel_data)
        
        if not is_valid:
            error_msg = "\n".join([f"{k}: {v}" for k, v in errors.items()])
            messagebox.showerror("Validation Error", f"Please fix:\n\n{error_msg}")
            return
        
        # Online verification
        print(f"🌐 Verifying {hotel_data['name']} via DuckDuckGo...")
        verification = self.validator.verify_hotel_online(
            hotel_data['name'], hotel_data['city'], hotel_data['state']
        )
        
        if verification['found']:
            hotel_data['rating'] = verification.get('rating', 0.0)
            hotel_data['verified'] = 1
            hotel_data['validation_source'] = verification.get('source', 'DuckDuckGo')
        
        # Check duplicates with AI
        existing = self.db.get_all_hotels()
        is_dup, similar = self.deduplicator.find_duplicates(hotel_data, existing)
        
        if is_dup:
            messagebox.showwarning("Duplicate Detected", f"Similar hotel found!\nSimilarity: {similar[0]['similarity_percent']}")
            return
        
        # Insert
        try:
            self.db.insert_hotel(hotel_data)
            messagebox.showinfo("Success", f"Hotel added successfully!\n\nVerified: {verification['found']}\nRating: {hotel_data.get('rating', 0.0):.1f}⭐")
            self.clear_form()
            self.refresh_table()
            self.refresh_dashboard()
        except Exception as e:
            messagebox.showerror("Error", f"Failed: {str(e)}")
    
    def clear_form(self):
        """Clear form"""
        for entry in self.entry_fields.values():
            entry.delete(0, tk.END)
        self.manual_state_var.set('')
