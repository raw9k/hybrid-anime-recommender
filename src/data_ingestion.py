import os, pandas as pd
from src.custom_exception import CustomException
from src.logger import get_logger
from config.path_config import *
from utils.common_function import read_yaml

logger = get_logger(__name__)

class DataIngestion:
    def __init__(self,config):
        self.config = config["data_ingestion"]
        self.bucket_name = self.config["bucket_name"]
        self.file_names = self.config["bucket_file_names"]
        
        os.makedirs(RAW_DIR,exist_ok=True)
        
        logger.info("Data Ingestion Started.....")
        
    