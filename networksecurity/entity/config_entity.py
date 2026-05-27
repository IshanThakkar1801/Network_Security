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