from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig
import sys  

if __name__ == "__main__":
    try:
        data_ingestion_config = DataIngestionConfig(training_pipeline_config=TrainingPipelineConfig())
        data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
        logging.info("Initiating data ingestion process")
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        print(f"Data Ingestion Artifact: {data_ingestion_artifact}")
    except Exception as e:
        logging.error(f"Error in main execution: {e}")
        raise NetworkSecurityException(e, sys)