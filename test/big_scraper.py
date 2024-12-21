from bs4 import BeautifulSoup
import requests
import feedparser
from lxml import etree
import json
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
import pytz
import re

class RSSFeedScraper:
    def __init__(self, resources_file="resources.json", output_dir="raw"):
        """Initialize the RSS feed scraper with resources file and output directory."""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.resources = self.load_resources(resources_file)
        self.current_time = datetime.now(pytz.UTC)
        self.cutoff_time = self.current_time - timedelta(hours=24)
        self.all_entries = []

    def load_resources(self, resources_file):
        """Load RSS feed resources from JSON file."""
        try:
            with open(resources_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading resources: {e}")
            return {}

    def parse_date(self, date_str):
        """Parse date string to UTC datetime object."""
        try:
            dt = pd.to_datetime(date_str)
            # Convert to UTC if timezone-naive
            if dt.tz is None:
                dt = dt.tz_localize('UTC')
            else:
                dt = dt.tz_convert('UTC')
            return dt
        except:
            return None

    def fetch_feed(self, feed_url: str):
        """Fetch and parse the RSS feed."""
        try:
            response = requests.get(feed_url)
            response.raise_for_status()
            feed = feedparser.parse(response.text)
            
            # Filter entries from last 24 hours
            filtered_entries = []
            for entry in feed.entries:
                published = entry.get('published', entry.get('pubDate', ''))
                pub_date = self.parse_date(published)
                
                if pub_date is not None and pub_date >= self.cutoff_time:
                    filtered_entries.append(entry)
            
            feed.entries = filtered_entries
            return feed
        except requests.RequestException as e:
            print(f"Error fetching feed: {e}")
            return {}

    def clean_html(self, html_text):
        """Clean HTML content from text."""
        if not html_text:
            return ""
        
        # Parse HTML with BeautifulSoup
        soup = BeautifulSoup(html_text, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
            
        # Get text content
        text = soup.get_text(separator=' ')
        
        # Clean up whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Remove URLs
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
        
        # Remove email addresses
        text = re.sub(r'[\w\.-]+@[\w\.-]+\.\w+', '', text)
        
        # Clean up any remaining special characters
        text = re.sub(r'[^\w\s.,!?-]', '', text)
        
        # Remove extra whitespace again
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text

    def process_feed(self, source_info, category):
        """Process an RSS feed and add entries to the combined list."""
        feed = self.fetch_feed(source_info['rss'])
        if feed and 'entries' in feed:
            # Add source info to each entry
            for entry in feed.entries:
                entry_dict = {
                    'source_category': category,
                    'source_name': source_info['name'],
                    'source_url': source_info['url'],
                    'title': entry.get('title', ''),
                    'link': entry.get('link', ''),
                    'description': self.clean_html(entry.get('summary', entry.get('description', ''))),
                    'published_date': entry.get('published', entry.get('pubDate', '')),
                    'author': self.clean_html(entry.get('author', '')),
                    'tags': [self.clean_html(tag.get('term', '')) for tag in entry.get('tags', [])]
                }
                self.all_entries.append(entry_dict)

    def process_all_feeds(self):
        """Process all feeds and save to a single daily file."""
        for category, sources in self.resources.items():
            print(f"\nProcessing {category} feeds:")
            for source_id, source_info in sources.items():
                print(f"\nFetching: {source_info['name']}")
                self.process_feed(source_info, category)
        
        # Save all entries to a single daily file
        if self.all_entries:
            # Use only date for filename (not time)
            date_str = self.current_time.strftime('%Y-%m-%d')
            output_file = self.output_dir / f'{date_str}.json'
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'date': date_str,
                    'last_updated': self.current_time.isoformat(),
                    'entries_count': len(self.all_entries),
                    'entries': sorted(self.all_entries, 
                                   key=lambda x: pd.to_datetime(x['published_date'], utc=True), 
                                   reverse=True)
                }, f, ensure_ascii=False, indent=4)
            
            print(f"\nSaved {len(self.all_entries)} entries to {output_file}")

def main():
    scraper = RSSFeedScraper()
    scraper.process_all_feeds()

if __name__ == "__main__":
    main()