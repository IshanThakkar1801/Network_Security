from sklearn.metrics import f1_score
import yaml
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging  
import os
import sys
import pandas as pd
import numpy as np
import dill
import pickle
from sklearn.model_selection import GridSearchCV

def read_yaml_file(file_path: str) -> dict:
    try:
        logging.info(f"Reading YAML file from: {file_path}")
        with open(file_path, 'r') as yaml_file:
            content = yaml.safe_load(yaml_file)
            logging.info(f"Completed reading YAML file from: {file_path}")
            return content
    except Exception as e:
        logging.exception(f"Error reading YAML file at {file_path}")
        raise NetworkSecurityException(e, sys)
    
def write_yaml_file(file_path: str, content: object,replace: bool = False) -> None:
    try:
        logging.info(f"Writing YAML file to: {file_path}")
        if replace:
            if os.path.exists(file_path):
                logging.info(f"Replacing existing YAML file: {file_path}")
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as yaml_file:
            yaml.dump(content, yaml_file)
        logging.info(f"Completed writing YAML file to: {file_path}")
    except Exception as e:
        logging.exception(f"Error writing YAML file at {file_path}")
        raise NetworkSecurityException(e, sys)

def save_numpy_array_data(file_path: str, array: np.array):
    try:
        logging.info(f"Saving numpy array to: {file_path}")
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, 'wb') as file_obj:
            np.save(file_obj, array)
        logging.info(f"Saved numpy array with shape {array.shape} to: {file_path}")
    except Exception as e:
        logging.exception(f"Error saving numpy array to {file_path}")
        raise NetworkSecurityException(e, sys)
    
def save_object(file_path: str, obj: object) -> None:
    try:
        logging.info(f"Saving object of type {type(obj).__name__} to: {file_path}")
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, 'wb') as file_obj:
            pickle.dump(obj, file_obj)
        logging.info(f"Saved object to: {file_path}")
    except Exception as e:
        logging.exception(f"Error saving object to {file_path}")
        raise NetworkSecurityException(e, sys)
    
def load_object(file_path: str):
    try:
        logging.info(f"Loading object from: {file_path}")
        if not os.path.exists(file_path):
            raise Exception(f"File not found: {file_path}")
        with open(file_path, 'rb') as file_obj:
            obj = pickle.load(file_obj)
            logging.info(f"Loaded object of type {type(obj).__name__} from: {file_path}")
            return obj
    except Exception as e:
        logging.exception(f"Error loading object from {file_path}")
        raise NetworkSecurityException(e, sys)
    
def load_numpy_array_data(file_path: str) -> np.array:
    try:
        logging.info(f"Loading numpy array from: {file_path}")
        if not os.path.exists(file_path):
            raise Exception(f"File not found: {file_path}")
        with open(file_path, 'rb') as file_obj:
            array = np.load(file_obj)
            logging.info(f"Loaded numpy array with shape {array.shape} from: {file_path}")
            return array
    except Exception as e:
        logging.exception(f"Error loading numpy array from {file_path}")
        raise NetworkSecurityException(e, sys)

def evaluate_models(x_train, y_train, x_test, y_test, models: dict, param: dict) -> dict:
    try:
        logging.info("Starting model evaluation with GridSearchCV")
        report = {}
        _, class_counts = np.unique(y_train, return_counts=True)
        cv = min(5, class_counts.min())
        if cv < 2:
            logging.warning("Model evaluation failed because at least one class has fewer than 2 samples")
            raise Exception("Each class must have at least 2 samples for model evaluation")
        logging.info(f"Using {cv}-fold cross validation for model evaluation")

        for model_name, model in models.items():
            para = param.get(model_name, {})
            logging.info(f"Training model: {model_name}")
            logging.info(f"Parameter grid for {model_name}: {para}")
            gs = GridSearchCV(model, para, cv=cv, scoring="f1")
            gs.fit(x_train, y_train)
            model.set_params(**gs.best_params_)
            model.fit(x_train, y_train)
            y_test_pred = model.predict(x_test)
            test_model_score = f1_score(y_test, y_test_pred, zero_division=0)
            report[model_name] = test_model_score
            logging.info(f"{model_name} best params: {gs.best_params_}")
            logging.info(f"{model_name} test F1 score: {test_model_score}")
        logging.info(f"Completed model evaluation. Report: {report}")
        return report
    except Exception as e:
        logging.exception("Error evaluating models")
        raise NetworkSecurityException(e, sys)
