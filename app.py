from NER.configuration.gcloud import GCloud
from NER.constants import *
from NER.pipeline.train_pipeline import TrainPipeline
import sys
from NER.exception import CustomException
try:
    obj=TrainPipeline()
    obj.run_pipeline()
except Exception as e:
    raise CustomException(e,sys) from e