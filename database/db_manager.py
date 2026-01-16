"""
Database Manager with AUTO REVALIDATION support
Checks and re-validates old data every 7 days using AI
"""
import sqlite3
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import json
from config import DB_PATH, ENABLE_AUTO_REVALIDATION, REVALIDATION_INTERVAL_DAYS

class DatabaseManager:
    def __init__(self):
        """Initialize database with auto-revalidation support"""
        self.db_path = DB_PATH
        self.conn = None
        self.create_tables()
        print(f"\u2705 Database connected: {DB_PATH}")
        
        if ENABLE_AUTO_REVALIDATION:
            print(f"\u2705 Auto-revalidation enabled (every {REVALIDATION_INTERVAL_DAYS} days)")
    
    def get_connection(self):
        """Get database connection"""
        if self.conn is None:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row
        return self.conn
    
    def create_tables(self):
        """Create database tables with validation tracking"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Hotels table with validation fields
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
                price INTEGER DEFAULT 0,
                room_types TEXT,
                amenities TEXT,
                verified INTEGER DEFAULT 0,
                last_validated_at TEXT,
                validation_source TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tourist places with travel routes
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
                latitude REAL,
                longitude REAL,
                how_to_reach_air TEXT,
                how_to_reach_train TEXT,
                how_to_reach_road TEXT,
                distances TEXT,
                verified INTEGER DEFAULT 0,
                last_validated_at TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Travel services
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
                state TEXT,
                verified INTEGER DEFAULT 0,
                last_validated_at TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Validation log for tracking revalidation
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS validation_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                table_name TEXT NOT NULL,
                record_id INTEGER NOT NULL,
                validation_type TEXT,
                result TEXT,
                validated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
    
    def insert_hotel(self, hotel_data: Dict[str, Any]) -> int:
        """Insert hotel with validation timestamp"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        hotel_data['last_validated_at'] = datetime.now().isoformat()
        hotel_data['updated_at'] = datetime.now().isoformat()
        
        cursor.execute('''
            INSERT INTO hotels (
                name, address, city, state, pincode, contact, email, website,
                rating, price, room_types, amenities, verified, 
                last_validated_at, validation_source
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
            hotel_data.get('price', 0),
            hotel_data.get('room_types'),
            hotel_data.get('amenities'),
            hotel_data.get('verified', 0),
            hotel_data.get('last_validated_at'),
            hotel_data.get('validation_source', 'manual')
        ))
        
        conn.commit()
        return cursor.lastrowid
    
    def update_hotel(self, hotel_id: int, hotel_data: Dict[str, Any]) -> bool:
        """Update hotel data"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        hotel_data['updated_at'] = datetime.now().isoformat()
        hotel_data['last_validated_at'] = datetime.now().isoformat()
        
        cursor.execute('''
            UPDATE hotels SET
                name = ?, address = ?, city = ?, state = ?, contact = ?,
                email = ?, website = ?, rating = ?, price = ?, 
                verified = ?, last_validated_at = ?, updated_at = ?
            WHERE id = ?
        ''', (
            hotel_data.get('name'),
            hotel_data.get('address'),
            hotel_data.get('city'),
            hotel_data.get('state'),
            hotel_data.get('contact'),
            hotel_data.get('email'),
            hotel_data.get('website'),
            hotel_data.get('rating', 0.0),
            hotel_data.get('price', 0),
            hotel_data.get('verified', 0),
            hotel_data.get('last_validated_at'),
            hotel_data.get('updated_at'),
            hotel_id
        ))
        
        conn.commit()
        return cursor.rowcount > 0
    
    def get_all_hotels(self, state: Optional[str] = None) -> List[Dict]:
        """Get all hotels, optionally filtered by state"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if state:
            cursor.execute("SELECT * FROM hotels WHERE state = ?", (state,))
        else:
            cursor.execute("SELECT * FROM hotels")
        
        return [dict(row) for row in cursor.fetchall()]
    
    def get_hotels_needing_revalidation(self, days: int = 7) -> List[Dict]:
        """
        Get hotels that need revalidation (older than X days)
        For weekly automatic revalidation
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
        
        cursor.execute('''
            SELECT * FROM hotels 
            WHERE last_validated_at IS NULL 
            OR last_validated_at < ?
        ''', (cutoff_date,))
        
        return [dict(row) for row in cursor.fetchall()]
    
    def insert_tourist_place(self, place_data: Dict[str, Any]) -> int:
        """Insert tourist place with travel routes"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        place_data['last_validated_at'] = datetime.now().isoformat()
        
        cursor.execute('''
            INSERT INTO tourist_places (
                name, description, city, state, category, entry_fee, timings,
                best_season, latitude, longitude, how_to_reach_air, 
                how_to_reach_train, how_to_reach_road, distances, 
                verified, last_validated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            place_data.get('name'),
            place_data.get('description'),
            place_data.get('city'),
            place_data.get('state'),
            place_data.get('category'),
            place_data.get('entry_fee'),
            place_data.get('timings'),
            place_data.get('best_season'),
            place_data.get('latitude'),
            place_data.get('longitude'),
            json.dumps(place_data.get('how_to_reach_air', [])),
            json.dumps(place_data.get('how_to_reach_train', [])),
            json.dumps(place_data.get('how_to_reach_road', [])),
            json.dumps(place_data.get('distances', {})),
            place_data.get('verified', 0),
            place_data.get('last_validated_at')
        ))
        
        conn.commit()
        return cursor.lastrowid
    
    def get_all_tourist_places(self, state: Optional[str] = None) -> List[Dict]:
        """Get all tourist places"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if state:
            cursor.execute("SELECT * FROM tourist_places WHERE state = ?", (state,))
        else:
            cursor.execute("SELECT * FROM tourist_places")
        
        places = []
        for row in cursor.fetchall():
            place = dict(row)
            # Parse JSON fields
            for field in ['how_to_reach_air', 'how_to_reach_train', 'how_to_reach_road', 'distances']:
                if place.get(field):
                    try:
                        place[field] = json.loads(place[field])
                    except:
                        pass
            places.append(place)
        
        return places
    
    def log_validation(self, table_name: str, record_id: int, 
                      validation_type: str, result: str):
        """Log validation activity"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO validation_log (table_name, record_id, validation_type, result)
            VALUES (?, ?, ?, ?)
        ''', (table_name, record_id, validation_type, result))
        
        conn.commit()
    
    def check_duplicate(self, table: str, name: str, city: str, state: str) -> bool:
        """Check if record already exists"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(f'''
            SELECT COUNT(*) FROM {table} 
            WHERE name = ? AND city = ? AND state = ?
        ''', (name, city, state))
        
        count = cursor.fetchone()[0]
        return count > 0
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
