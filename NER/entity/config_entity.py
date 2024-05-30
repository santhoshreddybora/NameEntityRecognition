from dataclasses import dataclass
from NER.constants import *
import os

@dataclass
class DataIngestionConfig:
    def __init__(self,):
        self.data_ingestion_artifact_dir:str = os.path.join(ARTIFACTS_DIR, DATA_INGESTION_ARTIFACTS_DIR)
        self.gcp_data_file_path: str = os.path.join(
            self.data_ingestion_artifact_dir, GCP_DATA_FILE_NAME
        )
        self.output_file_path: str = self.data_ingestion_artifact_dir
        self.csv_data_file_path: str = os.path.join(
            self.data_ingestion_artifact_dir, CSV_DATA_FILE_NAME
        )    
    
    