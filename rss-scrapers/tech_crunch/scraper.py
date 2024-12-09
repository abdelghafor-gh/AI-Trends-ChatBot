from pathlib import Path
import sys

# Add the parent directory to the Python path to import common module
parent_dir = str(Path(__file__).parent.parent)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from common.base_scraper import BaseRSSScraper

class TechCrunchScraper(BaseRSSScraper):
    """Scraper for TechCrunch - AI RSS feed."""
    
    def __init__(self):
        super().__init__(
            feed_url="https://techcrunch.com/category/artificial-intelligence/feed",
            source_name="tech_crunch"
        )
    
    def _process_entry(self, entry):
        """Process TechCrunch specific entry fields."""
        # Get base processing
        processed_entry = super()._process_entry(entry)
        
        # Add TechCrunch specific processing
        # Extract creator/author
        if 'dc_creator' in entry:
            processed_entry['author'] = entry.dc_creator
            
        # Extract comments URL if available
        if 'comments' in entry:
            processed_entry['comments_url'] = entry.comments
            
        # Extract categories
        if 'tags' in entry:
            processed_entry['categories'] = [
                tag.term for tag in entry.tags if hasattr(tag, 'term')
            ]
            
        # Extract featured image if available
        if 'media_thumbnail' in entry:
            processed_entry['featured_image'] = entry.media_thumbnail[0]['url'] if entry.media_thumbnail else None
            
        return processed_entry

def main():
    # Initialize scraper
    scraper = TechCrunchScraper()
    
    # Define output path
    output_dir = Path(__file__).parent.parent.parent / "data" / "raw" / "tech_crunch"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "feed.json"
    
    # Fetch and save data
    scraper.save_to_json(str(output_file))
    
    # Print sample of latest entries
    latest_entries = scraper.get_latest_entries(limit=3)
    print("\nLatest TechCrunch AI Articles:")
    for entry in latest_entries:
        print(f"\nTitle: {entry['title']}")
        print(f"Published: {entry['published_date']}")
        print(f"Description: {entry['description']}")
        print(f"Link: {entry['link']}")

if __name__ == "__main__":
    main()
