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
            logging.info("DataTransformation initialized")
        except Exception as e:
            logging.exception("Error initializing DataTransformation")
            raise NetworkSecurityException(e, sys)
    def get_data_transformer_object(self) -> Pipeline:
        try:
            logging.info(f"Creating KNNImputer with params: {DATA_TRANSFORMATION_IMPUTER_PARAMS}")
            imputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            data_transformation_pipeline = Pipeline(steps=[
                ("imputer", imputer)
            ])
            logging.info("Data transformation pipeline created")
            return data_transformation_pipeline
        except Exception as e:
            logging.exception("Error creating data transformation pipeline")
            raise NetworkSecurityException(e, sys)
        
    def initiate_data_transformation(self) -> DataTransformationArtifact:
        try:
            logging.info("Started data transformation component")
            # Load validated train and test data
            logging.info(f"Reading validated train data from: {self.data_validation_artifact.valid_train_file_path}")
            valid_train_df = pd.read_csv(self.data_validation_artifact.valid_train_file_path)
            logging.info(f"Reading validated test data from: {self.data_validation_artifact.valid_test_file_path}")
            valid_test_df = pd.read_csv(self.data_validation_artifact.valid_test_file_path)
            logging.info(f"Validated train shape: {valid_train_df.shape}, validated test shape: {valid_test_df.shape}")

            # Separate features and target
            X_train = valid_train_df.drop(columns=[TARGET_COLUMN])
            y_train = valid_train_df[TARGET_COLUMN]
            X_test = valid_test_df.drop(columns=[TARGET_COLUMN])
            y_test = valid_test_df[TARGET_COLUMN]
            logging.info(f"Separated features and target column: {TARGET_COLUMN}")

            # Get data transformation pipeline
            data_transformation_pipeline = self.get_data_transformer_object()

            # Fit transformation pipeline on training data and transform both train and test data
            logging.info("Fitting data transformation pipeline on training features")
            X_train_imputed = data_transformation_pipeline.fit_transform(X_train)
            logging.info("Transforming test features")
            X_test_imputed = data_transformation_pipeline.transform(X_test)
            logging.info(f"Transformed train feature shape: {X_train_imputed.shape}")
            logging.info(f"Transformed test feature shape: {X_test_imputed.shape}")

            train_arr = np.c_[X_train_imputed, np.array(y_train)]
            test_arr = np.c_[X_test_imputed, np.array(y_test)]
            logging.info(f"Final transformed train array shape: {train_arr.shape}")
            logging.info(f"Final transformed test array shape: {test_arr.shape}")

            # Save transformed data and imputer object
            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path, train_arr)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path, test_arr)
            save_object(self.data_transformation_config.transformed_object_file_path, data_transformation_pipeline)

            # Create and return DataTransformationArtifact
            data_transformation_artifact = DataTransformationArtifact(
                transformed_train_file_path = self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path = self.data_transformation_config.transformed_test_file_path,
                transformed_object_file_path = self.data_transformation_config.transformed_object_file_path
            )   
            logging.info(f"Data transformation artifact created: {data_transformation_artifact}")
            logging.info("Completed data transformation component")
            return data_transformation_artifact
        except Exception as e:
            logging.exception("Error during data transformation")
            raise NetworkSecurityException(e, sys)
     
    
