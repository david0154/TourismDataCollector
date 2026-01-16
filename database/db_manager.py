"""
SQLite database manager
"""
import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from config import DB_PATH

class DatabaseManager:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def init_database(self):
        """Initialize database with tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Hotels table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS hotels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            address TEXT,
            city TEXT,
            state TEXT,
            contact TEXT,
            email TEXT,
            website TEXT,
            room_types TEXT,
            rates TEXT,
            amenities TEXT,
            rating REAL,
            verified INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        # Tourist Places table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS tourist_places (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            city TEXT,
            state TEXT,
            category TEXT,
            entry_fee TEXT,
            timings TEXT,
            best_season TEXT,
            latitude REAL,
            longitude REAL,
            verified INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        # Travel Services table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS travel_services (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            service_type TEXT,
            provider_name TEXT,
            contact TEXT,
            email TEXT,
            website TEXT,
            routes TEXT,
            rates TEXT,
            state TEXT,
            verified INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        # Create indexes
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_hotels_state ON hotels(state)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_hotels_city ON hotels(city)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_places_state ON tourist_places(state)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_places_city ON tourist_places(city)")
        
        conn.commit()
        conn.close()
    
    def insert_hotel(self, hotel_data: Dict[str, Any]) -> int:
        """Insert hotel record"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
        INSERT INTO hotels (name, address, city, state, contact, email, website, 
                          room_types, rates, amenities, rating, verified)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            hotel_data.get('name'),
            hotel_data.get('address'),
            hotel_data.get('city'),
            hotel_data.get('state'),
            hotel_data.get('contact'),
            hotel_data.get('email'),
            hotel_data.get('website'),
            json.dumps(hotel_data.get('room_types', [])),
            json.dumps(hotel_data.get('rates', {})),
            json.dumps(hotel_data.get('amenities', [])),
            hotel_data.get('rating', 0.0),
            hotel_data.get('verified', 0)
        ))
        
        hotel_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return hotel_id
    
    def insert_tourist_place(self, place_data: Dict[str, Any]) -> int:
        """Insert tourist place record"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
        INSERT INTO tourist_places (name, description, city, state, category, 
                                   entry_fee, timings, best_season, latitude, longitude, verified)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            place_data.get('name'),
            place_data.get('description'),
            place_data.get('city'),
            place_data.get('state'),
            place_data.get('category'),
            place_data.get('entry_fee'),
            place_data.get('timings'),
            place_data.get('best_season'),
            place_data.get('latitude', 0.0),
            place_data.get('longitude', 0.0),
            place_data.get('verified', 0)
        ))
        
        place_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return place_id
    
    def get_all_hotels(self, state: Optional[str] = None) -> List[Dict]:
        """Retrieve all hotels, optionally filtered by state"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if state:
            cursor.execute("SELECT * FROM hotels WHERE state = ?", (state,))
        else:
            cursor.execute("SELECT * FROM hotels")
        
        columns = [description[0] for description in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        conn.close()
        return results
    
    def get_all_tourist_places(self, state: Optional[str] = None) -> List[Dict]:
        """Retrieve all tourist places, optionally filtered by state"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if state:
            cursor.execute("SELECT * FROM tourist_places WHERE state = ?", (state,))
        else:
            cursor.execute("SELECT * FROM tourist_places")
        
        columns = [description[0] for description in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        conn.close()
        return results
    
    def check_duplicate(self, table: str, name: str, city: str, state: str) -> bool:
        """Check if a record already exists"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(f"""
        SELECT COUNT(*) FROM {table} 
        WHERE name = ? AND city = ? AND state = ?
        """, (name, city, state))
        
        count = cursor.fetchone()[0]
        conn.close()
        
        return count > 0
