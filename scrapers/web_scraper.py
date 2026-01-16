"""
Web scraping utilities
"""
import requests
from bs4 import BeautifulSoup
from typing import Optional
from config import REQUEST_TIMEOUT, USER_AGENT

class WebScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': USER_AGENT})
    
    def fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        """Fetch and parse a web page"""
        try:
            response = self.session.get(url, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'lxml')
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None
    
    def extract_text(self, soup: BeautifulSoup, selector: str) -> str:
        """Extract text from HTML using CSS selector"""
        element = soup.select_one(selector)
        return element.get_text(strip=True) if element else ""
    
    def extract_all(self, soup: BeautifulSoup, selector: str) -> list:
        """Extract all matching elements"""
        return [elem.get_text(strip=True) for elem in soup.select(selector)]
