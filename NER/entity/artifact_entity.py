from dataclasses import dataclass



@dataclass
class DataIngestionArtifact:
    zip_data_file_path:str
    data_file_path:str

