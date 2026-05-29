import os
import sys
from networksecurity.exception.exception import exception
from networksecurity.logging.logger import logger
from networksecurity.constant import training_pipeline
from networksecurity.entity.config_entity import DataTransformationConfig,ModelTrainerConfig
from networksecurity.entity.artifact_entity import ModelTrainerArtifact, ClassificationMetricArtifact, DataTransformationArtifact
from sklearn.metrics import f1_score, precision_score, recall_score
from networksecurity.utils.main_utils import save_numpy_array_data, load_numpy_array_data,save_object, load_object, evaluate_models
from networksecurity.utils.ml_utils.metric.classification_metric import get_classification_score
from networksecurity.utils.ml_utils.model.estimator import NetworkModel

from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier

class ModelTrainer:
    def __init__(self, model_trainer_config: ModelTrainerConfig, data_transformation_artifact: DataTransformationArtifact):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            logger.error(f"Error initializing ModelTrainer: {e}")
            raise exception(e, sys)
    
    def train_model(self, x_train, y_train, x_test, y_test):
        try:
            models = {
                "RandomForestClassifier": RandomForestClassifier(),
                "GradientBoostingClassifier": GradientBoostingClassifier(),
                "AdaBoostClassifier": AdaBoostClassifier(),
                "LogisticRegression": LogisticRegression(),
                "DecisionTreeClassifier": DecisionTreeClassifier()
            }
            params = {
                DecisionTreeClassifier: {
                    'criterion': ['gini', 'entropy', 'log_loss'],
                    'max_depth': [None, 10, 20, 30],
                    'min_samples_split': [2, 5, 10],
                    'min_samples_leaf': [1, 2, 4]
                },
                RandomForestClassifier: {
                    'n_estimators': [8,16,32,64,128,256],
                    'criterion': ['gini', 'entropy'],
                    'max_depth': [None, 10, 20, 30],
                    'min_samples_split': [2, 5, 10],
                    'min_samples_leaf': [1, 2, 4]
                },
                GradientBoostingClassifier: {
                    'n_estimators': [100, 200, 300],
                    'learning_rate': [0.01, 0.1, 0.2],
                    'max_depth': [3, 5, 7]
                },
                AdaBoostClassifier: {
                    'n_estimators': [50, 100, 200],
                    'learning_rate': [0.01, 0.1, 1]
                },
                LogisticRegression: {
                    'penalty': ['l1', 'l2'],
                    'C': [0.01, 0.1, 1, 10],
                    'solver': ['liblinear']
                }

            }
            model_report: dict = evaluate_models(x_train=x_train, y_train=y_train,x_test=x_test, y_test=y_test, models=models, param=params)

            best_model_score = max(sorted(model_report.values()))
            best_model_name = list(model_report.keys())[list(model_report.values()).index(best_model_score)]
            best_model = models[best_model_name]

            y_train_pred = best_model.predict(x_train)

            classification_train_metric = get_classification_score(y_true=y_train, y_pred=y_train_pred)

            ## Track the mlflow

            y_test_pred = best_model.predict(x_test)
            classification_test_metric = get_classification_score(y_true=y_test,y_pred=y_test_pred)

            preprocessor = load_object(file_path = self.data_transformation_artifact.transformed_object_file_path)

            model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)
            os.makedirs(model_dir_path,exist_ok=True)

            Network_Model = NetworkModel(preprocessor=preprocessor,model=best_model)
            save_object(self.model_trainer_config.trained_model_file_path,obj = NetworkModel)

            ## Model Trainer Artifact

            model_trainer_artifact = ModelTrainerArtifact(trained_model_file_path=self.model_trainer_config.trained_model_file_path,train_metric_artifact=classification_train_metric, test_metric_artifact=classification_test_metric)

            return model_trainer_artifact
            
        except Exception as e:
            logger.error(f"Error training model: {e}")
            raise exception(e, sys)
    
    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        try:
            train_arr = load_numpy_array_data(self.data_transformation_artifact.transformed_train_file_path)
            test_arr = load_numpy_array_data(self.data_transformation_artifact.transformed_test_file_path)

            x_train, y_train = train_arr[:,:-1], train_arr[:,-1]
            x_test, y_test = test_arr[:,:-1], test_arr[:,-1]

            model = self.train_model(x_train, y_train)

            save_object(file_path=self.model_trainer_config.trained_model_file_path, obj=model)

            model_trainer_artifact = ModelTrainerArtifact(trained_model_file_path=self.model_trainer_config.trained_model_file_path)
            return model_trainer_artifact
        except Exception as e:
            logger.error(f"Error initiating model trainer: {e}")
            raise exception(e, sys)


