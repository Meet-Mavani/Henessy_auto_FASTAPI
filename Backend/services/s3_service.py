import boto3
import io
from typing import List
from fastapi import HTTPException
from botocore.exceptions import BotoCoreError, NoCredentialsError

from apis.function111.bedrockClient import create_s3_client_from_bedrock, fetch_result_from_s3, invoke_bedrock_data_automation
from ..config import BUCKET_NAME, OUTPUT_BUCKET_PATH

class S3Service:
    def __init__(self):
        self.s3 = boto3.client("s3")
        self.uploaded_s3_urls = []

    def clear_uploaded_urls(self):
        self.uploaded_s3_urls = []

    def get_uploaded_urls(self) -> List[str]:
        return self.uploaded_s3_urls

    async def upload_file(self, folder: str, file_name: str, file_content, content_type: str):
        try:
            s3_key = f"{folder}/{file_name}"
            
            self.s3.upload_fileobj(
                Fileobj=io.BytesIO(file_content),
                Bucket=BUCKET_NAME,
                Key=s3_key,
                ExtraArgs={"ContentType": content_type}
            )
            
            file_url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{s3_key}"
            file_s3_url = f"s3://{BUCKET_NAME}/{s3_key}"
            self.uploaded_s3_urls.append(file_s3_url)
            
            return file_url, file_s3_url

        except NoCredentialsError:
            raise HTTPException(status_code=403, detail="AWS credentials not found")
        except BotoCoreError as e:
            raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")

    def process_s3_urls(self):
        results = {}
        for url in self.uploaded_s3_urls:
            try:
                # Invoke bedrock data automation
                s3_url = invoke_bedrock_data_automation(
                    url,
                    OUTPUT_BUCKET_PATH
                )
                
                # Fetch results from S3
                cached_result = fetch_result_from_s3(s3_url)
                
                # Determine document type
                if url.endswith('poa_sign.pdf'):
                    document_type = 'poa_blueprint'
                elif url.endswith('title.pdf'):
                    document_type = 'title'
                elif url.endswith('Used_Car_Trade.pdf'):
                    document_type = 'user_car_trade'
                else:
                    document_type = 'unknown'
                
                results[document_type] = cached_result
                
            except Exception as e:
                results[url] = {"error": str(e)}
        
        return results
