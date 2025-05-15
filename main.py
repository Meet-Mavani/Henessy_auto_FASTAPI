from fastapi import FastAPI
from apis.function111.bedrockClient import create_s3_client_from_bedrock,fetch_result_from_s3,invoke_bedrock_data_automation
from typing import Optional
from Database.schema.add_data import store_data_in_DB
from Database.schema.starting_schema import Base
from Database.schema.connect import engine

app=FastAPI()
Base.metadata.create_all(bind=engine)
@app.get("/")
async def get_started():
    return {"message":"Hello Guys"}

s3_buckets=["s3://bda-input-bucket-9876/sahil3/Used_Car_Trade.pdf","s3://bda-input-bucket-9876/sahil3/poa_sign.pdf","s3://bda-input-bucket-9876/sahil3/title.pdf"]
@app.get("/get-result/")
def get_result():
    print("in the get_result")
    try:
        for url in s3_buckets:
            print(type(url))
            s3_url = invoke_bedrock_data_automation(
                url,
                's3://meet-output-bucket-21/results/'
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
