from networksecurity.exception.exception import NetworksecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig
import os, sys
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import pymongo
from typing import List
from networksecurity.entity.artifact_entity import DataIngestionArtifact

from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL = os.getenv("MONGODB_URL")

class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            logging.info(f"{'>>'*5}Data Ingestion log started.{'<<'*5} ")
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise NetworksecurityException(e, sys) from e

    def export_collection_as_dataframe(self) -> pd.DataFrame:
        try:
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL,tlsAllowInvalidCertificates=True)
            collection = self.mongo_client[database_name][collection_name]

            df = pd.DataFrame(list(collection.find()))
            if "_id" in df.columns:
                df.drop("_id", axis=1, inplace=True)
            
            df.replace({"na": np.nan}, inplace=True)
            logging.info(f"Data exported from MongoDB collection: {collection_name} in database: {database_name} successfully.")
            return df
        
        except Exception as e:
            raise NetworksecurityException(e, sys) from e

    def export_data_into_feature_store(self, dataframe: pd.DataFrame):
        try:
            feature_store_dir = os.path.dirname(self.data_ingestion_config.feature_store_file_path)
            os.makedirs(feature_store_dir, exist_ok=True)
            dataframe.to_csv(self.data_ingestion_config.feature_store_file_path, index=False)
            logging.info(f"Data exported to feature store at: {self.data_ingestion_config.feature_store_file_path} successfully.")
        except Exception as e:
            raise NetworksecurityException(e, sys) from e

    def split_data_as_train_test(self, dataframe: pd.DataFrame):
        try:
            train_set, test_set = train_test_split(dataframe, test_size=self.data_ingestion_config.train_test_split_ratio, random_state=42)
            train_file_path = self.data_ingestion_config.training_file_path
            test_file_path = self.data_ingestion_config.testing_file_path

            train_dir = os.path.dirname(train_file_path)
            test_dir = os.path.dirname(test_file_path)

            os.makedirs(train_dir, exist_ok=True)
            os.makedirs(test_dir, exist_ok=True)

            train_set.to_csv(train_file_path, index=False)
            test_set.to_csv(test_file_path, index=False)
            logging.info(f"Data split into train and test sets successfully. Train file path: {train_file_path}, Test file path: {test_file_path}")
        except Exception as e:
            raise NetworksecurityException(e, sys) from e

    def initiate_data_ingestion(self):
        try:
            dataframe = self.export_collection_as_dataframe()
            self.export_data_into_feature_store(dataframe=dataframe)
            self.split_data_as_train_test(dataframe=dataframe)
            data_ingestion_artifact = DataIngestionArtifact(
                feature_store_file_path=self.data_ingestion_config.feature_store_file_path,
                training_file_path=self.data_ingestion_config.training_file_path,
                testing_file_path=self.data_ingestion_config.testing_file_path
            )
            logging.info(f"Data ingestion artifact created successfully.")
            return data_ingestion_artifact
        except Exception as e:
            raise NetworksecurityException(e, sys) from e