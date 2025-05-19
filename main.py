from apis.function111.bedrockClient import create_s3_client_from_bedrock,fetch_result_from_s3,invoke_bedrock_data_automation
from typing import Optional,List
from Database.schema.add_data import store_data_in_DB
from Database.schema.starting_schema import Base
from Database.schema.connect import engine
from Database.schema.validate_data import validate_data
import boto3
from botocore.exceptions import BotoCoreError, NoCredentialsError
import uuid
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from botocore.exceptions import BotoCoreError, NoCredentialsError
import io
s3_buckets: List[str] = []

app=FastAPI()
Base.metadata.create_all(bind=engine)
@app.get("/")
async def get_started():
    return {"message":"Hello Guys"}

@app.get("/get-result/")
def get_result():
    print("in the get_result")
    try:
        for url in s3_buckets:
            print(type(url))
            s3_url = invoke_bedrock_data_automation(
                url,
                's3://meet-output-bucket-38/results/'
            )
            print("stopped here")
            print(f"Returned S3 URL: {s3_url}")
        
            print("Calling fetch_result_from_s3...")
            cached_result = fetch_result_from_s3(s3_url)
            print(f"Fetched Result: {cached_result}")
            if url.endswith('poa_sign.pdf'):
                
                if cached_result is None:
                    return {"error":"Please first load the data"}
                
                store_data_in_DB(cached_result,'poa_blueprint')
            elif url.endswith('title.pdf'):
                
                if cached_result is None:
                    return {"error":"Please first load the data"}
                
                store_data_in_DB(cached_result,'title')
            
            elif url.endswith('Used_Car_Trade.pdf'):
                if cached_result is None:
                    return {"error":"Please first load the data"}
                
                store_data_in_DB(cached_result,'user_car_trade')
        
        # return {"data": cached_result}

    except Exception as e:
        print(f"Unexpected Error: {e}")
        return {"error": str(e)}

BUCKET_NAME = "meet-input-bucket-38"
s3 = boto3.client("s3")


@app.post("/upload/")
async def upload_fixed_files(
    folder: str = Form(...),
    files: List[UploadFile] = File(...)
):
    global s3_buckets  # so you can modify the global list

    if len(files) != 2:
        raise HTTPException(status_code=400, detail="Exactly 2 files are required")

    file_mapping = {
        0: "poa_sign.pdf",
        1: "Used_Car_Trade.pdf"
    }

    uploaded_urls = []
    s3_buckets.clear()  # Reset previous uploads
    for idx, file in enumerate(files):
        try:
            file_content = await file.read()
            s3_key = f"{folder}/{file_mapping[idx]}"

            s3.upload_fileobj(
                Fileobj=io.BytesIO(file_content),
                Bucket=BUCKET_NAME,
                Key=s3_key,
                ExtraArgs={"ContentType": file.content_type}
            )

            file_url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{s3_key}"
            file_s3_url = f"s3://{BUCKET_NAME}/{s3_key}"
            s3_buckets.append(file_s3_url)
            uploaded_urls.append(file_url)

        except NoCredentialsError:
            raise HTTPException(status_code=403, detail="AWS credentials not found")
        except BotoCoreError as e:
            raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")

    return {
        "message": "Files uploaded successfully",
        "uploaded_files": {
            "poa_sign": uploaded_urls[0],
            "used_car_trade": uploaded_urls[1]
        }
    }
    
    
    
@app.get("/validation/")
async def validation():
    print("data validation started")
    validate_data()
    print("data validation ended")