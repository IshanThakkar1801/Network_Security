from datetime import datetime
import sys
import os
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.constant import training_pipeline

class TrainingPipelineConfig:
    def __init__(self,timestamp = datetime.now()):
        try:
            timestamp = timestamp.strftime('%m_%d_%Y_%H_%M_%S')
            self.pipeline_name = training_pipeline.PIPELINE_NAME
            self.artifsact_name = training_pipeline.ARTIFACT_DIR
            self.artifact_dir = os.path.join(self.artifsact_name, timestamp)
            self.timestamp: str = timestamp
        except Exception as e:
            logging.error(f"Error initializing TrainingPipelineConfig: {e}")
            raise NetworkSecurityException(e, sys)

class DataIngestionConfig:
    def __init__(self,training_pipeline_config: TrainingPipelineConfig):
        try:
            self.data_ingestion_dir = os.path.join(training_pipeline_config.artifact_dir, training_pipeline.DATA_INGESTION_DIR_NAME)
            self.feature_store_file_path = os.path.join(training_pipeline_config.artifact_dir, training_pipeline.DATA_INGESTION_FEATURE_STORE_NAME, training_pipeline.FILE_NAME)
            self.training_file_path = os.path.join(training_pipeline_config.artifact_dir, training_pipeline.DATA_INGESTION_INGESTED_DIR, training_pipeline.TRAIN_FILE_NAME)
            self.testing_file_path = os.path.join(training_pipeline_config.artifact_dir, training_pipeline.DATA_INGESTION_INGESTED_DIR, training_pipeline.TEST_FILE_NAME)

            self.train_test_split_ratio: float = training_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
            self.collection_name: str = training_pipeline.DATA_INGESTION_COLLECTION_NAME
            self.database_name: str = training_pipeline.DATA_INGESTION_DATABASE_NAME
        except Exception as e:
            logging.error(f"Error initializing DataIngestionConfig: {e}")
            raise NetworkSecurityException(e, sys)
        
class DataValidationConfig:

    def __init__(self,training_pipeline_config: TrainingPipelineConfig):
        try:
            self.data_validation_dir: str = os.path.join(training_pipeline_config.artifact_dir, training_pipeline.DATA_VALIDATION_DIR_NAME)
            self.valid_data_dir: str = os.path.join(self.data_validation_dir, training_pipeline.DATA_VALIDATION_VALID_DIR)
            self.invalid_data_dir: str = os.path.join(self.data_validation_dir, training_pipeline.DATA_VALIDATION_INVALID_DIR)
            self.valid_test_file_path: str = os.path.join(self.valid_data_dir, training_pipeline.TEST_FILE_NAME)
            self.valid_train_file_path: str = os.path.join(self.valid_data_dir, training_pipeline.TRAIN_FILE_NAME)
            self.invalid_train_file_path: str = os.path.join(self.invalid_data_dir, training_pipeline.TRAIN_FILE_NAME)
            self.invalid_test_file_path: str = os.path.join(self.invalid_data_dir, training_pipeline.TEST_FILE_NAME)
            self.drift_report_file_path: str = os.path.join(self.data_validation_dir, training_pipeline.DATA_VALIDATION_DRIFT_REPORT_DIR, training_pipeline.DATA_VALIDATION_DRIFT_REPORT_FILE_NAME)

        except Exception as e:
            logging.error(f"Error initializing DataValidationConfig: {e}")
            raise NetworkSecurityException(e, sys)
        
class DataTransformationConfig:

    def __init__(self,training_pipeline_config: TrainingPipelineConfig):
        try:
            self.data_transformation_dir: str = os.path.join(training_pipeline_config.artifact_dir, training_pipeline.DATA_TRANSFORMATION_DIR_NAME)
            self.transformed_train_file_path: str = os.path.join(self.data_transformation_dir, training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR, training_pipeline.TRAIN_FILE_NAME.replace("csv", "npy"))
            self.transformed_test_file_path: str = os.path.join(self.data_transformation_dir, training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR, training_pipeline.TEST_FILE_NAME.replace("csv", "npy"))
            self.transformed_object_file_path: str = os.path.join(self.data_transformation_dir, training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR, training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_OBJECT_FILE_NAME)
        except Exception as e:
            logging.error(f"Error initializing DataTransformationConfig: {e}")
            raise NetworkSecurityException(e, sys)  
        