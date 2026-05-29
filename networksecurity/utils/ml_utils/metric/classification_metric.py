from networksecurity.entity.artifact_entity import ClassificationMetricArtifact
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import sys
from sklearn.metrics import f1_score, precision_score, recall_score

def get_classification_score(y_true, y_pred) -> ClassificationMetricArtifact:
    try:
        logging.info("Calculating classification metrics")
        f1 = f1_score(y_true, y_pred, zero_division=0)
        precision = precision_score(y_true, y_pred, zero_division=0)
        recall = recall_score(y_true, y_pred, zero_division=0)

        classification_metric = ClassificationMetricArtifact(f1_score=f1, precision_score=precision, recall_score=recall)
        logging.info(f"Classification metrics calculated: {classification_metric}")
        return classification_metric
    except Exception as e:
        logging.exception("Error calculating classification score")
        raise NetworkSecurityException(e, sys)
