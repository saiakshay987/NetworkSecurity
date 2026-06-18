from networksecurity.exception.exception import NetworksecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.utils.main_utils.utils import read_yaml_file, write_yaml_file
from networksecurity.constant.training_pipeline import *
import os,sys
from scipy.stats import ks_2samp
import pandas as pd
import numpy as np

class DataValidation:
    def __init__(self,data_validation_config:DataValidationConfig,data_ingestion_artifact:DataIngestionArtifact):
        try:
            logging.info(f"{'>>'*5} Data Validation {'<<'*5}")
            self.data_validation_config=data_validation_config
            self.data_ingestion_artifact=data_ingestion_artifact
            self.schema_config=read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworksecurityException(e,sys) from e
        
    def validate_number_of_columns(self,dataframe:pd.DataFrame)->bool:
        try:
            number_of_columns=dataframe.shape[1]
            logging.info(f"Number of columns in dataframe: {number_of_columns}")
            if number_of_columns==len(self.schema_config["columns"]):
                return True
            return False
        except Exception as e:
            raise NetworksecurityException(e,sys) from e

    def is_numerical_column_exist(self,dataframe:pd.DataFrame)->bool:
        try:
            numerical_columns=self.schema_config["numerical_columns"]
            dataframe_numerical_columns=dataframe.select_dtypes(include=[np.number]).columns
            logging.info(f"Numerical columns in dataframe: {dataframe_numerical_columns}")
            for num_col in numerical_columns:
                if num_col not in dataframe_numerical_columns:
                    logging.info(f"Numerical column: {num_col} is not present in dataframe")
                    return False
            return True
        except Exception as e:
            raise NetworksecurityException(e,sys) from e

    def detect_data_drift(self,base_df:pd.DataFrame,current_df:pd.DataFrame)->bool:
        try:
            drift_report={}
            for column in base_df.columns:
                base_data,current_data=base_df[column],current_df[column]
                same_distribution=ks_2samp(base_data,current_data)
                if same_distribution.pvalue>0.05:
                    is_found = False
                else:
                    is_found = True
                drift_report.update({column:{
                    "p_value":float(same_distribution.pvalue),
                    "drift_status": "Different distribution" if is_found else "Same distribution"
                }})
            drift_report_file_path=self.data_validation_config.drift_report_file_path
            dir_path=os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path,exist_ok=True)
            write_yaml_file(drift_report_file_path, drift_report)
            return True
        except Exception as e:
            raise NetworksecurityException(e,sys) from e

    def initiate_data_validation(self)->DataValidationArtifact:
        try:
            logging.info(f"Reading training and testing file")
            training_file_path=self.data_ingestion_artifact.training_file_path
            testing_file_path=self.data_ingestion_artifact.testing_file_path
            train_df=pd.read_csv(training_file_path)
            test_df=pd.read_csv(testing_file_path)
            logging.info(f"Validating number of columns in training and testing dataframe")
            status = self.validate_number_of_columns(train_df)
            if not status:
                raise Exception(f"Number of columns in training dataframe is not equal to schema file")
            status = self.validate_number_of_columns(test_df)
            if not status:
                raise Exception(f"Number of columns in testing dataframe is not equal to schema file")
            status = self.is_numerical_column_exist(train_df)
            if not status:
                raise Exception(f"Numerical columns in training dataframe are not as per schema")
            status = self.is_numerical_column_exist(test_df)
            if not status:
                raise Exception(f"Numerical columns in testing dataframe are not as per schema")
            
            ##data drift report
            status = self.detect_data_drift(base_df=train_df,current_df=test_df)
            if not status:
                raise Exception(f"Data drift is detected between training and testing dataframe")
            dir_path= os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path,exist_ok=True)
            train_df.to_csv(self.data_validation_config.valid_train_file_path,index=False)

            dir_path= os.path.dirname(self.data_validation_config.valid_test_file_path)
            os.makedirs(dir_path,exist_ok=True)
            test_df.to_csv(self.data_validation_config.valid_test_file_path,index=False)

            data_validation_artifact=DataValidationArtifact(
                validation_status = status,
                valid_train_file_path = self.data_ingestion_artifact.training_file_path,
                valid_test_file_path = self.data_ingestion_artifact.testing_file_path,
                invalid_train_file_path = None,
                invalid_test_file_path = None,
                drift_report_file_path = self.data_validation_config.drift_report_file_path
            )
            logging.info(f"Data validation artifact: {data_validation_artifact}")
            return data_validation_artifact
        except Exception as e:
            raise NetworksecurityException(e,sys) from e
        
    