"""
Tourism Data Collector
Tkinter-based Windows application with auto AI download
Now with CONTINUOUS COLLECTION mode
"""
import tkinter as tk
import sys
import argparse
from ui.main_window import TourismApp
from scrapers.continuous_collector import ContinuousCollector

def run_gui():
    """Run Tkinter GUI application"""
    root = tk.Tk()
    app = TourismApp(root)
    root.mainloop()

def run_continuous():
    """Run continuous background collection"""
    print("\n" + "="*70)
    print("🚀 TOURISM DATA COLLECTOR - CONTINUOUS MODE")
    print("="*70)
    print("📊 Scrapes from 40+ platforms non-stop")
    print("✅ Only saves VERIFIED data (AI + DuckDuckGo validation)")
    print("❌ Unverified data is rejected automatically")
    print("\nPress Ctrl+C to stop\n")
    print("="*70 + "\n")
    
    collector = ContinuousCollector()
    
    try:
        collector.start_continuous_collection()
        
        # Keep main thread alive
        import time
        while True:
            time.sleep(1)
    
    except KeyboardInterrupt:
        print("\n\n⛔ Stopping collector...")
        collector.stop()
        print("✅ Stopped successfully!\n")
        sys.exit(0)

def main():
    """Main application entry point"""
    parser = argparse.ArgumentParser(
        description='Tourism Data Collector - Scrape & Verify Indian Tourism Data'
    )
    
    parser.add_argument(
        '--continuous',
        action='store_true',
        help='Run in continuous collection mode (background scraping)'
    )
    
    parser.add_argument(
        '--gui',
        action='store_true',
        default=True,
        help='Run GUI application (default)'
    )
    
    args = parser.parse_args()
    
    if args.continuous:
        # Run continuous background collector
        run_continuous()
    else:
        # Run Tkinter GUI (default)
        run_gui()

if __name__ == "__main__":
    main()
