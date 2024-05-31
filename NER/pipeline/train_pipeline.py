import sys
from NER.components.data_ingestion import DataIngestion
from NER.components.data_transforamation import DataTrandformation
from NER.components.model_trainer import ModelTraining
from NER.components.model_evaluation import ModelEvaluation
from NER.components.model_pusher import ModelPusher
from NER.constants import *
from NER.exception import CustomException
from NER.logger import logging

from NER.entity.config_entity import (DataIngestionConfig,DataTransformationConfig,
                                      ModelTrainingConfig,ModelEvalConfig,ModelPusherConfig)
from NER.entity.artifact_entity import (DataIngestionArtifact,DataTransformationArtifact,
                                        ModelTrainerArtifact,ModelEvaluationArtifacts,ModelPusherArtifacts)
from NER.configuration.gcloud import GCloud



class TrainPipeline:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        self.data_transformation_config=DataTransformationConfig()
        self.model_training_config=ModelTrainingConfig()
        self.model_evaluation_config=ModelEvalConfig()
        self.model_pusher_config=ModelPusherConfig()
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
    
    def start_data_transformation(self,data_ingestion_artifact:DataIngestionArtifact)->DataTransformationArtifact:
        logging.info("Starting data transformation in train pipeline")
        try:
            data_transformation=DataTrandformation(data_transformation_config=self.data_transformation_config,data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact=data_transformation.initiate_data_transformation()
            logging.info("Got the transformed data")
            logging.info(
                "Exited the start_data_transformation method of TrainPipeline class"
            )
            return data_transformation_artifact
        except Exception as e:
            raise CustomException(e, sys) from e

    def start_model_training(
        self, data_transformation_artifacts: DataTransformationArtifact
    ) -> ModelTrainerArtifact:
        logging.info("Entered the start_model_training method of Train pipeline class")
        try:
            model_trainer = ModelTraining(
                model_trainer_config=self.model_training_config,
                data_transformation_artifacts=data_transformation_artifacts,
            )
            model_trainer_artifact = model_trainer.initiate_model_training()

            logging.info("Performed the Model training operation")
            logging.info(
                "Exited the start_model_training method of Train pipeline class"
            )
            return model_trainer_artifact

        except Exception as e:
            raise CustomException(e, sys) from e  

    def start_model_evaluation(
        self,
        data_transformation_artifact: DataTransformationArtifact,
        model_trainer_artifact: ModelTrainerArtifact,
    ) -> ModelEvaluationArtifacts:
        try:
            logging.info(
                "Entered the start_model_evaluation method of Train pipeline class"
            )
            model_evaluation = ModelEvaluation(
                data_transformation_artifacts=data_transformation_artifact,
                model_training_artifacts=model_trainer_artifact,
                model_evaluation_config=self.model_evaluation_config,
            )

            model_evaluation_artifact = model_evaluation.initiate_model_evaluation()

            logging.info(
                "Exited the start_model_evaluation method of Train pipeline class"
            )
            return model_evaluation_artifact

        except Exception as e:
            raise CustomException(e, sys) from e 
    def start_model_pusher(
        self, model_evaluation_artifact: ModelEvaluationArtifacts
    ) -> ModelPusherArtifacts:
        try:
            logging.info(
                "Entered the start_model_pusher method of Train pipeline class"
            )
            model_pusher = ModelPusher(
                model_evaluation_artifact=model_evaluation_artifact,
                model_pusher_config=self.model_pusher_config,
            )
            model_pusher_artifact = model_pusher.initiate_model_pusher()

            logging.info("Exited the start_model_pusher method of Train pipeline class")
            return model_pusher_artifact

        except Exception as e:
            raise CustomException(e, sys) from e 
    def run_pipeline(self):
        try:
            data_ingestion_artifact=self.start_data_ingestion()
            data_transformation_artifact=self.start_data_transformation(data_ingestion_artifact=data_ingestion_artifact)
            model_training_artifact=self.start_model_training(data_transformation_artifacts=data_transformation_artifact)
            model_evaluation_artifact=self.start_model_evaluation(data_transformation_artifact=data_ingestion_artifact,
                                                                       model_trainer_artifact=model_training_artifact)
            self.model_pusher_config=self.start_model_pusher(model_evaluation_artifact=model_evaluation_artifact)
        except Exception as e:
            raise CustomException(e, sys) from e
    
