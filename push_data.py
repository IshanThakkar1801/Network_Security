import os
import sys
import json
from dotenv import load_dotenv
import certifi
import pymongo
import pandas as pd
import numpy as np
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")
print(MONGO_DB_URL)

ca = certifi.where()

class NetworkDataExtract:
    def __init__(self):
        try:
            pass
        except Exception as e:
            logging.error(f"Error creating MongoDB client: {e}")
            raise NetworkSecurityException(e, sys)
    
    def cv_to_json(self, file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(inplace=True, drop=True)
            records = data.T.to_dict().values()
            json_data = json.loads(data.T.to_json()).values()
            return json_data
        except Exception as e:
            logging.error(f"Error converting CSV to JSON: {e}")
            raise NetworkSecurityException(e, sys)
        
    def insert_data_to_mongodb(self, records, database, collection_name):
        try:
            self.database = database
            self.collection_name = collection_name
            self.records = records

            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL, tlsCAFile=ca)
            self.database = self.mongo_client["NetworkSecurityDB"]
            
            self.collection = self.database[self.collection_name]
            self.collection.insert_many(self.records)

            return (len(self.records))
        except Exception as e:
            logging.error(f"Error inserting data to MongoDB: {e}")
            raise NetworkSecurityException(e, sys)

if __name__ == "__main__":
    FILE_PATH = "Network_Data/phisingData.csv"
    DATABASE = "NetworkSecurityDB"
    COLLECTION_NAME = "NetworkData"
    networkobj = NetworkDataExtract()
    records = networkobj.cv_to_json(FILE_PATH)
    no_of_records = networkobj.insert_data_to_mongodb(records, DATABASE, COLLECTION_NAME)

    print(f"Number of records inserted to MongoDB: {no_of_records}")