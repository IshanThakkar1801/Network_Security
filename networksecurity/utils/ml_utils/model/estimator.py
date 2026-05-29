from networksecurity.constant.training_pipeline import SAVED_MODEL_DIR, MODEL_FILE_NAME

import os
import sys
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

class NetworkModel:
    def __init__(self, preprocessor, model):
        try:
            logging.info("Initializing NetworkModel")
            self.preprocessor = preprocessor
            self.model = model
            logging.info(
                f"NetworkModel initialized with preprocessor={type(preprocessor).__name__}, "
                f"model={type(model).__name__}"
            )
        except Exception as e:
            logging.exception("Error initializing NetworkModel")
            raise NetworkSecurityException(e, sys)

    def predict(self, X):
        try:
            logging.info(f"Starting prediction for input shape: {getattr(X, 'shape', None)}")
            x_transformed = self.preprocessor.transform(X)
            logging.info(f"Transformed prediction input shape: {getattr(x_transformed, 'shape', None)}")
            y_hat = self.model.predict(x_transformed)
            logging.info(f"Completed prediction. Output shape: {getattr(y_hat, 'shape', None)}")
            return y_hat
        except Exception as e:
            logging.exception("Error during prediction")
            raise NetworkSecurityException(e, sys)
