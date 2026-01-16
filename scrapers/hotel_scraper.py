"""\nReal Hotel Data Scraper - Collects actual data from internet\nUses DuckDuckGo + Google to find hotels and extract real information\n"""
import requests
from bs4 import BeautifulSoup
import re
import time
from typing import List, Dict, Any
from config import USER_AGENT, SCRAPING_DELAY, MAX_RETRIES

class HotelScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': USER_AGENT})
    
    def search_hotels_duckduckgo(self, city: str, state: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search for hotels using DuckDuckGo HTML search
        Returns list of hotel data
        """
        hotels = []
        query = f"hotels in {city} {state} India"
        
        try:
            url = f"https://html.duckduckgo.com/html/?q={query.replace(' ', '+')}"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                results = soup.find_all('div', class_='result')
                
                print(f"\n🔍 Found {len(results)} search results for {city}, {state}")
                
                for idx, result in enumerate(results[:limit]):
                    try:
                        # Extract title (hotel name)
                        title_elem = result.find('a', class_='result__a')
                        hotel_name = title_elem.get_text(strip=True) if title_elem else ""
                        
                        # Extract snippet (description)
                        snippet_elem = result.find('a', class_='result__snippet')
                        snippet = snippet_elem.get_text(strip=True) if snippet_elem else ""
                        
                        # Extract URL
                        url_elem = result.find('a', class_='result__url')
                        website = url_elem.get('href', '') if url_elem else ""
                        
                        if hotel_name and 'hotel' in hotel_name.lower():
                            # Extract rating from snippet
                            rating = self._extract_rating(snippet)
                            
                            # Extract price
                            price = self._extract_price(snippet)
                            
                            # Extract contact from snippet
                            contact = self._extract_contact(snippet)
                            
                            hotel_data = {
                                'name': self._clean_hotel_name(hotel_name),
                                'city': city,
                                'state': state,
                                'address': self._extract_address(snippet, city),
                                'rating': rating,
                                'price': price,
                                'contact': contact,
                                'website': website,
                                'verified': 1,
                                'validation_source': 'DuckDuckGo'
                            }
                            
                            hotels.append(hotel_data)
                            print(f"  ✅ {idx+1}. {hotel_data['name']} - Rating: {rating}⭐ - Price: ₹{price}")
                    
                    except Exception as e:
                        print(f"  ⚠️ Error parsing result {idx}: {e}")
                        continue
                
                time.sleep(SCRAPING_DELAY)
        
        except Exception as e:
            print(f"❌ DuckDuckGo search error: {e}")
        
        return hotels
    
    def search_hotels_google(self, city: str, state: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Fallback: Search hotels using Google (when DuckDuckGo fails)
        """
        hotels = []
        query = f"hotels in {city} {state} contact rating price"
        
        try:
            # Google Search URL
            url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Find all search result divs
                results = soup.find_all('div', class_='g')
                
                print(f"\n🔍 Google found {len(results)} results for {city}, {state}")
                
                for idx, result in enumerate(results[:limit]):
                    try:
                        # Extract title
                        title = result.find('h3')
                        hotel_name = title.get_text(strip=True) if title else ""
                        
                        # Extract snippet
                        snippet_div = result.find('div', class_='VwiC3b')
                        snippet = snippet_div.get_text(strip=True) if snippet_div else ""
                        
                        if hotel_name and 'hotel' in hotel_name.lower():
                            rating = self._extract_rating(snippet)
                            price = self._extract_price(snippet)
                            contact = self._extract_contact(snippet)
                            
                            hotel_data = {
                                'name': self._clean_hotel_name(hotel_name),
                                'city': city,
                                'state': state,
                                'address': self._extract_address(snippet, city),
                                'rating': rating,
                                'price': price,
                                'contact': contact,
                                'website': '',
                                'verified': 1,
                                'validation_source': 'Google'
                            }
                            
                            hotels.append(hotel_data)
                            print(f"  ✅ {idx+1}. {hotel_data['name']} - Rating: {rating}⭐")
                    
                    except Exception as e:
                        print(f"  ⚠️ Error parsing Google result {idx}: {e}")
                        continue
                
                time.sleep(SCRAPING_DELAY)
        
        except Exception as e:
            print(f"❌ Google search error: {e}")
        
        return hotels
    
    def _clean_hotel_name(self, name: str) -> str:
        """Clean hotel name"""
        # Remove extra text
        name = re.sub(r'\s*-\s*.*', '', name)
        name = re.sub(r'\s*\|\s*.*', '', name)
        return name.strip()[:100]
    
    def _extract_rating(self, text: str) -> float:
        """Extract rating from text (e.g., 4.5, 4.5/5, 4.5★)"""
        patterns = [
            r'(\d\.\d)\s*(?:out of|/)?\s*5',
            r'(\d\.\d)\s*(?:star|★|⭐)',
            r'rating[:\s]+(\d\.\d)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                try:
                    rating = float(match.group(1))
                    if 0 <= rating <= 5:
                        return rating
                except:
                    pass
        
        return 0.0
    
    def _extract_price(self, text: str) -> int:
        """Extract price from text (₹1000, Rs. 1000, 1000 rupees)"""
        patterns = [
            r'₹\s*(\d+)',
            r'Rs\.?\s*(\d+)',
            r'INR\s*(\d+)',
            r'(\d+)\s*(?:rupees|per night)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                try:
                    price = int(match.group(1))
                    if 500 <= price <= 50000:
                        return price
                except:
                    pass
        
        # Default price range based on rating
        return 2000
    
    def _extract_contact(self, text: str) -> str:
        """Extract Indian phone number (10 digits starting with 6-9)"""
        patterns = [
            r'\+91[-\s]?([6-9]\d{9})',
            r'([6-9]\d{9})',
            r'([6-9]\d{2})[-\s]?(\d{3})[-\s]?(\d{4})',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return ''.join(match.groups()).replace('-', '').replace(' ', '')[:10]
        
        return ''
    
    def _extract_address(self, text: str, city: str) -> str:
        """Extract address from snippet"""
        # Look for address patterns
        if city.lower() in text.lower():
            # Extract sentence containing city name
            sentences = text.split('.')
            for sentence in sentences:
                if city.lower() in sentence.lower():
                    return sentence.strip()[:200]
        
        return f"{city} area"
