import json
import pandas as pd
from pathlib import Path
import os
from datetime import datetime

class FeedTransformer:
    def __init__(self, input_dir="big_data", output_dir="cosmos"):
        """Initialize the feed transformer with input and output directories."""
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
    def load_json_feed(self, file_path):
        """Load a JSON feed file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
            return None

    def extract_feed_info(self, feed_data, source_category, source_name):
        """Extract relevant information from feed entries."""
        entries = []
        
        if not feed_data or 'entries' not in feed_data:
            return entries

        for entry in feed_data['entries']:
            # Common fields
            info = {
                'source_category': source_category,
                'source_name': source_name,
                'title': entry.get('title', ''),
                'link': entry.get('link', ''),
                'description': entry.get('summary', entry.get('description', '')),
                'published_date': entry.get('published', entry.get('pubDate', '')),
                'author': entry.get('author', ''),
                'tags': ','.join([tag.get('term', '') for tag in entry.get('tags', [])]),
                'id': entry.get('id', entry.get('guid', '')),
            }
            
            # Add feed title and link if available
            # if 'feed' in feed_data:
            #     info['feed_title'] = feed_data['feed'].get('title', '')
            #     info['feed_link'] = feed_data['feed'].get('link', '')
            
            entries.append(info)
            
        return entries

    def process_feeds(self):
        """Process all JSON feeds and convert to CSV."""
        all_entries = []
        
        # Process each JSON file in the input directory
        for file_path in self.input_dir.glob('*_feed.json'):
            try:
                # Extract category and source name from filename
                filename = file_path.stem  # Remove .json extension
                category = filename.split('-')[0]
                source_name = (filename.split('-')[1]).split('_')[:-1]  # Remove category and 'feed'
                
                print(f"Processing {filename}...")
                
                # Load and process feed
                feed_data = self.load_json_feed(file_path)
                if feed_data:
                    entries = self.extract_feed_info(feed_data, category, source_name)
                    all_entries.extend(entries)
                    
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
                continue
        
        if all_entries:
            # Convert to DataFrame
            df = pd.DataFrame(all_entries)
            
            # Clean and standardize dates
            df['published_date'] = pd.to_datetime(df['published_date'], utc=True, errors='coerce')
            
            # Sort by published date
            df = df.sort_values('published_date', ascending=False)
            
            # Generate output filename with timestamp
            timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            output_file = self.output_dir / f'ai_feeds_{timestamp}.csv'
            
            # Save to CSV
            df.to_csv(output_file, index=False, encoding='utf-8')
            print(f"\nSuccessfully saved {len(df)} entries to {output_file}")
            
            # # Save a latest version
            # latest_file = self.output_dir / 'ai_feeds_latest.csv'
            # df.to_csv(latest_file, index=False, encoding='utf-8')
            # print(f"Also saved to {latest_file}")
        else:
            print("No entries found to process")

def main():
    transformer = FeedTransformer()
    transformer.process_feeds()

if __name__ == "__main__":
    main()
