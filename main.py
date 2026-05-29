from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.model_trainer import ModelTrainer
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig, DataValidationConfig, DataTransformationConfig, ModelTrainerConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact, DataTransformationArtifact
from networksecurity.components.data_transformation import DataTransformation
import sys  

if __name__ == "__main__":
    try:
        logging.info("Started network security training pipeline")
        data_ingestion_config = DataIngestionConfig(training_pipeline_config=TrainingPipelineConfig())
        data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
        logging.info("Initiating data ingestion process")
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        print(f"Data Ingestion Artifact: {data_ingestion_artifact}")
        logging.info("Data ingestion process completed successfully")

        data_validation_config = DataValidationConfig(training_pipeline_config=TrainingPipelineConfig())
        data_validation = DataValidation(data_validation_config=data_validation_config, data_ingestion_artifact=data_ingestion_artifact)
        logging.info("Initiating data validation process")
        data_validation_artifact = data_validation.initiate_data_validation()
        logging.info("Data validation process completed successfully")
        print(f"Data Validation Artifact: {data_validation_artifact}")

        data_transformation_config = DataTransformationConfig(training_pipeline_config=TrainingPipelineConfig())
        data_transformation = DataTransformation(data_transformation_config=data_transformation_config, data_validation_artifact=data_validation_artifact)
        logging.info("Initiating data transformation process")
        data_transformation_artifact = data_transformation.initiate_data_transformation()
        print(f"Data Transformation Artifact: {data_transformation_artifact}")
        logging.info("Data transformation process completed successfully")

        model_trainer_config = ModelTrainerConfig(training_pipeline_config=TrainingPipelineConfig())
        model_trainer = ModelTrainer(model_trainer_config=model_trainer_config,data_transformation_artifact=data_transformation_artifact)
        logging.info("Initiating model trainer process")
        model_trainer_artifact = model_trainer.initiate_model_trainer()
        print(f"Model Trainer Artifact: {model_trainer_artifact}")
        logging.info("Model trainer process completed successfully")
        logging.info("Network security training pipeline completed successfully")

    except Exception as e:
        logging.exception("Error in main execution")
        raise NetworkSecurityException(e, sys)
