import sys
import os
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.constant import training_pipeline
from networksecurity.entity.config_entity import TrainingPipelineConfig, DataTransformationConfig
from networksecurity.entity.artifact_entity import DataTransformationArtifact, DataValidationArtifact
from networksecurity.constant.training_pipeline import TARGET_COLUMN,DATA_TRANSFORMATION_IMPUTER_PARAMS
from networksecurity.utils.main_utils.utils import save_numpy_array_data, save_object
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline
import pickle

class DataTransformation:

    def __init__(self,data_transformation_config: DataTransformationConfig,data_validation_artifact: DataValidationArtifact):
        try:
            self.data_transformation_config = data_transformation_config
            self.data_validation_artifact = data_validation_artifact
        except Exception as e:
            logging.error(f"Error initializing DataTransformation: {e}")
            raise NetworkSecurityException(e, sys)
    def get_data_transformer_object(self) -> Pipeline:
        try:
            imputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            data_transformation_pipeline = Pipeline(steps=[
                ("imputer", imputer)
            ])
            return data_transformation_pipeline
        except Exception as e:
            logging.error(f"Error creating data transformation pipeline: {e}")
            raise NetworkSecurityException(e, sys)
        
    def initiate_data_transformation(self) -> DataTransformationArtifact:
        try:
            # Load validated train and test data
            valid_train_df = pd.read_csv(self.data_validation_artifact.valid_train_file_path)
            valid_test_df = pd.read_csv(self.data_validation_artifact.valid_test_file_path)

            # Separate features and target
            X_train = valid_train_df.drop(columns=[TARGET_COLUMN])
            y_train = valid_train_df[TARGET_COLUMN]
            X_test = valid_test_df.drop(columns=[TARGET_COLUMN])
            y_test = valid_test_df[TARGET_COLUMN]

            # Get data transformation pipeline
            data_transformation_pipeline = self.get_data_transformer_object()

            # Fit transformation pipeline on training data and transform both train and test data
            X_train_imputed = data_transformation_pipeline.fit_transform(X_train)
            X_test_imputed = data_transformation_pipeline.transform(X_test)

            # Save transformed data and imputer object
            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path, X_train_imputed)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path, X_test_imputed)
            save_object(self.data_transformation_config.transformed_object_file_path, data_transformation_pipeline)

            # Create and return DataTransformationArtifact
            data_transformation_artifact = DataTransformationArtifact(
                transformed_train_file_path = self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path = self.data_transformation_config.transformed_test_file_path,
                transformed_object_file_path = self.data_transformation_config.transformed_object_file_path
            )   
            return data_transformation_artifact
        except Exception as e:
            logging.error(f"Error during data transformation: {e}")
            raise NetworkSecurityException(e, sys)
     
    