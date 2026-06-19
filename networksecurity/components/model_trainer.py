import sys
import os
import mlflow
from networksecurity.exception.exception import NetworksecurityException
from networksecurity.logging.logger import logging

from networksecurity.entity.artifact_entity import ClassificationMetricArtifact, DataTransformationArtifact,ModelTrainerArtifact
from networksecurity.entity.config_entity import ModelTrainerConfig

from networksecurity.utils.main_utils.utils import save_object,load_object,evaluate_models
from networksecurity.utils.main_utils.utils import save_numpy_array_data,load_numpy_array_data

from networksecurity.utils.ml_utils.metric.classification_metric import get_classification_metrics
from networksecurity.utils.ml_utils.model.estimator import NetworkModel

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier,GradientBoostingClassifier,AdaBoostClassifier
from sklearn.neighbors import KNeighborsClassifier

class ModelTrainer:
    def __init__(self,model_trainer_config:ModelTrainerConfig,
                 data_transformation_artifact:DataTransformationArtifact):
        try:
            self.model_trainer_config=model_trainer_config
            self.data_transformation_artifact=data_transformation_artifact
        except Exception as e:
            raise NetworksecurityException(e,sys) from e
        
    def track_mlflow(self,model,classification_metrics:ClassificationMetricArtifact):
        try:
            with mlflow.start_run(run_name="ModelTrainer") as mlflow_run:
                mlflow.log_param("model_name", model.__class__.__name__)
                mlflow.log_metric("accuracy", classification_metrics.model_accuracy)
                mlflow.log_metric("precision", classification_metrics.model_precision)
                mlflow.log_metric("recall", classification_metrics.model_recall)
                mlflow.log_metric("f1_score", classification_metrics.model_f1_score)
                mlflow.sklearn.log_model(model, artifact_path="model")
        except Exception as e:
            raise NetworksecurityException(e,sys) from e
    
    def train_model(self,X_train,y_train,X_test,y_test):
        try:
            models = {
                "LogisticRegression": LogisticRegression(n_jobs=-1),
                "DecisionTreeClassifier": DecisionTreeClassifier(),
                "RandomForestClassifier": RandomForestClassifier(n_jobs=-1),
                "GradientBoostingClassifier": GradientBoostingClassifier(verbose=1),
                "AdaBoostClassifier": AdaBoostClassifier(),
                "KNeighborsClassifier": KNeighborsClassifier()
            }
            params={
                "DecisionTreeClassifier": {
                    'criterion':['gini', 'entropy', 'log_loss'],
                    # 'splitter':['best','random'],
                    # 'max_features':['sqrt','log2'],
                },
                "RandomForestClassifier":{
                    # 'criterion':['gini', 'entropy', 'log_loss'],
                
                    # 'max_features':['sqrt','log2',None],
                    'n_estimators': [8,16,32,128,256]
                },
                "GradientBoostingClassifier":{
                    # 'loss':['log_loss', 'exponential'],
                    'learning_rate':[.1,.01,.05,.001],
                    'subsample':[0.6,0.7,0.75,0.85,0.9],
                    # 'criterion':['squared_error', 'friedman_mse'],
                    # 'max_features':['auto','sqrt','log2'],
                    'n_estimators': [8,16,32,64,128,256]
                },
                "LogisticRegression":{},
                "AdaBoostClassifier":{
                    'learning_rate':[.1,.01,.001],
                    'n_estimators': [8,16,32,64,128,256]
                },
                "KNeighborsClassifier":{
                    'n_neighbors':[5,7,9,11],
                    'weights':['uniform','distance']
                }
            }

            model_report : dict = evaluate_models(X_train=X_train,y_train=y_train,X_test=X_test,y_test=y_test,
                                                  models=models,params=params)
            
            best_model_score = max(sorted(model_report.values()))
            best_model_name = list(model_report.keys())[list(model_report.values()).index(best_model_score)]
            best_model = models[best_model_name]
            y_train_pred = best_model.predict(X_train)
            y_test_pred = best_model.predict(X_test)

            classification_metrics_train = get_classification_metrics(y_true=y_train,y_pred=y_train_pred)
            self.track_mlflow(best_model,classification_metrics_train)
            classification_metrics_test = get_classification_metrics(y_true=y_test,y_pred=y_test_pred)
            self.track_mlflow(best_model,classification_metrics_test)

            preprocessor = load_object(file_path=self.data_transformation_artifact.preprocessed_object_file_path)

            model_dir_path = os.path.dirname(self.model_trainer_config.model_trainer_dir)
            os.makedirs(model_dir_path,exist_ok=True)
            
            Network_model = NetworkModel(preprocessor=preprocessor,model=best_model)
            save_object(file_path=self.model_trainer_config.trained_model_file_path,obj=Network_model)

            ModelTrainer_Artifact = ModelTrainerArtifact(trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                                                        model_config_file_path=self.model_trainer_config.model_config_file_path,
                                                        train_metric_artifact=classification_metrics_train,
                                                        test_metric_artifact=classification_metrics_test)
            logging.info(f"Model trainer artifact: {ModelTrainer_Artifact}")
            return ModelTrainer_Artifact

        except Exception as e:
            raise NetworksecurityException(e,sys) from e
        
    
    def initiate_model_trainer(self)->ModelTrainerArtifact:
        try:
            train_file_path=self.data_transformation_artifact.transformed_train_file_path
            test_file_path=self.data_transformation_artifact.transformed_test_file_path

            train_arr = load_numpy_array_data(train_file_path)
            test_arr = load_numpy_array_data(test_file_path)
            X_train,y_train,X_test,y_test = train_arr[:,:-1],train_arr[:,-1],test_arr[:,:-1],test_arr[:,-1]

            model = self.train_model(X_train,y_train,X_test,y_test)
            return model
        except Exception as e:
            raise NetworksecurityException(e,sys) from e

