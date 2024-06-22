from ner.configuration.gcloud import GCloud
from ner.constants import *
from ner.pipeline.train_pipeline import TrainPipeline
import sys
from ner.exception import NerException
try:
    obj=TrainPipeline()
    obj.run_pipeline()
except Exception as e:
    raise NerException(e,sys) from e