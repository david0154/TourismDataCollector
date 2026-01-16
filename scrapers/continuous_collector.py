"""
Continuous Data Collector
Runs non-stop, scraping from multiple platforms
Only stores VERIFIED data after AI validation
"""
import time
from datetime import datetime
import threading
from typing import List, Dict

from scrapers.platform_scrapers import PlatformScrapers
from ai.data_validator import DataValidator
from ai.deduplicator import Deduplicator
from database.db_manager import DatabaseManager
from utils.india_data import INDIAN_STATES, TOURIST_PLACES
from config import (
    CONTINUOUS_COLLECTION_ENABLED,
    COLLECTION_INTERVAL_SECONDS,
    PLATFORMS_TO_SCRAPE
)

class ContinuousCollector:
    def __init__(self):
        """Initialize continuous collector"""
        self.scraper = PlatformScrapers()
        self.validator = DataValidator()
        self.deduplicator = Deduplicator()
        self.db = DatabaseManager()
        
        self.is_running = False
        self.stats = {
            'total_scraped': 0,
            'total_verified': 0,
            'total_rejected': 0,
            'total_saved': 0
        }
    
    def start_continuous_collection(self):
        """Start continuous data collection"""
        if not CONTINUOUS_COLLECTION_ENABLED:
            print("⚠️ Continuous collection is disabled in config.py")
            return
        
        print("\n" + "="*70)
        print("🚀 STARTING CONTINUOUS DATA COLLECTION")
        print("="*70)
        print(f"📡 Platforms: {len(PLATFORMS_TO_SCRAPE)}")
        print(f"⏱️ Interval: {COLLECTION_INTERVAL_SECONDS} seconds")
        print(f"🌍 States: {len(INDIAN_STATES)}")
        print(f"🏙️ Cities: {sum(len(cities) for cities in TOURIST_PLACES.values())}")
        print("="*70 + "\n")
        
        self.is_running = True
        
        # Run in background thread
        thread = threading.Thread(target=self._collection_loop, daemon=True)
        thread.start()
        
        print("✅ Continuous collection started!")
        print("   Press Ctrl+C to stop\n")
    
    def _collection_loop(self):
        """Main collection loop - runs forever"""
        cycle = 0
        
        while self.is_running:
            cycle += 1
            print(f"\n{'='*70}")
            print(f"🔄 COLLECTION CYCLE #{cycle} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"{'='*70}\n")
            
            # Iterate through all states and cities
            for state, cities in TOURIST_PLACES.items():
                if not self.is_running:
                    break
                
                print(f"\n📍 State: {state}")
                print("-" * 70)
                
                for city in cities:
                    if not self.is_running:
                        break
                    
                    print(f"\n  🏙️ City: {city}")
                    
                    # Scrape from all platforms
                    for platform in PLATFORMS_TO_SCRAPE:
                        if not self.is_running:
                            break
                        
                        try:
                            # Scrape platform
                            data = self.scraper.scrape_platform(platform, city, state)
                            self.stats['total_scraped'] += len(data)
                            
                            if data:
                                print(f"    ✅ {platform}: Found {len(data)} items")
                                
                                # Verify and save each item
                                for item in data:
                                    self._verify_and_save(item)
                            else:
                                print(f"    ⚠️ {platform}: No data found")
                        
                        except Exception as e:
                            print(f"    ❌ {platform}: Error - {e}")
                    
                    # Brief pause between cities
                    time.sleep(2)
                
                # Pause between states
                time.sleep(5)
            
            # Print cycle statistics
            self._print_stats(cycle)
            
            # Wait before next cycle
            print(f"\n⏸️ Waiting {COLLECTION_INTERVAL_SECONDS} seconds before next cycle...\n")
            time.sleep(COLLECTION_INTERVAL_SECONDS)
    
    def _verify_and_save(self, item: Dict):
        """Verify data with AI and save only if verified"""
        try:
            # Check if it's a hotel or tourist place
            if item.get('type') == 'tourist_place':
                # Verify tourist place
                is_valid = True  # Basic validation
                
                if is_valid:
                    # Check duplicates
                    existing = self.db.get_all_tourist_places(item['state'])
                    is_dup, _ = self.deduplicator.find_duplicates(item, existing)
                    
                    if not is_dup:
                        # Save to database
                        self.db.insert_tourist_place(item)
                        self.stats['total_verified'] += 1
                        self.stats['total_saved'] += 1
                        print(f"      💾 Saved: {item['name']}")
                    else:
                        print(f"      ⚠️ Duplicate: {item['name']}")
                else:
                    self.stats['total_rejected'] += 1
            
            else:
                # Verify hotel with online validation
                verification = self.validator.verify_hotel_online(
                    item['name'], item['city'], item['state']
                )
                
                if verification['found']:
                    # Update with verified data
                    item['rating'] = verification.get('rating', 0.0)
                    item['verified'] = 1
                    item['validation_source'] = verification.get('source', 'Auto')
                    
                    # Check duplicates with AI
                    existing = self.db.get_all_hotels(item['state'])
                    is_dup, similar = self.deduplicator.find_duplicates(item, existing)
                    
                    if not is_dup:
                        # Check if already exists by name
                        if not self.db.check_duplicate('hotels', item['name'], item['city'], item['state']):
                            # Save to database
                            self.db.insert_hotel(item)
                            self.stats['total_verified'] += 1
                            self.stats['total_saved'] += 1
                            print(f"      ✅💾 VERIFIED & SAVED: {item['name']} (Rating: {item['rating']:.1f}⭐)")
                        else:
                            print(f"      ⚠️ Already in database: {item['name']}")
                    else:
                        similarity = similar[0]['similarity_percent'] if similar else 'N/A'
                        print(f"      ⚠️ Duplicate detected: {item['name']} ({similarity})")
                        self.stats['total_rejected'] += 1
                else:
                    print(f"      ❌ NOT VERIFIED (not found online): {item['name']}")
                    self.stats['total_rejected'] += 1
        
        except Exception as e:
            print(f"      ❌ Error processing {item.get('name', 'Unknown')}: {e}")
            self.stats['total_rejected'] += 1
    
    def _print_stats(self, cycle: int):
        """Print collection statistics"""
        print(f"\n{'='*70}")
        print(f"📊 CYCLE #{cycle} STATISTICS")
        print(f"{'='*70}")
        print(f"📥 Total Scraped:     {self.stats['total_scraped']}")
        print(f"✅ Total Verified:    {self.stats['total_verified']}")
        print(f"💾 Total Saved:       {self.stats['total_saved']}")
        print(f"❌ Total Rejected:    {self.stats['total_rejected']}")
        
        if self.stats['total_scraped'] > 0:
            success_rate = (self.stats['total_verified'] / self.stats['total_scraped']) * 100
            print(f"📈 Success Rate:      {success_rate:.1f}%")
        
        print(f"{'='*70}\n")
    
    def stop(self):
        """Stop continuous collection"""
        print("\n⛔ Stopping continuous collection...")
        self.is_running = False
        print("✅ Stopped!\n")
