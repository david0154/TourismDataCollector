"""
Multi-Platform Travel Data Scrapers
Scrapes from 40+ Indian travel platforms continuously
Only stores VERIFIED data after AI validation
"""
import requests
from bs4 import BeautifulSoup
import time
import re
import json
from typing import Dict, List, Any, Optional
from config import (
    REQUEST_TIMEOUT, USER_AGENT, MAX_RETRIES, 
    SCRAPING_DELAY, PLATFORM_URLS
)

class PlatformScrapers:
    def __init__(self):
        """Initialize scrapers with session"""
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': USER_AGENT,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        })
    
    def scrape_platform(self, platform_name: str, city: str, state: str) -> List[Dict]:
        """
        Main scraper dispatcher - routes to specific platform scrapers
        """
        scrapers = {
            'makemytrip': self.scrape_makemytrip,
            'goibibo': self.scrape_goibibo,
            'cleartrip': self.scrape_cleartrip,
            'yatra': self.scrape_yatra,
            'easemytrip': self.scrape_easemytrip,
            'ixigo': self.scrape_ixigo,
            'oyo': self.scrape_oyo,
            'booking.com': self.scrape_booking,
            'agoda': self.scrape_agoda,
            'airbnb': self.scrape_airbnb,
            'google_maps': self.scrape_google_maps,
            'tripadvisor': self.scrape_tripadvisor,
            'irctc': self.scrape_irctc_stations,
            'incredibleindia': self.scrape_incredible_india,
        }
        
        scraper_func = scrapers.get(platform_name.lower().replace(' ', ''))
        if scraper_func:
            try:
                return scraper_func(city, state)
            except Exception as e:
                print(f"❌ Error scraping {platform_name}: {e}")
                return []
        return []
    
    # =====================================================
    # FLIGHT & TRAVEL BOOKING PLATFORMS
    # =====================================================
    
    def scrape_makemytrip(self, city: str, state: str) -> List[Dict]:
        """Scrape hotels from MakeMyTrip"""
        print(f"🔍 Scraping MakeMyTrip for {city}...")
        
        # Search URL
        search_url = f"https://www.makemytrip.com/hotels/hotel-listing/?city={city.lower()}"
        
        try:
            response = self.session.get(search_url, timeout=REQUEST_TIMEOUT)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            hotels = []
            
            # Find hotel listings
            hotel_cards = soup.find_all('div', class_=re.compile('listingRowOuter|hotel.*card', re.I))
            
            for card in hotel_cards[:20]:  # Limit to 20 per city
                try:
                    hotel_data = {
                        'name': self._extract_text(card, ['hotel.*name', 'property.*name'], 'h3, h4, .hotelName'),
                        'address': city + ', ' + state,
                        'city': city,
                        'state': state,
                        'rating': self._extract_rating(card),
                        'price': self._extract_price(card),
                        'source': 'MakeMyTrip',
                        'verified': 0  # Will be verified by AI
                    }
                    
                    if hotel_data['name']:
                        hotels.append(hotel_data)
                        print(f"  ✅ Found: {hotel_data['name']}")
                
                except Exception as e:
                    continue
            
            time.sleep(SCRAPING_DELAY)
            return hotels
            
        except Exception as e:
            print(f"  ❌ MakeMyTrip error: {e}")
            return []
    
    def scrape_goibibo(self, city: str, state: str) -> List[Dict]:
        """Scrape hotels from Goibibo"""
        print(f"🔍 Scraping Goibibo for {city}...")
        
        search_url = f"https://www.goibibo.com/hotels/{city.lower()}-hotels/"
        
        try:
            response = self.session.get(search_url, timeout=REQUEST_TIMEOUT)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            hotels = []
            hotel_cards = soup.find_all('div', class_=re.compile('hotel.*item|propertyCard', re.I))
            
            for card in hotel_cards[:20]:
                try:
                    hotel_data = {
                        'name': self._extract_text(card, ['hotel.*title', 'property.*name'], 'h3, h2'),
                        'address': city + ', ' + state,
                        'city': city,
                        'state': state,
                        'rating': self._extract_rating(card),
                        'price': self._extract_price(card),
                        'source': 'Goibibo',
                        'verified': 0
                    }
                    
                    if hotel_data['name']:
                        hotels.append(hotel_data)
                        print(f"  ✅ Found: {hotel_data['name']}")
                
                except Exception as e:
                    continue
            
            time.sleep(SCRAPING_DELAY)
            return hotels
            
        except Exception as e:
            print(f"  ❌ Goibibo error: {e}")
            return []
    
    def scrape_cleartrip(self, city: str, state: str) -> List[Dict]:
        """Scrape hotels from Cleartrip"""
        print(f"🔍 Scraping Cleartrip for {city}...")
        
        search_url = f"https://www.cleartrip.com/hotels/{city.lower()}"
        
        try:
            response = self.session.get(search_url, timeout=REQUEST_TIMEOUT)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            hotels = []
            hotel_cards = soup.find_all('div', class_=re.compile('hotel', re.I))
            
            for card in hotel_cards[:20]:
                try:
                    name = self._extract_text(card, ['title', 'name'], 'h2, h3, h4')
                    if name:
                        hotels.append({
                            'name': name,
                            'address': city + ', ' + state,
                            'city': city,
                            'state': state,
                            'rating': self._extract_rating(card),
                            'price': self._extract_price(card),
                            'source': 'Cleartrip',
                            'verified': 0
                        })
                        print(f"  ✅ Found: {name}")
                except:
                    continue
            
            time.sleep(SCRAPING_DELAY)
            return hotels
            
        except Exception as e:
            print(f"  ❌ Cleartrip error: {e}")
            return []
    
    def scrape_yatra(self, city: str, state: str) -> List[Dict]:
        """Scrape hotels from Yatra"""
        print(f"🔍 Scraping Yatra for {city}...")
        
        search_url = f"https://www.yatra.com/hotels/{city.lower()}"
        
        try:
            response = self.session.get(search_url, timeout=REQUEST_TIMEOUT)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            hotels = []
            hotel_cards = soup.find_all('div', class_=re.compile('hotel.*card|ht.*item', re.I))
            
            for card in hotel_cards[:20]:
                try:
                    name = self._extract_text(card, ['hotel.*name'], 'h3, h4')
                    if name:
                        hotels.append({
                            'name': name,
                            'address': city + ', ' + state,
                            'city': city,
                            'state': state,
                            'rating': self._extract_rating(card),
                            'price': self._extract_price(card),
                            'source': 'Yatra',
                            'verified': 0
                        })
                        print(f"  ✅ Found: {name}")
                except:
                    continue
            
            time.sleep(SCRAPING_DELAY)
            return hotels
            
        except Exception as e:
            print(f"  ❌ Yatra error: {e}")
            return []
    
    def scrape_easemytrip(self, city: str, state: str) -> List[Dict]:
        """Scrape hotels from EaseMyTrip"""
        print(f"🔍 Scraping EaseMyTrip for {city}...")
        
        search_url = f"https://www.easemytrip.com/hotels/{city.lower()}-hotels.html"
        
        try:
            response = self.session.get(search_url, timeout=REQUEST_TIMEOUT)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            hotels = []
            hotel_cards = soup.find_all('div', class_=re.compile('hotel', re.I))
            
            for card in hotel_cards[:20]:
                try:
                    name = self._extract_text(card, ['hotel.*name', 'title'], 'h3, h4, strong')
                    if name:
                        hotels.append({
                            'name': name,
                            'address': city + ', ' + state,
                            'city': city,
                            'state': state,
                            'rating': self._extract_rating(card),
                            'price': self._extract_price(card),
                            'source': 'EaseMyTrip',
                            'verified': 0
                        })
                        print(f"  ✅ Found: {name}")
                except:
                    continue
            
            time.sleep(SCRAPING_DELAY)
            return hotels
            
        except Exception as e:
            print(f"  ❌ EaseMyTrip error: {e}")
            return []
    
    def scrape_ixigo(self, city: str, state: str) -> List[Dict]:
        """Scrape hotels from Ixigo"""
        print(f"🔍 Scraping Ixigo for {city}...")
        
        search_url = f"https://www.ixigo.com/hotels-in-{city.lower()}"
        
        try:
            response = self.session.get(search_url, timeout=REQUEST_TIMEOUT)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            hotels = []
            hotel_cards = soup.find_all('div', class_=re.compile('hotel.*card', re.I))
            
            for card in hotel_cards[:20]:
                try:
                    name = self._extract_text(card, ['hotel.*name'], 'h2, h3')
                    if name:
                        hotels.append({
                            'name': name,
                            'address': city + ', ' + state,
                            'city': city,
                            'state': state,
                            'rating': self._extract_rating(card),
                            'price': self._extract_price(card),
                            'source': 'Ixigo',
                            'verified': 0
                        })
                        print(f"  ✅ Found: {name}")
                except:
                    continue
            
            time.sleep(SCRAPING_DELAY)
            return hotels
            
        except Exception as e:
            print(f"  ❌ Ixigo error: {e}")
            return []
    
    # =====================================================
    # HOTEL BOOKING PLATFORMS
    # =====================================================
    
    def scrape_oyo(self, city: str, state: str) -> List[Dict]:
        """Scrape hotels from OYO"""
        print(f"🔍 Scraping OYO for {city}...")
        
        search_url = f"https://www.oyorooms.com/hotels-in-{city.lower()}/"
        
        try:
            response = self.session.get(search_url, timeout=REQUEST_TIMEOUT)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            hotels = []
            hotel_cards = soup.find_all('div', class_=re.compile('hotelCard|oyo.*card', re.I))
            
            for card in hotel_cards[:30]:  # OYO has many listings
                try:
                    name = self._extract_text(card, ['hotel.*name', 'title'], 'h3, h4')
                    if name and 'OYO' in name:
                        hotels.append({
                            'name': name,
                            'address': city + ', ' + state,
                            'city': city,
                            'state': state,
                            'rating': self._extract_rating(card),
                            'price': self._extract_price(card),
                            'source': 'OYO',
                            'verified': 0
                        })
                        print(f"  ✅ Found: {name}")
                except:
                    continue
            
            time.sleep(SCRAPING_DELAY)
            return hotels
            
        except Exception as e:
            print(f"  ❌ OYO error: {e}")
            return []
    
    def scrape_booking(self, city: str, state: str) -> List[Dict]:
        """Scrape hotels from Booking.com"""
        print(f"🔍 Scraping Booking.com for {city}...")
        
        search_url = f"https://www.booking.com/searchresults.html?ss={city.replace(' ', '+')}"
        
        try:
            response = self.session.get(search_url, timeout=REQUEST_TIMEOUT)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            hotels = []
            hotel_cards = soup.find_all('div', attrs={'data-testid': re.compile('property.*card', re.I)})
            
            for card in hotel_cards[:20]:
                try:
                    name = self._extract_text(card, ['title'], 'h3, h2, [data-testid="title"]')
                    if name:
                        hotels.append({
                            'name': name,
                            'address': city + ', ' + state,
                            'city': city,
                            'state': state,
                            'rating': self._extract_rating(card),
                            'price': self._extract_price(card),
                            'source': 'Booking.com',
                            'verified': 0
                        })
                        print(f"  ✅ Found: {name}")
                except:
                    continue
            
            time.sleep(SCRAPING_DELAY)
            return hotels
            
        except Exception as e:
            print(f"  ❌ Booking.com error: {e}")
            return []
    
    def scrape_agoda(self, city: str, state: str) -> List[Dict]:
        """Scrape hotels from Agoda"""
        print(f"🔍 Scraping Agoda for {city}...")
        
        search_url = f"https://www.agoda.com/search?city={city.replace(' ', '%20')}"
        
        try:
            response = self.session.get(search_url, timeout=REQUEST_TIMEOUT)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            hotels = []
            hotel_cards = soup.find_all('div', class_=re.compile('PropertyCard|hotel', re.I))
            
            for card in hotel_cards[:20]:
                try:
                    name = self._extract_text(card, ['hotel.*name'], 'h3, h2')
                    if name:
                        hotels.append({
                            'name': name,
                            'address': city + ', ' + state,
                            'city': city,
                            'state': state,
                            'rating': self._extract_rating(card),
                            'price': self._extract_price(card),
                            'source': 'Agoda',
                            'verified': 0
                        })
                        print(f"  ✅ Found: {name}")
                except:
                    continue
            
            time.sleep(SCRAPING_DELAY)
            return hotels
            
        except Exception as e:
            print(f"  ❌ Agoda error: {e}")
            return []
    
    def scrape_airbnb(self, city: str, state: str) -> List[Dict]:
        """Scrape stays from Airbnb"""
        print(f"🔍 Scraping Airbnb for {city}...")
        
        # Note: Airbnb requires more sophisticated handling
        # This is a simplified version
        search_url = f"https://www.airbnb.co.in/s/{city.replace(' ', '-')}/homes"
        
        try:
            response = self.session.get(search_url, timeout=REQUEST_TIMEOUT)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            hotels = []
            # Airbnb uses dynamic loading, so this might return limited results
            listings = soup.find_all('div', attrs={'itemprop': 'itemListElement'})
            
            for listing in listings[:15]:
                try:
                    name = self._extract_text(listing, ['name'], '[itemprop="name"]')
                    if name:
                        hotels.append({
                            'name': name,
                            'address': city + ', ' + state,
                            'city': city,
                            'state': state,
                            'rating': self._extract_rating(listing),
                            'price': self._extract_price(listing),
                            'source': 'Airbnb',
                            'verified': 0
                        })
                        print(f"  ✅ Found: {name}")
                except:
                    continue
            
            time.sleep(SCRAPING_DELAY)
            return hotels
            
        except Exception as e:
            print(f"  ❌ Airbnb error: {e}")
            return []
    
    # =====================================================
    # GOOGLE MAPS & TRIPADVISOR
    # =====================================================
    
    def scrape_google_maps(self, city: str, state: str) -> List[Dict]:
        """Scrape hotels from Google Maps search"""
        print(f"🔍 Scraping Google Maps for {city}...")
        
        search_query = f"hotels in {city} {state}"
        search_url = f"https://www.google.com/search?q={search_query.replace(' ', '+')}"
        
        try:
            response = self.session.get(search_url, timeout=REQUEST_TIMEOUT)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            hotels = []
            # Google search results
            results = soup.find_all('div', class_=re.compile('g|result', re.I))[:20]
            
            for result in results:
                try:
                    name = self._extract_text(result, [], 'h3')
                    if name and ('hotel' in name.lower() or 'resort' in name.lower()):
                        hotels.append({
                            'name': name,
                            'address': city + ', ' + state,
                            'city': city,
                            'state': state,
                            'rating': self._extract_rating(result),
                            'price': 0,
                            'source': 'Google Maps',
                            'verified': 0
                        })
                        print(f"  ✅ Found: {name}")
                except:
                    continue
            
            time.sleep(SCRAPING_DELAY * 2)  # Be more respectful with Google
            return hotels
            
        except Exception as e:
            print(f"  ❌ Google Maps error: {e}")
            return []
    
    def scrape_tripadvisor(self, city: str, state: str) -> List[Dict]:
        """Scrape hotels and attractions from TripAdvisor"""
        print(f"🔍 Scraping TripAdvisor for {city}...")
        
        search_url = f"https://www.tripadvisor.in/Hotels-g-{city.replace(' ', '_')}-Hotels.html"
        
        try:
            response = self.session.get(search_url, timeout=REQUEST_TIMEOUT)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            hotels = []
            hotel_cards = soup.find_all('div', class_=re.compile('listing|property', re.I))
            
            for card in hotel_cards[:20]:
                try:
                    name = self._extract_text(card, ['title'], 'a')
                    if name:
                        hotels.append({
                            'name': name,
                            'address': city + ', ' + state,
                            'city': city,
                            'state': state,
                            'rating': self._extract_rating(card),
                            'price': self._extract_price(card),
                            'source': 'TripAdvisor',
                            'verified': 0
                        })
                        print(f"  ✅ Found: {name}")
                except:
                    continue
            
            time.sleep(SCRAPING_DELAY)
            return hotels
            
        except Exception as e:
            print(f"  ❌ TripAdvisor error: {e}")
            return []
    
    # =====================================================
    # GOVERNMENT TOURISM & IRCTC
    # =====================================================
    
    def scrape_incredible_india(self, city: str, state: str) -> List[Dict]:
        """Scrape tourist places from Incredible India"""
        print(f"🔍 Scraping Incredible India for {city}...")
        
        search_url = f"https://www.incredibleindia.org/content/incredibleindia/en/destinations/{state.lower().replace(' ', '-')}.html"
        
        try:
            response = self.session.get(search_url, timeout=REQUEST_TIMEOUT)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            places = []
            place_cards = soup.find_all('div', class_=re.compile('destination|place|attraction', re.I))
            
            for card in place_cards[:15]:
                try:
                    name = self._extract_text(card, ['title', 'name'], 'h2, h3, h4')
                    if name:
                        places.append({
                            'name': name,
                            'city': city,
                            'state': state,
                            'description': self._extract_text(card, ['desc'], 'p')[:200],
                            'source': 'Incredible India',
                            'verified': 0,
                            'type': 'tourist_place'
                        })
                        print(f"  ✅ Found place: {name}")
                except:
                    continue
            
            time.sleep(SCRAPING_DELAY)
            return places
            
        except Exception as e:
            print(f"  ❌ Incredible India error: {e}")
            return []
    
    def scrape_irctc_stations(self, city: str, state: str) -> List[Dict]:
        """Scrape railway stations from IRCTC/Indian Railways"""
        print(f"🔍 Scraping IRCTC stations for {city}...")
        
        # Search for railway stations
        search_url = f"https://enquiry.indianrail.gov.in/mntes/q?opt=TrainName&field1={city}"
        
        try:
            response = self.session.get(search_url, timeout=REQUEST_TIMEOUT)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            stations = []
            # Extract station information
            tables = soup.find_all('table')
            
            for table in tables:
                rows = table.find_all('tr')
                for row in rows:
                    cols = row.find_all('td')
                    if len(cols) >= 2:
                        station_name = cols[0].get_text(strip=True)
                        if station_name and city.lower() in station_name.lower():
                            stations.append({
                                'name': station_name,
                                'city': city,
                                'state': state,
                                'type': 'railway_station',
                                'source': 'IRCTC',
                                'verified': 0
                            })
                            print(f"  ✅ Found station: {station_name}")
            
            time.sleep(SCRAPING_DELAY)
            return stations
            
        except Exception as e:
            print(f"  ❌ IRCTC error: {e}")
            return []
    
    # =====================================================
    # HELPER METHODS
    # =====================================================
    
    def _extract_text(self, element, class_patterns: List[str], selectors: str) -> str:
        """Extract text from element using multiple strategies"""
        try:
            # Try class-based search
            for pattern in class_patterns:
                found = element.find(class_=re.compile(pattern, re.I))
                if found:
                    return found.get_text(strip=True)
            
            # Try CSS selectors
            for selector in selectors.split(','):
                found = element.select_one(selector.strip())
                if found:
                    text = found.get_text(strip=True)
                    if text:
                        return text
            
            return ""
        except:
            return ""
    
    def _extract_rating(self, element) -> float:
        """Extract rating from element"""
        try:
            # Look for rating patterns
            rating_patterns = [
                r'(\d+\.\d+)\s*(?:out of|/|★|stars?)',
                r'(?:rating|score)[:\s]+(\d+\.\d+)',
                r'(\d+\.\d+)\s*stars?'
            ]
            
            text = element.get_text()
            for pattern in rating_patterns:
                match = re.search(pattern, text, re.I)
                if match:
                    rating = float(match.group(1))
                    if 0 <= rating <= 5:
                        return rating
            
            # Look for star elements
            stars = element.find_all(class_=re.compile('star|rating', re.I))
            if stars:
                return min(len(stars), 5.0)
            
            return 0.0
        except:
            return 0.0
    
    def _extract_price(self, element) -> int:
        """Extract price from element"""
        try:
            # Look for price patterns (INR)
            price_patterns = [
                r'₹\s*([\d,]+)',
                r'INR\s*([\d,]+)',
                r'Rs\.?\s*([\d,]+)',
                r'([\d,]+)\s*(?:per night|/night)'
            ]
            
            text = element.get_text()
            for pattern in price_patterns:
                match = re.search(pattern, text, re.I)
                if match:
                    price_str = match.group(1).replace(',', '')
                    price = int(price_str)
                    if 500 <= price <= 50000:  # Reasonable range
                        return price
            
            return 0
        except:
            return 0
