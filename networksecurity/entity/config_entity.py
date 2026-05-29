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
            logging.info(f"TrainingPipelineConfig initialized with artifact_dir: {self.artifact_dir}")
        except Exception as e:
            logging.exception("Error initializing TrainingPipelineConfig")
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
            logging.info("DataIngestionConfig initialized")
            logging.info(f"Feature store path: {self.feature_store_file_path}")
            logging.info(f"Training file path: {self.training_file_path}")
            logging.info(f"Testing file path: {self.testing_file_path}")
        except Exception as e:
            logging.exception("Error initializing DataIngestionConfig")
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
            logging.info("DataValidationConfig initialized")
            logging.info(f"Valid train path: {self.valid_train_file_path}")
            logging.info(f"Valid test path: {self.valid_test_file_path}")
            logging.info(f"Drift report path: {self.drift_report_file_path}")

        except Exception as e:
            logging.exception("Error initializing DataValidationConfig")
            raise NetworkSecurityException(e, sys)
        
class DataTransformationConfig:

    def __init__(self,training_pipeline_config: TrainingPipelineConfig):
        try:
            self.data_transformation_dir: str = os.path.join(training_pipeline_config.artifact_dir, training_pipeline.DATA_TRANSFORMATION_DIR_NAME)
            self.transformed_train_file_path: str = os.path.join(self.data_transformation_dir, training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR, training_pipeline.TRAIN_FILE_NAME.replace("csv", "npy"))
            self.transformed_test_file_path: str = os.path.join(self.data_transformation_dir, training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR, training_pipeline.TEST_FILE_NAME.replace("csv", "npy"))
            self.transformed_object_file_path: str = os.path.join(self.data_transformation_dir, training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR, training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_OBJECT_FILE_NAME)
            logging.info("DataTransformationConfig initialized")
            logging.info(f"Transformed train file path: {self.transformed_train_file_path}")
            logging.info(f"Transformed test file path: {self.transformed_test_file_path}")
            logging.info(f"Transformed object file path: {self.transformed_object_file_path}")
        except Exception as e:
            logging.exception("Error initializing DataTransformationConfig")
            raise NetworkSecurityException(e, sys)  

class ModelTrainerConfig:

    def __init__(self,training_pipeline_config: TrainingPipelineConfig):
        try:
            self.model_trainer_dir: str = os.path.join(training_pipeline_config.artifact_dir, training_pipeline.MODEL_TRAINER_DIR_NAME)
            self.trained_model_file_path: str = os.path.join(self.model_trainer_dir, training_pipeline.MODEL_TRAINER_TRAINED_MODEL_DIR, training_pipeline.MODEL_TRAINER_TRAINED_MODEL_FILE_NAME)
            self.expected_score: float = training_pipeline.MODEL_TRAINER_EXPECTED_SCORE
            self.overfitting_underfitting_threshold: float = training_pipeline.MODEL_TRAINER_OVER_FITTING_UNDER_FITTING_THRESHOLD
            logging.info("ModelTrainerConfig initialized")
            logging.info(f"Trained model file path: {self.trained_model_file_path}")
            logging.info(f"Expected model score: {self.expected_score}")
            logging.info(f"Overfitting/underfitting threshold: {self.overfitting_underfitting_threshold}")
        except Exception as e:
            logging.exception("Error initializing ModelTrainerConfig")
            raise NetworkSecurityException(e, sys)
