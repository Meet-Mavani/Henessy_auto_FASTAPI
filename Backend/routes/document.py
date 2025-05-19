from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from typing import List

from Database.schema.add_data import store_data_in_DB
from ..services.s3_service import S3Service

router = APIRouter()
s3_service = S3Service()

@router.post("/upload/")
async def upload_fixed_files(
    folder: str = Form(...),
    files: List[UploadFile] = File(...)
):
    if len(files) != 2:
        raise HTTPException(status_code=400, detail="Exactly 2 files are required")

    file_mapping = {
        0: "poa_sign.pdf",
        1: "Used_Car_Trade.pdf"
    }

    s3_service.clear_uploaded_urls()
    uploaded_urls = {}
    
    for idx, file in enumerate(files):
        file_content = await file.read()
        file_url, _ = await s3_service.upload_file(
            folder=folder,
            file_name=file_mapping[idx],
            file_content=file_content,
            content_type=file.content_type
        )
        
        key_name = "poa_sign" if idx == 0 else "used_car_trade"
        uploaded_urls[key_name] = file_url

    return {
        "message": "Files uploaded successfully",
        "uploaded_files": uploaded_urls
    }

@router.get("/get-result/")
async def get_result():
    try:
        # Get results from S3
        results = s3_service.process_s3_urls()
        
        # Store data in DB
        for doc_type, result in results.items():
            if result is None:
                continue
                
            if "error" not in result:
                store_data_in_DB(result, doc_type)
        
        return {"message": "Data processed and stored successfully", "results": results}
        
    except Exception as e:
        return {"error": str(e)}