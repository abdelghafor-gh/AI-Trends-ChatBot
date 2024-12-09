from pathlib import Path
import sys

# Add the parent directory to the Python path to import common module
parent_dir = str(Path(__file__).parent.parent)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from common.base_scraper import BaseRSSScraper

class GoogleDeepMindScraper(BaseRSSScraper):
    """Scraper for Google DeepMind Blog RSS feed."""
    
    def __init__(self):
        super().__init__(
            feed_url="https://deepmind.google/blog/rss.xml",
            source_name="google_deepmind"
        )
    
    def _process_entry(self, entry):
        """Process Google DeepMind Blog specific entry fields."""
        # Get base processing
        processed_entry = super()._process_entry(entry)
        
        # Add DeepMind specific processing
        # Extract categories/tags if available
        if 'tags' in entry:
            processed_entry['categories'] = [
                tag.term for tag in entry.tags if hasattr(tag, 'term')
            ]
        
        # Extract author information if available
        if 'authors' in entry:
            processed_entry['authors'] = [
                author.name for author in entry.authors if hasattr(author, 'name')
            ]
        
        return processed_entry

def main():
    # Initialize scraper
    scraper = GoogleDeepMindScraper()
    
    # Define output path
    output_dir = Path(__file__).parent.parent.parent / "data" / "raw" / "google_deepmind"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "feed.json"
    
    # Fetch and save data
    scraper.save_to_json(str(output_file))
    
    # Print sample of latest entries
    latest_entries = scraper.get_latest_entries(limit=3)
    print("\nLatest Google DeepMind Articles:")
    for entry in latest_entries:
        print(f"\nTitle: {entry['title']}")
        print(f"Published: {entry['published_date']}")
        print(f"Description: {entry['description']}")
        print(f"Link: {entry['link']}")

if __name__ == "__main__":
    main()
