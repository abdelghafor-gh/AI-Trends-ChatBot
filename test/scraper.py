from bs4 import BeautifulSoup
import requests
import feedparser
from lxml import etree
import json
import pandas as pd
from pathlib import Path

class RSSFeedScraper:
    def __init__(self, output_dir="data"):
        """Initialize the RSS feed scraper with output directory."""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def fetch_feed(self, feed_url: str):
        """Fetch and parse the RSS feed."""
        try:
            response = requests.get(feed_url)
            response.raise_for_status()
            feed = feedparser.parse(response.text)
            return feed
        except requests.RequestException as e:
            print(f"Error fetching feed: {e}")
            return {}

    def save_feed_as_json(self, feed, filename):
        """Save feed data as JSON file."""
        try:
            # Convert feed to JSON-serializable format
            feed_json = json.loads(json.dumps(feed, default=str))
            
            # Create full output path
            output_path = self.output_dir / filename
            
            # Save feed as JSON file
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(feed_json, f, ensure_ascii=False, indent=4)
            
            print(f"Successfully saved feed to {output_path}")
            return feed_json
        except Exception as e:
            print(f"Error saving feed: {e}")
            return None

    def process_feed(self, feed_url: str, output_filename: str):
        """Process an RSS feed and save it to JSON."""
        feed = self.fetch_feed(feed_url)
        if feed:
            return self.save_feed_as_json(feed, output_filename)
        return None

def main():
    # Initialize scraper
    scraper = RSSFeedScraper()
    
    # Define feed URLs and their output filenames
    feeds = [
        ("https://www.amazon.science/index.rss", "amazon_science_feed.json"),
        ("https://deepmind.google/blog/rss.xml", "google_deepmind_feed.json"),
        ("https://news.mit.edu/topic/mitartificial-intelligence2-rss.xml", "mit_news.json"),
        ("https://techcrunch.com/tag/artificial-intelligence/feed/", "techcrunch_feed.json")
    ]
    
    # Process each feed
    for feed_url, output_filename in feeds:
        print(f"\nProcessing feed: {feed_url}")
        scraper.process_feed(feed_url, output_filename)

if __name__ == "__main__":
    main()
