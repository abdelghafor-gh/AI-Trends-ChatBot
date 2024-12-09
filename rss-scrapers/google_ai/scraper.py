from pathlib import Path
import sys

# Add the parent directory to the Python path to import common module
parent_dir = str(Path(__file__).parent.parent)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from common.base_scraper import BaseRSSScraper

class GoogleAIScraper(BaseRSSScraper):
    """Scraper for Google AI Blog RSS feed."""
    
    def __init__(self):
        super().__init__(
            feed_url="https://blog.research.google/feeds/posts/default?alt=rss",
            source_name="google_ai"
        )
    
    def _process_entry(self, entry):
        """Process Google AI Blog specific entry fields."""
        # Get base processing
        processed_entry = super()._process_entry(entry)
        
        # Add Google AI Blog specific processing
        # Extract categories/tags if available
        if 'category' in entry:
            processed_entry['categories'] = [
                cat.get('term', '') for cat in entry.get('category', [])
            ]
        
        # Extract author information
        if 'author_detail' in entry:
            processed_entry['author'] = {
                'name': entry.author_detail.get('name', ''),
                'email': entry.author_detail.get('email', '')
            }
            
        return processed_entry

def main():
    # Initialize scraper
    scraper = GoogleAIScraper()
    
    # Define output path
    output_dir = Path(__file__).parent.parent.parent / "data" / "raw" / "google_ai"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "feed.json"
    
    # Fetch and save data
    scraper.save_to_json(str(output_file))
    
    # Print sample of latest entries
    latest_entries = scraper.get_latest_entries(limit=3)
    print("\nLatest Google AI Blog Articles:")
    for entry in latest_entries:
        print(f"\nTitle: {entry['title']}")
        print(f"Published: {entry['published_date']}")
        print(f"Description: {entry['description']}")
        print(f"Link: {entry['link']}")
        if entry.get('categories'):
            print(f"Categories: {', '.join(entry['categories'])}")

if __name__ == "__main__":
    main()
