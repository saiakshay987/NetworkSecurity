from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig

if __name__ == "__main__":
    training_pipeline_config = TrainingPipelineConfig()
    data_ingestion_config = DataIngestionConfig(training_pipeline_config=training_pipeline_config)
    print(data_ingestion_config.__dict__)
    data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
    data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
    print(data_ingestion_artifact)