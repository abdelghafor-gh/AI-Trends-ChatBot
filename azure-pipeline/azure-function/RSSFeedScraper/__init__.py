import datetime
import logging
import azure.functions as func
from ..shared_code.feeds_scraper import RSSFeedScraper
from azure.identity import DefaultAzureCredential
from azure.storage.filedatalake import DataLakeServiceClient
import os
import json
import pandas as pd

def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.now().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due!')

    logging.info('RSS Feed scraper function started at %s', utc_timestamp)

    try:
        # Initialize the scraper
        scraper = RSSFeedScraper(
            resources_file="shared_code/resources.json",
            output_dir="data"
        )
        
        # Process all feeds
        scraper.process_all_feeds()
        
        # Get the output file path and data
        date_str = datetime.datetime.now().strftime('%Y-%m-%d')
        output_data = {
            'date': date_str,
            'last_updated': utc_timestamp,
            'entries_count': len(scraper.all_entries),
            'entries': sorted(scraper.all_entries, 
                            key=lambda x: pd.to_datetime(x['published_date'], utc=True), 
                            reverse=True)
        }
        
        # Upload to Azure Data Lake Storage Gen2
        try:
            # Get storage account credentials
            account_name = os.environ["STORAGE_ACCOUNT_NAME"]
            credential = DefaultAzureCredential()
            
            # Initialize the Data Lake service client
            service_client = DataLakeServiceClient(
                account_url=f"https://{account_name}.dfs.core.windows.net",
                credential=credential
            )
            
            # Get file system client (container)
            file_system_name = "ai-feeds"
            file_system_client = service_client.get_file_system_client(file_system_name)
            
            # Create directory structure: year/month/day
            year = datetime.datetime.now().strftime('%Y')
            month = datetime.datetime.now().strftime('%m')
            day = datetime.datetime.now().strftime('%d')
            directory_path = f"raw/year={year}/month={month}/day={day}"
            
            # Get directory client
            directory_client = file_system_client.get_directory_client(directory_path)
            
            # Create directory if it doesn't exist
            if not directory_client.exists():
                directory_client.create_directory()
            
            # Get file client
            file_name = f"{date_str}.json"
            file_client = directory_client.get_file_client(file_name)
            
            # Upload the data
            file_contents = json.dumps(output_data, ensure_ascii=False, indent=4)
            file_client.upload_data(file_contents, overwrite=True)
            
            logging.info(f"Successfully uploaded {file_name} to Data Lake Storage")
            
        except Exception as e:
            logging.error(f"Error uploading to Data Lake Storage: {str(e)}")
            raise
        
        logging.info('RSS Feed scraper function completed successfully.')
        
    except Exception as e:
        logging.error(f'Error in RSS Feed scraper function: {str(e)}')
        raise
