"""
Search-Based Hotel Data Collector
Uses Google & DuckDuckGo to find hotels from all platforms
This ACTUALLY WORKS because we're not blocked by anti-bot protection
"""
import requests
from bs4 import BeautifulSoup
import time
import re
from typing import List, Dict
from config import REQUEST_TIMEOUT, SCRAPING_DELAY, USER_AGENT

class SearchBasedScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': USER_AGENT,
            'Accept': 'text/html,application/xhtml+xml',
            'Accept-Language': 'en-US,en;q=0.9',
        })
    
    def search_hotels_all_platforms(self, city: str, state: str) -> List[Dict]:
        """
        Search for hotels using Google & DuckDuckGo
        This finds hotels from ALL platforms in one search
        """
        print(f"\n🔍 Searching hotels in {city}, {state}...")
        
        all_hotels = []
        
        # Search queries for different platforms
        search_queries = [
            f"hotels in {city} {state} site:makemytrip.com",
            f"hotels in {city} {state} site:goibibo.com",
            f"hotels in {city} {state} site:oyorooms.com",
            f"hotels in {city} {state} site:booking.com",
            f"{city} {state} hotels",  # Generic search
            f"best hotels {city} {state}",
            f"top rated hotels {city}",
        ]
        
        for query in search_queries:
            try:
                # Try DuckDuckGo first (no rate limits)
                hotels = self._search_duckduckgo(query, city, state)
                all_hotels.extend(hotels)
                
                time.sleep(SCRAPING_DELAY)
                
            except Exception as e:
                print(f"  ⚠️ Search error: {e}")
        
        # Remove duplicates based on name
        unique_hotels = self._remove_duplicates(all_hotels)
        
        print(f"  ✅ Found {len(unique_hotels)} unique hotels")
        return unique_hotels
    
    def _search_duckduckgo(self, query: str, city: str, state: str) -> List[Dict]:
        """
        Search DuckDuckGo HTML (no rate limits, no blocking)
        """
        try:
            search_url = f"https://html.duckduckgo.com/html/?q={query.replace(' ', '+')}"
            
            response = self.session.get(search_url, timeout=REQUEST_TIMEOUT)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            hotels = []
            
            # Extract results
            results = soup.find_all('div', class_='result')
            
            for result in results[:10]:  # Top 10 results per query
                try:
                    # Extract title
                    title_elem = result.find('a', class_='result__a')
                    if not title_elem:
                        continue
                    
                    title = title_elem.get_text(strip=True)
                    
                    # Extract snippet
                    snippet_elem = result.find('a', class_='result__snippet')
                    snippet = snippet_elem.get_text(strip=True) if snippet_elem else ""
                    
                    # Extract URL to determine source
                    url = title_elem.get('href', '')
                    source = self._detect_source(url)
                    
                    # Extract hotel name from title
                    hotel_name = self._extract_hotel_name(title)
                    
                    if hotel_name:
                        # Extract rating from snippet
                        rating = self._extract_rating_from_text(snippet)
                        
                        # Extract price from snippet
                        price = self._extract_price_from_text(snippet)
                        
                        hotel_data = {
                            'name': hotel_name,
                            'city': city,
                            'state': state,
                            'address': f"{city}, {state}",
                            'rating': rating,
                            'price': price,
                            'source': source,
                            'description': snippet[:200],
                            'verified': 0  # Will be verified by AI
                        }
                        
                        hotels.append(hotel_data)
                        print(f"    ✅ Found: {hotel_name} ({source})")
                
                except Exception as e:
                    continue
            
            return hotels
            
        except Exception as e:
            print(f"    ❌ DuckDuckGo error: {e}")
            return []
    
    def _search_google(self, query: str, city: str, state: str) -> List[Dict]:
        """
        Search Google (backup method)
        """
        try:
            search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}&num=20"
            
            response = self.session.get(search_url, timeout=REQUEST_TIMEOUT)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            hotels = []
            
            # Extract search results
            results = soup.find_all('div', class_='g')
            
            for result in results:
                try:
                    # Title
                    title_elem = result.find('h3')
                    if not title_elem:
                        continue
                    
                    title = title_elem.get_text(strip=True)
                    
                    # Snippet
                    snippet_elem = result.find('div', class_=re.compile('VwiC3b|s3v9rd'))
                    snippet = snippet_elem.get_text(strip=True) if snippet_elem else ""
                    
                    # URL
                    link_elem = result.find('a')
                    url = link_elem.get('href', '') if link_elem else ''
                    source = self._detect_source(url)
                    
                    hotel_name = self._extract_hotel_name(title)
                    
                    if hotel_name:
                        rating = self._extract_rating_from_text(snippet + title)
                        price = self._extract_price_from_text(snippet + title)
                        
                        hotels.append({
                            'name': hotel_name,
                            'city': city,
                            'state': state,
                            'address': f"{city}, {state}",
                            'rating': rating,
                            'price': price,
                            'source': source,
                            'description': snippet[:200],
                            'verified': 0
                        })
                        
                        print(f"    ✅ Found: {hotel_name} ({source})")
                
                except:
                    continue
            
            return hotels
            
        except Exception as e:
            print(f"    ❌ Google error: {e}")
            return []
    
    def _extract_hotel_name(self, text: str) -> str:
        """
        Extract clean hotel name from search result title
        """
        # Remove common suffixes
        text = re.sub(r'\s*[-|:;].*$', '', text)  # Remove everything after - | : ;
        text = re.sub(r'\s*\(.*?\)', '', text)  # Remove parentheses
        text = re.sub(r'\s+in\s+.*$', '', text, flags=re.I)  # Remove "in City"
        text = re.sub(r'\s*,.*$', '', text)  # Remove comma and after
        
        # Remove platform names
        platforms = ['MakeMyTrip', 'Goibibo', 'OYO', 'Booking.com', 'Agoda', 'Cleartrip', 'Yatra']
        for platform in platforms:
            text = text.replace(platform, '').strip()
        
        # Clean up
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Only return if it looks like a hotel name
        if len(text) > 3 and not text.lower() in ['hotel', 'hotels', 'book', 'booking']:
            return text
        
        return ""
    
    def _extract_rating_from_text(self, text: str) -> float:
        """
        Extract rating from text
        """
        # Patterns for ratings
        patterns = [
            r'(\d+\.\d+)\s*(?:out of|/)\s*5',
            r'(\d+\.\d+)\s*★',
            r'(\d+\.\d+)\s*stars?',
            r'Rating[:\s]+(\d+\.\d+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.I)
            if match:
                rating = float(match.group(1))
                if 0 <= rating <= 5:
                    return rating
        
        return 0.0
    
    def _extract_price_from_text(self, text: str) -> int:
        """
        Extract price from text (INR)
        """
        patterns = [
            r'₹\s*([\d,]+)',
            r'INR\s*([\d,]+)',
            r'Rs\.?\s*([\d,]+)',
            r'([\d,]+)\s*(?:per night|/night)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.I)
            if match:
                price_str = match.group(1).replace(',', '')
                try:
                    price = int(price_str)
                    if 500 <= price <= 50000:
                        return price
                except:
                    continue
        
        return 0
    
    def _detect_source(self, url: str) -> str:
        """
        Detect platform from URL
        """
        url_lower = url.lower()
        
        if 'makemytrip' in url_lower:
            return 'MakeMyTrip'
        elif 'goibibo' in url_lower:
            return 'Goibibo'
        elif 'oyo' in url_lower:
            return 'OYO'
        elif 'booking.com' in url_lower:
            return 'Booking.com'
        elif 'agoda' in url_lower:
            return 'Agoda'
        elif 'cleartrip' in url_lower:
            return 'Cleartrip'
        elif 'yatra' in url_lower:
            return 'Yatra'
        elif 'airbnb' in url_lower:
            return 'Airbnb'
        elif 'tripadvisor' in url_lower:
            return 'TripAdvisor'
        else:
            return 'Google Search'
    
    def _remove_duplicates(self, hotels: List[Dict]) -> List[Dict]:
        """
        Remove duplicate hotels by name
        """
        seen = set()
        unique = []
        
        for hotel in hotels:
            name_lower = hotel['name'].lower().strip()
            if name_lower not in seen:
                seen.add(name_lower)
                unique.append(hotel)
        
        return unique
    
    def search_tourist_places(self, city: str, state: str) -> List[Dict]:
        """
        Search for tourist places/attractions
        """
        print(f"\n🏞️ Searching tourist places in {city}, {state}...")
        
        queries = [
            f"tourist places in {city} {state}",
            f"top attractions {city}",
            f"things to do {city} {state}",
            f"{city} sightseeing places",
        ]
        
        all_places = []
        
        for query in queries:
            try:
                places = self._search_places_duckduckgo(query, city, state)
                all_places.extend(places)
                time.sleep(SCRAPING_DELAY)
            except:
                continue
        
        unique_places = self._remove_duplicates(all_places)
        print(f"  ✅ Found {len(unique_places)} tourist places")
        return unique_places
    
    def _search_places_duckduckgo(self, query: str, city: str, state: str) -> List[Dict]:
        """
        Search for tourist places
        """
        try:
            search_url = f"https://html.duckduckgo.com/html/?q={query.replace(' ', '+')}"
            
            response = self.session.get(search_url, timeout=REQUEST_TIMEOUT)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            places = []
            results = soup.find_all('div', class_='result')[:15]
            
            for result in results:
                try:
                    title_elem = result.find('a', class_='result__a')
                    if not title_elem:
                        continue
                    
                    title = title_elem.get_text(strip=True)
                    
                    snippet_elem = result.find('a', class_='result__snippet')
                    description = snippet_elem.get_text(strip=True) if snippet_elem else ""
                    
                    # Clean title to get place name
                    place_name = re.sub(r'\s*[-|:;].*$', '', title)
                    place_name = re.sub(r'\s*\(.*?\)', '', place_name)
                    place_name = re.sub(r'\s+', ' ', place_name).strip()
                    
                    if place_name and len(place_name) > 3:
                        places.append({
                            'name': place_name,
                            'city': city,
                            'state': state,
                            'description': description[:300],
                            'category': self._detect_category(title + description),
                            'verified': 0,
                            'type': 'tourist_place'
                        })
                        print(f"    ✅ Found place: {place_name}")
                
                except:
                    continue
            
            return places
            
        except Exception as e:
            print(f"    ❌ Error: {e}")
            return []
    
    def _detect_category(self, text: str) -> str:
        """
        Detect category of tourist place
        """
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['fort', 'palace', 'temple', 'monument', 'historical']):
            return 'Historical'
        elif any(word in text_lower for word in ['museum', 'gallery', 'art']):
            return 'Museum'
        elif any(word in text_lower for word in ['park', 'garden', 'zoo', 'wildlife']):
            return 'Nature'
        elif any(word in text_lower for word in ['beach', 'lake', 'river', 'waterfall']):
            return 'Water Body'
        elif any(word in text_lower for word in ['mall', 'market', 'shopping']):
            return 'Shopping'
        elif any(word in text_lower for word in ['restaurant', 'food', 'cuisine']):
            return 'Food'
        else:
            return 'General'
