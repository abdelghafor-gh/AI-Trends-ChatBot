
import logging 
from dotenv import load_dotenv
from AuthFactory import AuthDBFactory
import uuid 

load_dotenv()


class CosmosDBServices:


    def __init__(self, url, key, database_name, container_name):
        """
        Initialize the CosmosDBHandler with connection details.

        :param url: Cosmos DB URL
        :param key: Cosmos DB primary key
        :param database_name: Name of the database
        :param container_name: Name of the container
        """
        self.container = AuthDBFactory.get_container(url, key, database_name, container_name)


    def get_all_guids(self):
        """
        Retrieve all 'guid' attributes from the container.

        :return: List of GUIDs
        """
        query = "SELECT c.guid FROM c"
        items = self.container.query_items(query=query, enable_cross_partition_query=True)

        guids = []
        for item in items:
            guid = item.get('guid')
            if guid:
                guids.append(guid)
                logging.info(f"Guid: {guid}")
        return guids


    def process_and_store_raw_data(self, data):
        """
        Read data from a JSON file, add a 'processed' attribute, and store records in Cosmos DB.

        :param json_file_path: Path to the JSON file
        """
        try:

            for record in data:
                record["id"] = str(uuid.uuid4())  # Generate unique ID
                record['processed'] = False  # Add 'processed' attribute

                try:
                    self.container.create_item(body=record)
                    logging.info(f"Data inserted into Cosmos DB: {record}")
                except Exception as e:
                    logging.error(f"Error inserting data into Cosmos DB: {e}")
        except Exception as e:
            logging.error(f"Error reading JSON file: {e}")