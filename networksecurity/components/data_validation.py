import os
import sys
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.constant import training_pipeline
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.constant.training_pipeline import SCHEMA_FILE_PATH
from networksecurity.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from scipy.stats import ks_2samp
from networksecurity.utils.main_utils.utils import read_yaml_file,write_yaml_file
import pandas as pd
import numpy as np

class DataValidation:
    def __init__(self, data_validation_config: DataValidationConfig, data_ingestion_artifact: DataIngestionArtifact):
        try:
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            logging.error(f"Error initializing DataValidation: {e}")
            raise NetworkSecurityException(e, sys)
        
    @staticmethod
    def read_data(file_path: str) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            logging.error(f"Error reading data from {file_path}: {e}")
            raise NetworkSecurityException(e, sys)
        
    def validate_no_of_columns(self, dataframe: pd.DataFrame) -> bool:
        try:
            number_of_columns = len(self._schema_config)
            actual_num_columns = len(dataframe.columns)
            if number_of_columns != actual_num_columns:
                logging.warning(f"Expected {number_of_columns} columns, but got {actual_num_columns}")
                return False
            return True
        except Exception as e:
            logging.error(f"Error validating number of columns: {e}")
            raise NetworkSecurityException(e, sys)
    def detect_data_drift(self, base_df: pd.DataFrame, current_df: pd.DataFrame, threshold = 0.05) -> bool:
        try:
            status = True
            report = {}
            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]
                p_value = ks_2samp(d1, d2).pvalue
                if p_value >= threshold:
                    status = False
                else:
                    status = True
                report[column] = {
                    "p_value": p_value,
                    "drift_status": status                }
            logging.info(f"Data drift report: {report}")
            drift_report_file_path = self.data_validation_config.drift_report_file_path
            os.makedirs(os.path.dirname(drift_report_file_path), exist_ok=True)
            write_yaml_file(file_path=drift_report_file_path, content=report, replace=True)
            return status
        except Exception as e:
            logging.error(f"Error detecting data drift: {e}")
            raise NetworkSecurityException(e, sys)
        

    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            train_file_path=self.data_ingestion_artifact.train_file_path
            test_file_path=self.data_ingestion_artifact.test_file_path
            ##Read the data from the Train and Test file location
            train_dataframe = DataValidation.read_data(train_file_path)
            test_dataframe = DataValidation.read_data(test_file_path)
            ## Validate number of columns
            status = self.validate_no_of_columns(train_dataframe) 
            if not status:
                logging.warning(f"Training data at {train_file_path} failed column validation.")
            status = self.validate_no_of_columns(test_dataframe)
            if not status:
                logging.warning(f"Testing data at {test_file_path} failed column validation.")

            ## Check Data Drift
            drift_status = self.detect_data_drift(base_df=train_dataframe, current_df=test_dataframe)
            dir_path = os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path, exist_ok=True)
            train_dataframe.to_csv(self.data_validation_config.valid_train_file_path, index=False)
            test_dataframe.to_csv(self.data_validation_config.valid_test_file_path, index=False)
            data_validation_artifact = DataValidationArtifact(
                    validation_status=drift_status,
                    valid_train_file_path=self.data_validation_config.valid_train_file_path,
                    valid_test_file_path=self.data_validation_config.valid_test_file_path,
                    invalid_train_file_path=self.data_validation_config.invalid_train_file_path,
                    invalid_test_file_path=self.data_validation_config.invalid_test_file_path,
                    drift_report_file_path=self.data_validation_config.drift_report_file_path
                )
            return data_validation_artifact
        except Exception as e:
            logging.error(f"Error during data validation: {e}")
            raise NetworkSecurityException(e, sys)