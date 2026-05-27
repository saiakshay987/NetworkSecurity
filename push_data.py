import os
import sys
import json

from dotenv import load_dotenv
load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL")

import certifi
ca = certifi.where()

import pandas as pd
import numpy as np
import pymongo
from networksecurity.exception.exception import NetworksecurityException
from networksecurity.logging.logger import logging

class NetworkDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            logging.error("An error occurred: %s", str(e))
            raise NetworksecurityException(e, sys)
        
    def cv_to_json_converter(self, file_path):
        try:
            df = pd.read_csv(file_path)
            df.reset_index(drop=True, inplace=True)
            json_data = list(json.loads(df.T.to_json()).values())
            return json_data
        except Exception as e:
            logging.error("An error occurred: %s", str(e))
            raise NetworksecurityException(e, sys)
    def push_data_to_mongodb(self, json_data , database , collection):
        try:
            self.database = database
            self.collection = collection
            self.records = json_data

            self.mongo_client = pymongo.MongoClient(MONGODB_URL, tlsCAFile=ca)
            self.db = self.mongo_client[self.database]
            self.col = self.db[self.collection]
            self.col.insert_many(self.records)
        except Exception as e:
            logging.error("An error occurred: %s", str(e))
            raise NetworksecurityException(e, sys)
        
if __name__ == "__main__":
    FILE_PATH = "Network_data/phisingData.csv"
    database = "Network_security"
    collection = "phishing_data"
    network_data_extract = NetworkDataExtract()
    json_data = network_data_extract.cv_to_json_converter(FILE_PATH)
    network_data_extract.push_data_to_mongodb(json_data, database, collection)