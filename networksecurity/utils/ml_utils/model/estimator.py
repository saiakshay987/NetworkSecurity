import os
import sys
from networksecurity.exception.exception import NetworksecurityException
from networksecurity.logging.logger import logging
from networksecurity.constant.training_pipeline import SAVED_MODEL_DIR,MODEL_TRAINER_TRAINED_MODEL_FILE_NAME

class NetworkModel:
    def __init__(self,model,preprocessor):
        self.model=model
        self.preprocessor=preprocessor

    def predict(self,X):
        try:
            X = self.preprocessor.transform(X)
            return self.model.predict(X)
        except Exception as e:
            raise NetworksecurityException(e,sys) from e
