import feedparser
from datetime import datetime
import json
from typing import Dict, List, Optional
import html
import requests
from pathlib import Path
import logging
from pprint import pformat
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import OperationFailure

class BaseRSSScraper:
    """Base class for RSS feed scrapers."""
    
    def __init__(self, feed_url: str, source_name: str):
        """Initialize the RSS feed scraper.
        
        Args:
            feed_url (str): URL of the RSS feed
            source_name (str): Name of the source (e.g., 'amazon_science')
        """
        self.feed_url = feed_url
        self.source_name = source_name
        self._setup_logging()
        self._setup_mongodb()
    
    def _setup_logging(self):
        """Set up logging for the scraper."""
        self.logger = logging.getLogger(f"rss_scraper.{self.source_name}")
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)
    
    def _load_mongodb_schema(self):
        """Load MongoDB schema from schema.json file."""
        try:
            schema_path = Path(__file__).parent / "schema.json"
            with open(schema_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Error loading MongoDB schema: {e}")
            return None
    
    def _setup_mongodb(self):
        """Set up MongoDB connection and ensure schema validation."""
        try:
            load_dotenv()
            self.mongo_uri = os.getenv("MONGO_URI")
            self.db_name = os.getenv("MONGO_DB_NAME", "ai_trends")
            self.collection_name = os.getenv("MONGO_COLLECTION_NAME", "rss_feeds")
            
            if not self.mongo_uri:
                self.logger.error("MongoDB URI not found in environment variables")
                return
            
            self.client = MongoClient(self.mongo_uri)
            self.db = self.client[self.db_name]
            
            # Create collection with schema validation if it doesn't exist
            if self.collection_name not in self.db.list_collection_names():
                schema = self._load_mongodb_schema()
                if schema:
                    self.db.create_collection(self.collection_name, **schema)
                else:
                    self.logger.error("Failed to load MongoDB schema, collection will be created without validation")
                    self.db.create_collection(self.collection_name)
            
            self.collection = self.db[self.collection_name]
            self.logger.info(f"Successfully connected to MongoDB: {self.db_name}.{self.collection_name}")
            
        except ConnectionError as e:
            self.logger.error(f"Failed to connect to MongoDB: {e}")
            self.client = None
        except Exception as e:
            self.logger.error(f"Error setting up MongoDB: {e}")
            self.client = None
    
    def inspect_feed_structure(self, sample_size: int = 1) -> None:
        """Inspect and log the structure of the RSS feed.
        
        Args:
            sample_size (int): Number of entries to inspect
        """
        try:
            response = requests.get(self.feed_url)
            response.raise_for_status()
            feed = feedparser.parse(response.text)
            
            # Log feed metadata structure
            self.logger.info("Feed Metadata Structure:")
            feed_meta = {k: v for k, v in feed.feed.items() if k not in ['entries']}
            self.logger.info(pformat(feed_meta))
            
            # Log entry structure for sample entries
            if feed.entries:
                self.logger.info(f"\nSample Entry Structure (first {sample_size} entries):")
                for i, entry in enumerate(feed.entries[:sample_size]):
                    self.logger.info(f"\nEntry {i+1}:")
                    self.logger.info(pformat(entry))
            
        except Exception as e:
            self.logger.error(f"Error inspecting feed structure: {e}")
    
    def fetch_feed(self) -> Dict:
        """Fetch and parse the RSS feed."""
        try:
            self.logger.info(f"Fetching feed from {self.feed_url}")
            response = requests.get(self.feed_url)
            response.raise_for_status()
            feed = feedparser.parse(response.text)
            print(feed)
            exit()
            return self._process_feed(feed)
        except requests.RequestException as e:
            self.logger.error(f"Error fetching feed: {e}")
            return {}

    def _process_feed(self, feed: feedparser.FeedParserDict) -> Dict:
        """Process the feed and extract relevant information."""
        feed_info = {
            "feed_title": feed.feed.get("title", ""),
            "feed_link": feed.feed.get("link", ""),
            "feed_description": feed.feed.get("description", ""),
            "feed_language": feed.feed.get("language", ""),
            "last_updated": feed.feed.get("updated", ""),
            "source": self.source_name,
            "scrape_date": datetime.utcnow().isoformat(),
            "entries": []
        }

        for entry in feed.entries:
            processed_entry = self._process_entry(entry)
            feed_info["entries"].append(processed_entry)

        self.logger.info(f"Processed {len(feed_info['entries'])} entries")
        return feed_info

    def _process_entry(self, entry: Dict) -> Dict:
        """Process a single feed entry."""
        description = html.unescape(entry.get("description", ""))
        
        # Try different date fields that might be present
        date_fields = ["published", "updated", "pubDate", "date"]
        pub_date = None
        for field in date_fields:
            pub_date = entry.get(field, "")
            if pub_date:
                break
        
        try:
            if pub_date:
                # Try different date formats
                date_formats = [
                    "%a, %d %b %Y %H:%M:%S %Z",
                    "%Y-%m-%dT%H:%M:%S%z",
                    "%Y-%m-%dT%H:%M:%SZ",
                    "%Y-%m-%d %H:%M:%S"
                ]
                for fmt in date_formats:
                    try:
                        dt = datetime.strptime(pub_date, fmt)
                        pub_date = dt.isoformat()
                        break
                    except ValueError:
                        continue
        except Exception as e:
            self.logger.warning(f"Could not parse date: {pub_date} - {e}")

        return {
            "title": entry.get("title", ""),
            "link": entry.get("link", ""),
            "description": description,
            "published_date": pub_date,
            "guid": entry.get("guid", ""),
            "categories": entry.get("tags", []),
            "author": entry.get("author", "")
        }

    def save_to_json(self, base_path: str):
        """Save the scraped feed data to a JSON file with date-based organization.
        
        Args:
            base_path (str): Base path for saving files
        """
        feed_data = self.fetch_feed()
        if not feed_data:
            return
        
        # Create date-based directory structure
        now = datetime.utcnow()
        date_path = now.strftime("%Y/%m/%d")
        output_dir = Path(base_path) / self.source_name / date_path
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create filename with timestamp
        timestamp = now.strftime("%Y%m%d_%H%M%S")
        output_file = output_dir / f"feed_{timestamp}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(feed_data, f, indent=2, ensure_ascii=False)
        self.logger.info(f"Feed data saved to {output_file}")
        
    def save_to_mongodb(self) -> bool:
        """Save the scraped feed data to MongoDB.
        
        Returns:
            bool: True if save was successful, False otherwise
        """
        if not hasattr(self, 'client') or not self.client:
            self.logger.error("MongoDB client not initialized")
            return False
            
        try:
            feed_data = self.fetch_feed()
            if not feed_data:
                return False
                
            # Add unique compound index on source and scrape_date
            self.collection.create_index([("source", 1), ("scrape_date", 1)], unique=True)
            
            # Insert or update the document
            result = self.collection.update_one(
                {
                    "source": feed_data["source"],
                    "scrape_date": feed_data["scrape_date"]
                },
                {"$set": feed_data},
                upsert=True
            )
            
            self.logger.info(
                f"Successfully saved feed data to MongoDB. "
                f"Modified: {result.modified_count}, Upserted: {bool(result.upserted_id)}"
            )
            return True
            
        except OperationFailure as e:
            self.logger.error(f"MongoDB operation failed: {e}")
            return False
        except Exception as e:
            self.logger.error(f"Error saving to MongoDB: {e}")
            return False
            
    def get_latest_entries(self, limit: Optional[int] = None) -> List[Dict]:
        """Get the latest entries from the feed.
        
        Args:
            limit (Optional[int]): Maximum number of entries to return
            
        Returns:
            List[Dict]: List of latest entries
        """
        feed_data = self.fetch_feed()
        entries = feed_data.get("entries", [])
        
        if limit:
            entries = entries[:limit]
            
        return entries

    def __del__(self):
        """Cleanup MongoDB connection when object is destroyed."""
        if hasattr(self, 'client') and self.client:
            self.client.close()
