from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    feature_store_file_path: str
    training_file_path: str
    testing_file_path: str

@dataclass
class DataValidationArtifact:
    validation_status: bool
    valid_train_file_path: str
    valid_test_file_path: str
    invalid_train_file_path: str
    invalid_test_file_path: str
    drift_report_file_path: str

@dataclass
class DataTransformationArtifact:
    transformed_train_file_path: str
    transformed_test_file_path: str
    preprocessed_object_file_path: str

@dataclass
class ClassificationMetricArtifact:
    model_accuracy: float
    model_precision: float
    model_recall: float
    model_f1_score: float

@dataclass
class ModelTrainerArtifact:
    trained_model_file_path: str
    model_config_file_path: str
    train_metric_artifact: ClassificationMetricArtifact
    test_metric_artifact: ClassificationMetricArtifact
