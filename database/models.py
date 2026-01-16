"""
Data models for tourism entities
"""
from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Hotel:
    name: str
    city: str
    state: str
    address: Optional[str] = None
    pincode: Optional[str] = None
    contact: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    rating: float = 0.0
    price_min: int = 0
    price_max: int = 0
    price_avg: int = 0
    room_types: Optional[str] = None
    amenities: Optional[str] = None
    verified: int = 0
    id: Optional[int] = None

@dataclass
class TouristPlace:
    name: str
    city: str
    state: str
    description: Optional[str] = None
    category: Optional[str] = None
    entry_fee: Optional[int] = None
    timings: Optional[str] = None
    best_season: Optional[str] = None
    how_to_reach: Optional[str] = None
    nearby_attractions: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    verified: int = 0
    id: Optional[int] = None
