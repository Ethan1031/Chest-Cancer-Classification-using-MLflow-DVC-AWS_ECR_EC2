import os
import zipfile
import requests
from cnnClassifier import logger
from cnnClassifier.utils.common import get_size
from cnnClassifier.entity.config_entity import DataIngestionConfig


class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def download_file(self) -> str:
        '''
        Fetch data from the url using requests instead of gdown
        '''
        try: 
            dataset_url = self.config.source_URL
            zip_download_dir = self.config.local_data_file
            os.makedirs(os.path.dirname(zip_download_dir), exist_ok=True)
            logger.info(f"Downloading data from {dataset_url} into file {zip_download_dir}")

            # Extract file ID from Google Drive URL
            if "drive.google.com/file/d/" in dataset_url:
                file_id = dataset_url.split("/file/d/")[1].split("/")[0]
            else:
                file_id = dataset_url.split("/")[-2]
            
            logger.info(f"File ID: {file_id}")
            
            # Construct direct download URL for Google Drive
            download_url = f"https://drive.google.com/uc?export=download&id={file_id}"
            
            # For larger files that might trigger the virus scan warning
            session = requests.Session()
            
            # First request to get cookies and confirmation token if needed
            response = session.get(download_url, stream=True)
            
            # Check if we got the download warning page
            if 'text/html' in response.headers.get('Content-Type', ''):
                logger.info("Handling Google Drive download warning")
                # Need to handle the confirmation page
                import re
                confirmation_token = re.search('confirm=([0-9A-Za-z]+)', response.text)
                if confirmation_token:
                    download_url = f"{download_url}&confirm={confirmation_token.group(1)}"
                    logger.info(f"Using confirmation URL: {download_url}")
                    response = session.get(download_url, stream=True)
            
            # Save the file
            with open(zip_download_dir, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            logger.info(f"Downloaded file size: {os.path.getsize(zip_download_dir)} bytes")
            
            # Verify the file is a zip file
            self._verify_zip_file(zip_download_dir)
            
            logger.info(f"Successfully downloaded ZIP file to {zip_download_dir}")
            return zip_download_dir

        except Exception as e:
            logger.error(f"Error downloading file: {str(e)}")
            raise e
    
    def _verify_zip_file(self, file_path):
        '''
        Verify if the file is a valid zip file
        '''
        try:
            # Try to open it as a zip file - this will raise BadZipFile if it's not a zip
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                # Check if it has at least one file
                if len(zip_ref.namelist()) == 0:
                    raise Exception("ZIP file is empty")
            logger.info(f"Verified {file_path} is a valid ZIP file")
            return True
        except zipfile.BadZipFile:
            # If not a zip file, examine and log file content
            try:
                with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                    content_preview = f.read(200)
                    logger.error(f"Invalid ZIP file content preview: {content_preview}")
            except Exception as read_err:
                logger.error(f"Could not read file content: {str(read_err)}")
                
            # Remove the invalid file
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"Removed invalid file: {file_path}")
                
            raise Exception(f"Downloaded file is not a valid ZIP archive: {file_path}")
    
    def extract_zip_file(self):
        """
        Extracts the zip file into the data directory
        """
        try:
            unzip_path = self.config.unzip_dir
            os.makedirs(unzip_path, exist_ok=True)
            
            # Verify it's a zip file before extracting
            if not os.path.exists(self.config.local_data_file):
                raise Exception(f"Zip file not found at {self.config.local_data_file}")
                
            self._verify_zip_file(self.config.local_data_file)
            
            with zipfile.ZipFile(self.config.local_data_file, 'r') as zip_ref:
                zip_ref.extractall(unzip_path)
                
            logger.info(f"Extracted zip file to {unzip_path}")
            return unzip_path
        except Exception as e:
            logger.error(f"Error extracting zip file: {str(e)}")
            raise e