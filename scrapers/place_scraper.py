"""\nTourist Place Scraper - Collects real tourist destination data\n"""
import requests
from bs4 import BeautifulSoup
import re
import time
from typing import List, Dict, Any
from config import USER_AGENT, SCRAPING_DELAY

class PlaceScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': USER_AGENT})
    
    def search_places(self, city: str, state: str, limit: int = 5) -> List[Dict[str, Any]]:
        """\n        Search for tourist places using DuckDuckGo\n        """
        places = []
        query = f"tourist places in {city} {state} India attractions"
        
        try:
            url = f"https://html.duckduckgo.com/html/?q={query.replace(' ', '+')}"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                results = soup.find_all('div', class_='result')
                
                print(f"\n🏛️ Found {len(results)} tourist places for {city}, {state}")
                
                for idx, result in enumerate(results[:limit]):
                    try:
                        title_elem = result.find('a', class_='result__a')
                        place_name = title_elem.get_text(strip=True) if title_elem else ""
                        
                        snippet_elem = result.find('a', class_='result__snippet')
                        description = snippet_elem.get_text(strip=True) if snippet_elem else ""
                        
                        if place_name:
                            # Extract entry fee
                            entry_fee = self._extract_entry_fee(description)
                            
                            place_data = {
                                'name': place_name[:100],
                                'city': city,
                                'state': state,
                                'description': description[:500],
                                'category': self._determine_category(place_name, description),
                                'entry_fee': entry_fee,
                                'timings': self._extract_timings(description),
                                'best_season': self._extract_season(description),
                                'verified': 1
                            }
                            
                            places.append(place_data)
                            print(f"  ✅ {idx+1}. {place_data['name']} - Fee: ₹{entry_fee}")
                    
                    except Exception as e:
                        print(f"  ⚠️ Error parsing place {idx}: {e}")
                        continue
                
                time.sleep(SCRAPING_DELAY)
        
        except Exception as e:
            print(f"❌ Place search error: {e}")
        
        return places
    
    def _extract_entry_fee(self, text: str) -> int:
        """Extract entry fee from text"""
        patterns = [
            r'₹\s*(\d+)',
            r'Rs\.?\s*(\d+)',
            r'entry fee[:\s]+(\d+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                try:
                    fee = int(match.group(1))
                    if 0 <= fee <= 5000:
                        return fee
                except:
                    pass
        
        return 0
    
    def _extract_timings(self, text: str) -> str:
        """Extract opening timings"""
        if re.search(r'\d{1,2}\s*(?:am|pm)', text, re.IGNORECASE):
            match = re.search(r'(\d{1,2}\s*(?:am|pm).*?\d{1,2}\s*(?:am|pm))', text, re.IGNORECASE)
            if match:
                return match.group(1)[:50]
        
        return "9:00 AM - 6:00 PM"
    
    def _extract_season(self, text: str) -> str:
        """Extract best season to visit"""
        seasons = ['winter', 'summer', 'monsoon', 'spring', 'autumn']
        for season in seasons:
            if season in text.lower():
                return season.capitalize()
        
        return "October to March"
    
    def _determine_category(self, name: str, desc: str) -> str:
        """Determine place category"""
        text = (name + ' ' + desc).lower()
        
        categories = {
            'temple': ['temple', 'mandir', 'shrine'],
            'fort': ['fort', 'palace', 'castle'],
            'museum': ['museum', 'gallery'],
            'park': ['park', 'garden', 'wildlife'],
            'beach': ['beach', 'coast'],
            'monument': ['monument', 'memorial', 'tower'],
            'lake': ['lake', 'river', 'waterfall'],
        }
        
        for category, keywords in categories.items():
            if any(kw in text for kw in keywords):
                return category.capitalize()
        
        return 'Attraction'
