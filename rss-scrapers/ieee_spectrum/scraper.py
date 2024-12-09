from pathlib import Path
import sys
from typing import Dict, Any
import html
import requests
import json
from datetime import datetime
import logging
from bs4 import BeautifulSoup

# Add the parent directory to the Python path to import common module
parent_dir = str(Path(__file__).parent.parent)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from common.base_scraper import BaseRSSScraper

class IEEESpectrumScraper(BaseRSSScraper):
    """Scraper for IEEE Spectrum - AI articles."""
    
    def __init__(self):
        super().__init__(
            feed_url="https://spectrum.ieee.org/artificial-intelligence",
            source_name="ieee_spectrum"
        )
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def fetch_feed(self):
        """Fetch articles from IEEE Spectrum website."""
        try:
            response = requests.get(self.feed_url, headers=self.headers)
            response.raise_for_status()
            return response.text
        except Exception as e:
            logging.error(f"Error fetching IEEE Spectrum articles: {str(e)}")
            return None

    def get_latest_entries(self, limit=10):
        """Get latest entries from IEEE Spectrum.
        
        Args:
            limit: Maximum number of entries to return
            
        Returns:
            List of processed entries
        """
        html_content = self.fetch_feed()
        if not html_content:
            return []
            
        soup = BeautifulSoup(html_content, 'html.parser')
        article_elements = soup.select('article.article-preview')
        
        entries = []
        for article in article_elements[:limit]:
            entry = self._process_article(article)
            if entry:
                entries.append(entry)
        return entries
    
    def _process_article(self, article_element: BeautifulSoup) -> Dict[str, Any]:
        """Process IEEE Spectrum article element.
        
        Args:
            article_element: BeautifulSoup article element
            
        Returns:
            Processed article with standardized fields
        """
        try:
            # Extract basic information
            title_element = article_element.select_one('h2')
            link_element = article_element.select_one('a')
            description_element = article_element.select_one('.article-preview__description')
            date_element = article_element.select_one('time')
            author_element = article_element.select_one('.article-preview__author')
            image_element = article_element.select_one('img')
            
            processed = {
                'title': title_element.get_text(strip=True) if title_element else '',
                'link': f"https://spectrum.ieee.org{link_element['href']}" if link_element else '',
                'published_date': date_element['datetime'] if date_element else '',
                'description': description_element.get_text(strip=True) if description_element else '',
                'source': self.source_name,
                'id': link_element['href'].split('/')[-1] if link_element else '',
                'authors': [],
                'topics': [{'term': 'Artificial Intelligence'}],
                'media': []
            }
            
            # Extract authors
            if author_element:
                author_name = author_element.get_text(strip=True)
                if author_name:
                    processed['authors'].append({'name': author_name})
            
            # Extract image
            if image_element and image_element.get('src'):
                processed['media'].append({
                    'url': image_element['src'],
                    'type': 'image',
                    'caption': image_element.get('alt', '')
                })
                
            return processed
        except Exception as e:
            logging.error(f"Error processing IEEE Spectrum article: {str(e)}")
            return None

def main():
    # Initialize scraper
    scraper = IEEESpectrumScraper()
    
    # Define output path
    output_dir = Path(__file__).parent.parent.parent / "data" / "raw" / "ieee_spectrum"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "feed.json"
    
    # Fetch latest entries
    entries = scraper.get_latest_entries(limit=10)
    
    # Save to file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({'entries': entries}, f, indent=2, ensure_ascii=False)
    
    # Print sample of latest entries
    print("\nLatest IEEE Spectrum AI Articles:")
    for entry in entries[:3]:
        print(f"\nTitle: {entry['title']}")
        print(f"Published: {entry['published_date']}")
        if entry.get('authors'):
            authors = [author['name'] for author in entry['authors']]
            print(f"Authors: {', '.join(authors)}")
        print(f"Link: {entry['link']}")

if __name__ == "__main__":
    main()
