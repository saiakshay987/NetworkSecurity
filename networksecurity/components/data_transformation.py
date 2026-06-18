import sys
import os
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from networksecurity.constant import training_pipeline
from networksecurity.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact, DataTransformationArtifact
from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.exception.exception import NetworksecurityException
from networksecurity.logging.logger import logging
from networksecurity.utils.main_utils.utils import *

class DataTransformation:
    def __init__(self, data_transformation_config: DataTransformationConfig,data_validation_artifact:DataValidationArtifact):
        try:
            logging.info(f"{'>>'*5}Data Transformation log started.{'<<'*5}")
            self.data_transformation_config = data_transformation_config
            self.data_validation_artifact = data_validation_artifact
        except Exception as e:
            raise NetworksecurityException(e, sys) from e
        
    def get_data_transformer_object(cls)->Pipeline:
        try:
            imputer = KNNImputer(**training_pipeline.DATA_TRANSFORMATION_IMPUTER_PARAMS)
            preprocessor = Pipeline(steps=[
                ('imputer', imputer)
            ])
            return preprocessor
        except Exception as e:
            raise NetworksecurityException(e, sys) from e

    def initiate_data_transformation(self)->DataTransformationArtifact:
        try:
            logging.info("Initiating data transformation...")
            # Load the validated training and testing data
            train_df = pd.read_csv(self.data_validation_artifact.valid_train_file_path)
            test_df = pd.read_csv(self.data_validation_artifact.valid_test_file_path)

            #training dataframe
            input_feature_train_df = train_df.drop(columns=[training_pipeline.TARGET_COLUMN],axis=1)
            target_feature_train_df = train_df[training_pipeline.TARGET_COLUMN]
            target_feature_train_df = target_feature_train_df.replace(-1,0)

            #testing dataframe
            input_feature_test_df = test_df.drop(columns=[training_pipeline.TARGET_COLUMN],axis=1)
            target_feature_test_df = test_df[training_pipeline.TARGET_COLUMN]
            target_feature_test_df = target_feature_test_df.replace(-1,0)

            # Get the data transformer object
            preprocessor = self.get_data_transformer_object()
            # Fit and transform the training data, transform the testing data
            transformed_input_train_feature = preprocessor.fit_transform(input_feature_train_df)
            transformed_input_test_feature = preprocessor.transform(input_feature_test_df)

            # Concatenate the transformed input features with the target features
            train_arr = np.c_[transformed_input_train_feature, np.array(target_feature_train_df)]
            test_arr = np.c_[transformed_input_test_feature, np.array(target_feature_test_df)]

            # Save the transformed arrays and the preprocessor object
            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path, train_arr)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path, test_arr)
            save_object(self.data_transformation_config.transformed_object_file_path, preprocessor)

            data_transformation_artifact = DataTransformationArtifact(
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path,
                preprocessed_object_file_path=self.data_transformation_config.transformed_object_file_path
            )
            logging.info(f"Data transformation artifact: {data_transformation_artifact}")
            return data_transformation_artifact

        except Exception as e:
            raise NetworksecurityException(e, sys) from e

        
    



