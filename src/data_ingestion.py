import os
import pandas as pd
from azure.identity import ClientSecretCredential
from azure.storage.blob import BlobServiceClient
from src.logger import get_logger
from src.custom_exception import CustomException
from config.path_config import *
from utils.common_function import read_yaml
import sys
from dotenv import load_dotenv  # Add this import

# Load environment variables from .env file
load_dotenv()  # Add this line

logger = get_logger(__name__)

class DataIngestion:
    def __init__(self, config):
        self.config = config["data_ingestion"]
        self.container_name = self.config["bucket_name"]  # Azure uses "container" instead of bucket
        self.file_names = self.config["bucket_file_names"]

        os.makedirs(RAW_DIR, exist_ok=True)
        logger.info("Data Ingestion Started....")

        # Load Azure credentials from environment variables
        self.tenant_id = os.getenv("AZURE_TENANT_ID")
        self.client_id = os.getenv("AZURE_CLIENT_ID")
        self.client_secret = os.getenv("AZURE_CLIENT_SECRET")
        self.account_name = self.config["storage_account_name"]  # Add this to your YAML

        if not all([self.tenant_id, self.client_id, self.client_secret, self.account_name]):
            raise CustomException("Azure credentials or storage account not set in env/YAML", sys.exc_info())

        # Authenticate with Azure
        self.credential = ClientSecretCredential(
            tenant_id=self.tenant_id,
            client_id=self.client_id,
            client_secret=self.client_secret
        )

        self.account_url = f"https://{self.account_name}.blob.core.windows.net"
        self.blob_service_client = BlobServiceClient(account_url=self.account_url, credential=self.credential)
        self.container_client = self.blob_service_client.get_container_client(self.container_name)

    def download_csv_from_azure(self):
        try:
            for file_name in self.file_names:
                file_path = os.path.join(RAW_DIR, file_name)

                blob_client = self.container_client.get_blob_client(file_name)
                
                # Download blob
                with open(file_path, "wb") as f:
                    f.write(blob_client.download_blob().readall())

                # Handle large file (animelist.csv)
                if file_name == "animelist.csv":
                    data = pd.read_csv(file_path, nrows=5000000)
                    data.to_csv(file_path, index=False)
                    logger.info("Large file detected: Only downloading 5M rows")
                else:
                    logger.info(f"Downloading smaller file: {file_name}")

        except Exception as e:
            logger.error("Error while downloading data from Azure")
            raise CustomException("Failed to download data", e)

    def run(self):
        try:
            logger.info("Starting Data Ingestion Process....")
            self.download_csv_from_azure()
            logger.info("Data Ingestion Completed...")
        except CustomException as ce:
            logger.error(f"CustomException : {str(ce)}")
        finally:
            logger.info("Data Ingestion DONE...")


if __name__ == "__main__":
    data_ingestion = DataIngestion(read_yaml(CONFIG_PATH))
    data_ingestion.run()
