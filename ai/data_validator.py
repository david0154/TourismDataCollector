"""
AI-powered data validation using open-source models
"""
import re
import requests
from typing import Dict, Any, Tuple
from transformers import pipeline
import torch

class DataValidator:
    def __init__(self):
        # Use lightweight open-source model for validation
        self.device = 0 if torch.cuda.is_available() else -1
        
    def validate_hotel_data(self, hotel_data: Dict[str, Any]) -> Tuple[bool, Dict[str, str]]:
        """
        Validate hotel data comprehensively
        Returns: (is_valid, errors_dict)
        """
        errors = {}
        
        # Required fields
        if not hotel_data.get('name'):
            errors['name'] = "Hotel name is required"
        
        if not hotel_data.get('city'):
            errors['city'] = "City is required"
        
        if not hotel_data.get('state'):
            errors['state'] = "State is required"
        
        # Contact validation
        contact = hotel_data.get('contact', '')
        if contact and not self._validate_phone(contact):
            errors['contact'] = "Invalid phone number format"
        
        # Email validation
        email = hotel_data.get('email', '')
        if email and not self._validate_email(email):
            errors['email'] = "Invalid email format"
        
        # URL validation
        website = hotel_data.get('website', '')
        if website and not self._validate_url(website):
            errors['website'] = "Invalid website URL"
        
        # Rating validation
        rating = hotel_data.get('rating', 0)
        if rating < 0 or rating > 5:
            errors['rating'] = "Rating must be between 0 and 5"
        
        return len(errors) == 0, errors
    
    def validate_tourist_place(self, place_data: Dict[str, Any]) -> Tuple[bool, Dict[str, str]]:
        """Validate tourist place data"""
        errors = {}
        
        if not place_data.get('name'):
            errors['name'] = "Place name is required"
        
        if not place_data.get('city'):
            errors['city'] = "City is required"
        
        if not place_data.get('state'):
            errors['state'] = "State is required"
        
        # Validate coordinates if provided
        lat = place_data.get('latitude', 0)
        lon = place_data.get('longitude', 0)
        
        if lat != 0 and (lat < -90 or lat > 90):
            errors['latitude'] = "Invalid latitude"
        
        if lon != 0 and (lon < -180 or lon > 180):
            errors['longitude'] = "Invalid longitude"
        
        return len(errors) == 0, errors
    
    def _validate_phone(self, phone: str) -> bool:
        """Validate Indian phone number"""
        cleaned = re.sub(r'[^\d]', '', phone)
        return bool(re.match(r'^[6-9]\d{9}$', cleaned))
    
    def _validate_email(self, email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    def _validate_url(self, url: str) -> bool:
        """Validate URL format"""
        pattern = r'^https?://[^\s/$.?#].[^\s]*$'
        return bool(re.match(pattern, url))
    
    def verify_online(self, data_type: str, name: str, location: str) -> bool:
        """
        Verify data existence online using search
        Returns True if data seems legitimate
        """
        try:
            # Simple verification using search
            query = f"{name} {location} {data_type}"
            # In production, implement actual search API or scraping
            return True  # Placeholder
        except:
            return False
