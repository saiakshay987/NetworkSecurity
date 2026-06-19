import os
import sys
import numpy as np
import pandas as pd

"""Data Ingestion related constant start with DATA_INGESTION_VARIABLE_NAME"""

DATA_INGESTION_COLLECTION_NAME: str = "phishing_data"
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.2
DATA_INGESTION_DATABASE_NAME: str = "Network_security"

"""defining common constant variable for training pipeline """

TARGET_COLUMN = "Result"
PIPELINE_NAME: str = "NetworkSecurity"
ARTIFACT_DIR: str = "Artifacts"
FILE_NAME: str = "phishingData.csv"

TRAIN_FILE_NAME: str = "train.csv"
TEST_FILE_NAME: str = "test.csv"

SCHEMA_FILE_PATH: str = os.path.join("data_schema", "schema.yaml")

SAVED_MODEL_DIR: str = os.path.join("saved_models")


"""Data Validation related constant start with DATA_VALIDATION_VARIABLE_NAME"""

DATA_VALIDATION_DIR_NAME: str = "data_validation"
DATA_VALIDATION_VALID_DIR: str = "validated"
DATA_VALIDATION_INVALID_DIR: str = "invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR: str = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME: str = "report.yaml"

"""Data Transformation related constant start with DATA_TRANSFORMATION_VARIABLE_NAME"""

DATA_TRANSFORMATION_DIR_NAME: str = "data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DIR: str = "transformed"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR: str = "transformed_object"
TRANSFORMED_OBJECT_FILE_NAME: str = "preprocessor.pkl"

DATA_TRANSFORMATION_IMPUTER_PARAMS : dict = {
    "missing_values": np.nan,
    "n_neighbors": 3,
    "weights": "uniform",
    "metric": "nan_euclidean",
}

"""Model Trainer related constant start with MODEL_TRAINER_VARIABLE_NAME"""

MODEL_TRAINER_DIR_NAME: str = "model_trainer"
MODEL_TRAINER_TRAINED_MODEL_DIR: str = "trained_model"
MODEL_TRAINER_TRAINED_MODEL_FILE_NAME: str = "model.pkl"
MODEL_TRAINER_EXPECTED_ACCURACY: float = 0.6
MODEL_TRAINER_MODEL_CONFIG_DIR: str = "model_config"
MODEL_TRAINER_MODEL_CONFIG_FILE_NAME: str = "model_config.yaml"
MODEL_TRAINER_OVERFITTING_UNDERFITTING_THRESHOLD: float = 0.05
