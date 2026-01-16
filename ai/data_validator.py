"""
AI-powered data validation with DuckDuckGo + Google verification
Scrapes data from internet WITHOUT opening browser frontend
"""
import re
import requests
from typing import Dict, Any, Tuple, List
from bs4 import BeautifulSoup
import json
from datetime import datetime, timedelta

class DataValidator:
    def __init__(self):
        """Initialize validator with internet access"""
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def validate_hotel_data(self, hotel_data: Dict[str, Any]) -> Tuple[bool, Dict[str, str]]:
        """Comprehensive hotel data validation"""
        errors = {}
        
        if not hotel_data.get('name'):
            errors['name'] = "Hotel name is required"
        
        if not hotel_data.get('city'):
            errors['city'] = "City is required"
        
        if not hotel_data.get('state'):
            errors['state'] = "State is required"
        
        contact = hotel_data.get('contact', '')
        if contact and not self._validate_phone(contact):
            errors['contact'] = "Invalid Indian phone number format"
        
        email = hotel_data.get('email', '')
        if email and not self._validate_email(email):
            errors['email'] = "Invalid email format"
        
        website = hotel_data.get('website', '')
        if website and not self._validate_url(website):
            errors['website'] = "Invalid website URL"
        
        rating = hotel_data.get('rating', 0)
        if rating < 0 or rating > 5:
            errors['rating'] = "Rating must be between 0 and 5"
        
        price = hotel_data.get('price', 0)
        if price < 0:
            errors['price'] = "Price cannot be negative"
        
        return len(errors) == 0, errors
    
    def verify_online_duckduckgo(self, query: str) -> Dict[str, Any]:
        """
        Verify data using DuckDuckGo (privacy-focused, no tracking)
        Backend scraping without opening browser
        """
        result = {
            'found': False,
            'rating': 0.0,
            'reviews_count': 0,
            'price_range': '',
            'source': 'DuckDuckGo'
        }
        
        try:
            # DuckDuckGo HTML search (no API key needed)
            search_url = f"https://html.duckduckgo.com/html/?q={query.replace(' ', '+')}"
            
            response = self.session.get(search_url, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Extract snippets
                snippets = soup.find_all('a', class_='result__snippet')
                if snippets:
                    result['found'] = True
                    
                    # Combine all text for analysis
                    text_content = ' '.join([s.get_text() for s in snippets[:5]])
                    
                    # Extract rating
                    rating_match = re.search(r'(\d\.\d)\s*(?:out of|/|★)\s*5', text_content)
                    if rating_match:
                        result['rating'] = float(rating_match.group(1))
                    
                    # Extract review count
                    reviews_match = re.search(r'(\d+)\s*(?:reviews?|ratings?)', text_content, re.IGNORECASE)
                    if reviews_match:
                        result['reviews_count'] = int(reviews_match.group(1))
                    
                    # Extract price
                    price_match = re.search(r'₹\s*(\d+,?\d*)', text_content)
                    if price_match:
                        result['price_range'] = f"₹{price_match.group(1)}"
        
        except Exception as e:
            print(f"DuckDuckGo verification error: {e}")
        
        return result
    
    def verify_online_google(self, query: str) -> Dict[str, Any]:
        """
        Verify data using Google Search (fallback)
        Backend scraping without opening browser
        """
        result = {
            'found': False,
            'rating': 0.0,
            'reviews_count': 0,
            'price_range': '',
            'source': 'Google'
        }
        
        try:
            search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            
            response = self.session.get(search_url, timeout=10)
            
            if response.status_code == 200:
                result['found'] = True
                text = response.text
                
                # Extract rating
                rating_match = re.search(r'(\d\.\d)\s*(?:out of|/|★)\s*5', text)
                if rating_match:
                    result['rating'] = float(rating_match.group(1))
                
                # Extract reviews
                reviews_match = re.search(r'([\d,]+)\s*(?:reviews?|ratings?)', text, re.IGNORECASE)
                if reviews_match:
                    result['reviews_count'] = int(reviews_match.group(1).replace(',', ''))
                
                # Extract price
                prices = re.findall(r'₹\s*(\d+,?\d*)', text)
                if prices:
                    result['price_range'] = f"₹{min(prices)} - ₹{max(prices)}"
        
        except Exception as e:
            print(f"Google verification error: {e}")
        
        return result
    
    def verify_hotel_online(self, hotel_name: str, city: str, state: str) -> Dict[str, Any]:
        """
        Verify hotel using both DuckDuckGo and Google
        Returns combined results
        """
        query = f"{hotel_name} {city} {state} hotel"
        
        # Try DuckDuckGo first (privacy-focused)
        result = self.verify_online_duckduckgo(query)
        
        # If DuckDuckGo doesn't find, try Google
        if not result['found']:
            result = self.verify_online_google(query)
        
        # Add verification metadata
        result['verified_at'] = datetime.now().isoformat()
        result['query'] = query
        
        return result
    
    def get_travel_routes(self, destination: str, state: str) -> Dict[str, Any]:
        """
        Collect 'how to reach' data for tourist destinations
        Backend scraping only
        """
        routes = {
            'by_air': [],
            'by_train': [],
            'by_road': [],
            'distances': {}
        }
        
        try:
            query = f"how to reach {destination} {state} by air train road"
            
            # Use DuckDuckGo for travel info
            search_url = f"https://html.duckduckgo.com/html/?q={query.replace(' ', '+')}"
            response = self.session.get(search_url, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                text = soup.get_text()
                
                # Extract airport info
                airport_match = re.findall(r'([A-Z][a-z]+)\s+(?:airport|Airport)', text)
                routes['by_air'] = list(set(airport_match))[:3]
                
                # Extract railway station info
                station_match = re.findall(r'([A-Z][a-z]+)\s+(?:railway station|station)', text)
                routes['by_train'] = list(set(station_match))[:3]
                
                # Extract distance info
                distance_match = re.findall(r'(\d+)\s*(?:km|kilometers?)', text, re.IGNORECASE)
                if distance_match:
                    routes['distances']['nearest_major_city'] = f"{distance_match[0]} km"
        
        except Exception as e:
            print(f"Travel route extraction error: {e}")
        
        return routes
    
    def get_hotel_pricing_updated(self, hotel_name: str, city: str) -> Dict[str, Any]:
        """
        Get latest hotel pricing from multiple sources
        """
        pricing = {
            'min_price': 0,
            'max_price': 0,
            'average_price': 0,
            'currency': 'INR',
            'updated_at': datetime.now().isoformat()
        }
        
        try:
            query = f"{hotel_name} {city} room price rate tariff"
            
            # Search both DuckDuckGo and Google for prices
            prices = []
            
            for search_func in [self.verify_online_duckduckgo, self.verify_online_google]:
                result = search_func(query)
                if result.get('price_range'):
                    # Extract numbers from price range
                    price_nums = re.findall(r'\d+', result['price_range'].replace(',', ''))
                    prices.extend([int(p) for p in price_nums if 500 <= int(p) <= 50000])
            
            if prices:
                pricing['min_price'] = min(prices)
                pricing['max_price'] = max(prices)
                pricing['average_price'] = sum(prices) // len(prices)
        
        except Exception as e:
            print(f"Pricing update error: {e}")
        
        return pricing
    
    def should_revalidate(self, last_validated: str, days: int = 7) -> bool:
        """
        Check if data should be revalidated based on age
        """
        if not last_validated:
            return True
        
        try:
            last_date = datetime.fromisoformat(last_validated)
            age = (datetime.now() - last_date).days
            return age >= days
        except:
            return True
    
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
