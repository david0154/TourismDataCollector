"""
SQLite Database Manager for Tourism Data
"""
import sqlite3
from typing import List, Dict, Any, Optional
from datetime import datetime
import os
from config import DB_PATH

class DatabaseManager:
    def __init__(self):
        """Initialize database connection and create tables"""
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        self.conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.create_tables()
    
    def create_tables(self):
        """Create all required tables"""
        cursor = self.conn.cursor()
        
        # Hotels table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS hotels (
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
                price_min INTEGER DEFAULT 0,
                price_max INTEGER DEFAULT 0,
                price_avg INTEGER DEFAULT 0,
                room_types TEXT,
                amenities TEXT,
                verified INTEGER DEFAULT 0,
                last_verified TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tourist Places table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tourist_places (
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
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Travel Services table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS travel_services (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                service_type TEXT NOT NULL,
                provider_name TEXT NOT NULL,
                contact TEXT,
                email TEXT,
                website TEXT,
                routes TEXT,
                rates TEXT,
                city TEXT,
                state TEXT NOT NULL,
                verified INTEGER DEFAULT 0,
                last_verified TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.conn.commit()
    
    def insert_hotel(self, hotel_data: Dict[str, Any]) -> int:
        """Insert new hotel record"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO hotels (name, address, city, state, pincode, contact, email, 
                              website, rating, price_min, price_max, price_avg, 
                              room_types, amenities, verified, last_verified)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            hotel_data.get('name'),
            hotel_data.get('address'),
            hotel_data.get('city'),
            hotel_data.get('state'),
            hotel_data.get('pincode'),
            hotel_data.get('contact'),
            hotel_data.get('email'),
            hotel_data.get('website'),
            hotel_data.get('rating', 0.0),
            hotel_data.get('price_min', 0),
            hotel_data.get('price_max', 0),
            hotel_data.get('price_avg', 0),
            hotel_data.get('room_types'),
            hotel_data.get('amenities'),
            hotel_data.get('verified', 0),
            datetime.now() if hotel_data.get('verified') else None
        ))
        self.conn.commit()
        return cursor.lastrowid
    
    def insert_tourist_place(self, place_data: Dict[str, Any]) -> int:
        """Insert new tourist place record"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO tourist_places (name, description, city, state, category,
                                      entry_fee, timings, best_season, how_to_reach,
                                      nearby_attractions, latitude, longitude, verified, last_verified)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            place_data.get('name'),
            place_data.get('description'),
            place_data.get('city'),
            place_data.get('state'),
            place_data.get('category'),
            place_data.get('entry_fee'),
            place_data.get('timings'),
            place_data.get('best_season'),
            place_data.get('how_to_reach'),
            place_data.get('nearby_attractions'),
            place_data.get('latitude'),
            place_data.get('longitude'),
            place_data.get('verified', 0),
            datetime.now() if place_data.get('verified') else None
        ))
        self.conn.commit()
        return cursor.lastrowid
    
    def get_all_hotels(self, state_filter: Optional[str] = None) -> List[Dict]:
        """Get all hotels with optional state filter"""
        cursor = self.conn.cursor()
        if state_filter:
            cursor.execute('SELECT * FROM hotels WHERE state = ? ORDER BY created_at DESC', (state_filter,))
        else:
            cursor.execute('SELECT * FROM hotels ORDER BY created_at DESC')
        
        return [dict(row) for row in cursor.fetchall()]
    
    def get_all_tourist_places(self, state_filter: Optional[str] = None) -> List[Dict]:
        """Get all tourist places with optional state filter"""
        cursor = self.conn.cursor()
        if state_filter:
            cursor.execute('SELECT * FROM tourist_places WHERE state = ? ORDER BY created_at DESC', (state_filter,))
        else:
            cursor.execute('SELECT * FROM tourist_places ORDER BY created_at DESC')
        
        return [dict(row) for row in cursor.fetchall()]
    
    def update_hotel_verification(self, hotel_id: int, verification_data: Dict[str, Any]):
        """Update hotel verification data"""
        cursor = self.conn.cursor()
        cursor.execute('''
            UPDATE hotels 
            SET rating = ?, price_min = ?, price_max = ?, price_avg = ?,
                verified = 1, last_verified = ?, updated_at = ?
            WHERE id = ?
        ''', (
            verification_data.get('rating', 0.0),
            verification_data.get('price_min', 0),
            verification_data.get('price_max', 0),
            verification_data.get('price_avg', 0),
            datetime.now(),
            datetime.now(),
            hotel_id
        ))
        self.conn.commit()
    
    def get_old_unverified_records(self, days: int = 30) -> List[Dict]:
        """Get records older than specified days for re-validation"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM hotels 
            WHERE last_verified IS NULL 
               OR julianday('now') - julianday(last_verified) > ?
            ORDER BY last_verified ASC
        ''', (days,))
        
        return [dict(row) for row in cursor.fetchall()]
    
    def check_duplicate(self, table: str, name: str, city: str, state: str) -> bool:
        """Check if record already exists"""
        cursor = self.conn.cursor()
        cursor.execute(f'SELECT COUNT(*) FROM {table} WHERE name = ? AND city = ? AND state = ?',
                      (name, city, state))
        count = cursor.fetchone()[0]
        return count > 0
    
    def close(self):
        """Close database connection"""
        self.conn.close()
