"""
Database models for tourism data
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Hotel:
    id: Optional[int] = None
    name: str = ""
    address: str = ""
    city: str = ""
    state: str = ""
    contact: str = ""
    email: str = ""
    website: str = ""
    room_types: str = ""  # JSON string
    rates: str = ""  # JSON string
    amenities: str = ""  # JSON string
    rating: float = 0.0
    verified: bool = False
    created_at: datetime = None
    updated_at: datetime = None

@dataclass
class TouristPlace:
    id: Optional[int] = None
    name: str = ""
    description: str = ""
    city: str = ""
    state: str = ""
    category: str = ""  # Historical, Religious, Adventure, etc.
    entry_fee: str = ""
    timings: str = ""
    best_season: str = ""
    latitude: float = 0.0
    longitude: float = 0.0
    verified: bool = False
    created_at: datetime = None
    updated_at: datetime = None

@dataclass
class TravelService:
    id: Optional[int] = None
    service_type: str = ""  # Cab, Bus, Train, Flight
    provider_name: str = ""
    contact: str = ""
    email: str = ""
    website: str = ""
    routes: str = ""  # JSON string
    rates: str = ""  # JSON string
    state: str = ""
    verified: bool = False
    created_at: datetime = None
    updated_at: datetime = None
