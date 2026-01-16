"""
Web scraping utilities using BeautifulSoup
"""
import requests
from bs4 import BeautifulSoup
from typing import Dict, List, Optional
from config import REQUEST_TIMEOUT, USER_AGENT, MAX_RETRIES

class WebScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': USER_AGENT})
    
    def get_page(self, url: str) -> Optional[BeautifulSoup]:
        """Fetch and parse web page"""
        for attempt in range(MAX_RETRIES):
            try:
                response = self.session.get(url, timeout=REQUEST_TIMEOUT)
                if response.status_code == 200:
                    return BeautifulSoup(response.text, 'html.parser')
            except Exception as e:
                if attempt == MAX_RETRIES - 1:
                    print(f"Failed to fetch {url}: {e}")
        return None
    
    def extract_text(self, soup: BeautifulSoup, selector: str) -> str:
        """Extract text from element"""
        element = soup.select_one(selector)
        return element.get_text(strip=True) if element else ""
    
    def extract_all_text(self, soup: BeautifulSoup, selector: str) -> List[str]:
        """Extract text from all matching elements"""
        elements = soup.select(selector)
        return [el.get_text(strip=True) for el in elements]
