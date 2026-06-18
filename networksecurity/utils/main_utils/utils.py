import yaml
from networksecurity.exception.exception import NetworksecurityException
from networksecurity.logging.logger import logging
import os,sys
import numpy as np
import pandas as pd
import dill
import pickle

def read_yaml_file(file_path:str)->dict:
    try:
        with open(file_path,"rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise NetworksecurityException(e,sys) from e
    
def write_yaml_file(file_path:str,data:object):
    try:
        dir_path=os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path,"w") as yaml_file:
            yaml.safe_dump(data,yaml_file)
    except Exception as e:
        raise NetworksecurityException(e,sys) from e
    
def save_numpy_array_data(file_path:str,array:np.array):
    try:
        dir_path=os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path,"wb") as file_obj:
            np.save(file_obj,array)
    except Exception as e:
        raise NetworksecurityException(e,sys) from e
    
def save_object(file_path:str,obj:object):
    try:
        dir_path=os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path,"wb") as file_obj:
            dill.dump(obj,file_obj)
    except Exception as e:
        raise NetworksecurityException(e,sys) from e