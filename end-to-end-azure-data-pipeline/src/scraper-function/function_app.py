import logging
import azure.functions as func
import json 
from utils import Scraper
from utils.DBservices import CosmosDBServices
from dotenv import load_dotenv
import os

load_dotenv()



app = func.FunctionApp()

@app.timer_trigger(schedule="11,23 * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False) 
def scrapingFunction(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info('The timer is past due!')

    try:
            # Usage example
        scraper = Scraper()
        data = scraper.get_data()
        
        cosmosDBservices = CosmosDBServices(os.getenv("URL"), os.getenv("KEY"), os.getenv("DATABASE_NAME"), os.getenv("CONTAINER_NAME"))

        # cosmosDBservices.process_and_store_raw_data(data)

        with open("new_data_test.json", "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, indent=4, ensure_ascii=False)\
            
        logging.info("Data is Successfully stored into cosmosDB")

    except Exception as e:
        logging.error(e)




    logging.info('Python timer trigger function executed.')

