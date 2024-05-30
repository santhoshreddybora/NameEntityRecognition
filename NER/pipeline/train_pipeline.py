import sys
from NER.components.data_ingestion import DataIngestion
from NER.constants import *
from NER.exception import CustomException
from NER.logger import logging

from NER.entity.config_entity import DataIngestionConfig
from NER.entity.artifact_entity import DataIngestionArtifact
from NER.configuration.gcloud import GCloud



class TrainPipeline:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        
        self.gcloud=GCloud
    
    def start_data_ingestion(self)->DataIngestionArtifact:
        logging.info("Starting data ingestion in train pipeline")
        try:
            data_ingestion=DataIngestion(data_ingestion_config=self.data_ingestion_config,
                                         gcloud=self.gcloud)
            data_ingestion_artifact=data_ingestion.initiate_data_ingestion()
            logging.info("Got the data from Google cloud storage")
            logging.info(
                "Exited the start_data_ingestion method of TrainPipeline class"
            )
            return data_ingestion_artifact
        except Exception as e:
            raise CustomException(e, sys) from e
    
    def run_pipeline(self):
        try:
            data_ingestion_artifact=self.start_data_ingestion()
        except Exception as e:
            raise CustomException(e, sys) from e
    
