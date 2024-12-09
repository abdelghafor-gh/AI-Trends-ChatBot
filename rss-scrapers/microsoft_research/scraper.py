from pathlib import Path
import sys

# Add the parent directory to the Python path to import common module
parent_dir = str(Path(__file__).parent.parent)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from common.base_scraper import BaseRSSScraper

class MicrosoftResearchScraper(BaseRSSScraper):
    """Scraper for Microsoft Research RSS feed."""
    
    def __init__(self):
        super().__init__(
            feed_url="https://www.microsoft.com/en-us/research/feed/",
            source_name="microsoft_research"
        )
    
    def _process_entry(self, entry):
        """Process Microsoft Research specific entry fields."""
        # Get base processing
        processed_entry = super()._process_entry(entry)
        
        # Add Microsoft Research specific processing
        # Extract content if available
        if 'content' in entry:
            processed_entry['content'] = entry.get('content', [{}])[0].get('value', '')
            
        # Extract media content (images, videos)
        if 'media_content' in entry:
            processed_entry['media'] = [
                {
                    'url': media.get('url', ''),
                    'type': media.get('type', ''),
                    'width': media.get('width', ''),
                    'height': media.get('height', '')
                }
                for media in entry.get('media_content', [])
            ]
            
        return processed_entry

def main():
    # Initialize scraper
    scraper = MicrosoftResearchScraper()
    
    # Define output path
    output_dir = Path(__file__).parent.parent.parent / "data" / "raw" / "microsoft_research"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "feed.json"
    
    # Fetch and save data
    scraper.save_to_json(str(output_file))
    
    # Print sample of latest entries
    latest_entries = scraper.get_latest_entries(limit=3)
    print("\nLatest Microsoft Research Articles:")
    for entry in latest_entries:
        print(f"\nTitle: {entry['title']}")
        print(f"Published: {entry['published_date']}")
        print(f"Description: {entry['description']}")
        print(f"Link: {entry['link']}")
        if entry.get('media'):
            print(f"Media: {len(entry['media'])} items")

if __name__ == "__main__":
    main()
