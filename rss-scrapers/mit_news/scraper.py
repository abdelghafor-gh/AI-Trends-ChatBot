from pathlib import Path
import sys
from typing import Dict, Any
import html

# Add the parent directory to the Python path to import common module
parent_dir = str(Path(__file__).parent.parent)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from common.base_scraper import BaseRSSScraper

class MITNewsScraper(BaseRSSScraper):
    """Scraper for MIT News - Artificial Intelligence RSS feed."""
    
    def __init__(self):
        super().__init__(
            feed_url="https://news.mit.edu/topic/mitartificial-intelligence2-rss.xml",
            source_name="mit_news"
        )
    
    def _process_entry(self, entry: Dict[str, Any]) -> Dict[str, Any]:
        """Process MIT News specific entry fields.
        
        Args:
            entry: Raw feed entry from feedparser
            
        Returns:
            Processed entry with standardized fields
        """
        # Get base processing
        processed_entry = super()._process_entry(entry)
        
        # Extract full content if available
        if 'content' in entry and entry.content:
            content = entry.content[0]
            if content.get('type') == 'text/html':
                processed_entry['full_content'] = html.unescape(content.get('value', ''))
        
        # Extract media content (images)
        if 'media_content' in entry:
            processed_entry['media'] = [
                {
                    'url': content.get('url', ''),
                    'type': content.get('type', ''),
                    'width': content.get('width', ''),
                    'height': content.get('height', '')
                }
                for content in entry.get('media_content', [])
            ]
        
        # Extract author details
        if 'author_detail' in entry:
            processed_entry['author'] = {
                'name': entry.author_detail.get('name', ''),
                'affiliation': 'MIT News' if 'MIT News' in entry.author_detail.get('name', '') else ''
            }
        
        # Extract topics/categories with their full taxonomy
        if 'tags' in entry:
            processed_entry['topics'] = [
                {
                    'term': tag.term,
                    'scheme': tag.scheme,
                    'label': tag.label if hasattr(tag, 'label') else None
                }
                for tag in entry.tags
            ]
            
            # Extract AI-related categories for easier filtering
            processed_entry['ai_related_tags'] = [
                tag.term for tag in entry.tags 
                if any(ai_term in tag.term.lower() 
                      for ai_term in ['artificial intelligence', 'machine learning', 'deep learning', 'neural network'])
            ]
        
        # Extract any additional metadata
        if 'summary' in entry:
            processed_entry['summary'] = entry.get('summary', '')
            
        if 'media_credit' in entry:
            processed_entry['image_credits'] = [
                credit.get('content', '') for credit in entry.get('media_credit', [])
            ]
            
        return processed_entry

def main():
    # Initialize scraper
    scraper = MITNewsScraper()
    
    # Define output path
    output_dir = Path(__file__).parent.parent.parent / "data" / "raw" / "mit_news"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "feed.json"
    
    # Fetch and save data
    scraper.save_to_json(str(output_file))
    
    # Print sample of latest entries
    latest_entries = scraper.get_latest_entries(limit=3)
    print("\nLatest MIT News AI Articles:")
    for entry in latest_entries:
        print(f"\nTitle: {entry['title']}")
        print(f"Published: {entry['published_date']}")
        if 'ai_related_tags' in entry:
            print(f"AI Tags: {', '.join(entry['ai_related_tags'])}")
        print(f"Link: {entry['link']}")

if __name__ == "__main__":
    main()
