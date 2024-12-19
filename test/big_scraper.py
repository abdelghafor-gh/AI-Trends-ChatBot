from bs4 import BeautifulSoup
import requests
import feedparser
from lxml import etree
import json
import pandas as pd
from pathlib import Path

class RSSFeedScraper:
    def __init__(self, resources_file="resources.json", output_dir="big_data"):
        """Initialize the RSS feed scraper with resources file and output directory."""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.resources = self.load_resources(resources_file)

    def load_resources(self, resources_file):
        """Load RSS feed resources from JSON file."""
        try:
            with open(resources_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading resources: {e}")
            return {}

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
            feed_json = json.loads(json.dumps(feed, default=str))
            output_path = self.output_dir / filename
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(feed_json, f, ensure_ascii=False, indent=4)
            
            print(f"Successfully saved feed to {output_path}")
            return feed_json
        except Exception as e:
            print(f"Error saving feed: {e}")
            return None

    def process_feed(self, source_info, category):
        """Process an RSS feed and save it to JSON."""
        feed = self.fetch_feed(source_info['rss'])
        if feed:
            filename = f"{category}-{source_info['name'].lower().replace(' ', '_').replace('-', '')}_feed.json"
            return self.save_feed_as_json(feed, filename)
        return None

    def process_all_feeds(self):
        """Process all feeds from the resources file."""
        for category, sources in self.resources.items():
            print(f"\nProcessing {category} feeds:")
            for source_id, source_info in sources.items():
                print(f"\nFetching: {source_info['name']}")
                self.process_feed(source_info, category)

def main():
    scraper = RSSFeedScraper()
    scraper.process_all_feeds()

if __name__ == "__main__":
    main()