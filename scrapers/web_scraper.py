"""
Web Scraper - Backend only, NO browser frontend
Scrapes data silently in background using requests + BeautifulSoup
"""
import requests
from bs4 import BeautifulSoup
from typing import Dict, Any, List
import time
from config import REQUEST_TIMEOUT, USER_AGENT, MAX_RETRIES, SCRAPING_DELAY

class WebScraper:
    def __init__(self):
        """Initialize scraper with session"""
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': USER_AGENT})
    
    def scrape_page(self, url: str) -> str:
        """
        Scrape page content (backend only, no browser window)
        """
        for attempt in range(MAX_RETRIES):
            try:
                response = self.session.get(url, timeout=REQUEST_TIMEOUT)
                response.raise_for_status()
                
                # Delay to be respectful
                time.sleep(SCRAPING_DELAY)
                
                return response.text
            except Exception as e:
                print(f"Scraping attempt {attempt + 1} failed: {e}")
                if attempt < MAX_RETRIES - 1:
                    time.sleep(SCRAPING_DELAY * 2)
        
        return ""
    
    def extract_data(self, html: str, selectors: Dict[str, str]) -> Dict[str, Any]:
        """
        Extract data from HTML using CSS selectors
        """
        soup = BeautifulSoup(html, 'html.parser')
        data = {}
        
        for key, selector in selectors.items():
            element = soup.select_one(selector)
            data[key] = element.get_text(strip=True) if element else ""
        
        return data
