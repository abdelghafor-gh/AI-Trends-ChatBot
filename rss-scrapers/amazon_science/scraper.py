from pathlib import Path
import sys

# Add the parent directory to the Python path to import common module
parent_dir = str(Path(__file__).parent.parent)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from common.base_scraper import BaseRSSScraper

class AmazonScienceScraper(BaseRSSScraper):
    """Scraper for Amazon Science RSS feed."""
    
    def __init__(self):
        super().__init__(
            feed_url="https://www.amazon.science/index.rss",
            source_name="amazon_science"
        )
    
    def _process_entry(self, entry):
        """Process Amazon Science specific entry fields."""
        # Get base processing
        processed_entry = super()._process_entry(entry)
        
        # Add any Amazon Science specific processing here
        # For example, extracting specific tags or metadata
        
        return processed_entry

def main():
    # Initialize scraper
    scraper = AmazonScienceScraper()
    
    # Define output path
    output_dir = Path(__file__).parent.parent.parent / "data" / "raw" / "amazon_science"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "feedo.json"
    
    # Fetch and save data
    scraper.save_to_json(str(output_file))
    
    # Print sample of latest entries
    latest_entries = scraper.get_latest_entries(limit=3)
    print("\nLatest Amazon Science Articles:")
    for entry in latest_entries:
        print(f"\nTitle: {entry['title']}")
        print(f"Published: {entry['published_date']}")
        print(f"Description: {entry['description']}")
        print(f"Link: {entry['link']}")

if __name__ == "__main__":
    main()
