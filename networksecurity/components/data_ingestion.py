from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.logging.logger import logging
from networksecurity.entity.arifact_entity import DataIngestionArtifact
import sys
import os
import pandas as pd
import numpy as np
import pymongo 
from typing import List
from sklearn.model_selection import train_test_split
from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")

class DataIngestion:
    
        def __init__(self, data_ingestion_config: DataIngestionConfig):
            try:
                self.data_ingestion_config = data_ingestion_config
            except Exception as e:
                raise NetworkSecurityException(e, sys)
            
        def export_collection_as_dataframe(self) -> pd.DataFrame:
            try:
                database_name = self.data_ingestion_config.database_name
                collection_name = self.data_ingestion_config.collection_name
                self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
                collection = self.mongo_client[database_name][collection_name]
                
                df = pd.DataFrame(list(collection.find()))
                if '_id' in df.columns.to_list():
                    df = df.drop(columns=['_id'], axis=1)
                    df.replace({'na': np.nan}, inplace=True)

                logging.info(f"Successfully exported collection {collection_name} to DataFrame with shape {df.shape}")
                return df
            except Exception as e:
                logging.error(f"Error exporting collection {collection_name} to DataFrame: {e}")
                raise NetworkSecurityException(e, sys)
        
        def export_data_into_feature_store(self, dataframe: pd.DataFrame):
            try:
                feature_store_dir = os.path.dirname(self.data_ingestion_config.feature_store_file_path)
                os.makedirs(feature_store_dir, exist_ok=True)
                dataframe.to_csv(self.data_ingestion_config.feature_store_file_path, index=False, header=True)
                logging.info(f"Successfully exported DataFrame to feature store at {self.data_ingestion_config.feature_store_file_path}")
                return dataframe
            except Exception as e:
                logging.error(f"Error exporting DataFrame to feature store: {e}")
                raise NetworkSecurityException(e, sys)  
        
        def split_data_as_train_test(self, dataframe: pd.DataFrame):
            try:
                train_set, test_set = train_test_split(dataframe, test_size=self.data_ingestion_config.train_test_split_ratio)
                os.makedirs(os.path.dirname(self.data_ingestion_config.training_file_path), exist_ok=True)
                os.makedirs(os.path.dirname(self.data_ingestion_config.testing_file_path), exist_ok=True)
                train_set.to_csv(self.data_ingestion_config.training_file_path, index=False, header=True)
                test_set.to_csv(self.data_ingestion_config.testing_file_path, index=False, header=True)
                logging.info(f"Successfully split data into train and test sets with ratio {self.data_ingestion_config.train_test_split_ratio}")
            except Exception as e:
                logging.error(f"Error splitting data into train and test sets: {e}")
                raise NetworkSecurityException(e, sys)
        
        def initiate_data_ingestion(self):
            try:
                dataframe = self.export_collection_as_dataframe()
                self.export_data_into_feature_store(dataframe)
                self.split_data_as_train_test(dataframe)
                dataingestionartifact = DataIngestionArtifact(train_file_path=self.data_ingestion_config.training_file_path, test_file_path=self.data_ingestion_config.testing_file_path)
                return dataingestionartifact
            except Exception as e:
                logging.error(f"Error during data ingestion: {e}")
                raise NetworkSecurityException(e, sys)