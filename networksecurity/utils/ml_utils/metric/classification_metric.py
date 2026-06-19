import sys
from networksecurity.exception.exception import NetworksecurityException
from networksecurity.entity.artifact_entity import ClassificationMetricArtifact
from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score

def get_classification_metrics(y_true, y_pred):
    try:
        accuracy = accuracy_score(y_true, y_pred)
        precision = precision_score(y_true, y_pred, average='weighted')
        recall = recall_score(y_true, y_pred, average='weighted')
        f1 = f1_score(y_true, y_pred, average='weighted')

        metric_artifact = ClassificationMetricArtifact(
            model_accuracy=accuracy,
            model_precision=precision,
            model_recall=recall,
            model_f1_score=f1
        )
        return metric_artifact
    except Exception as e:
        raise NetworksecurityException(e, sys) from e