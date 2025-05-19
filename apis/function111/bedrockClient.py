# ## do not run directly
 
# import boto3
# import json
# import re
# client=boto3.client('bedrock-data-automation-runtime')
 
# response=client.invoke_data_automation_async(
#     inputConfiguration={
#         's3Uri': 's3://bucket-for-henessy/bank_stmt_0.png'
#     },
#     outputConfiguration={
#         's3Uri': 's3://bucket-for-henessy/results/'
#     },
#     dataAutomationConfiguration={
#         'dataAutomationProjectArn': 'arn:aws:bedrock:us-east-1:050752609444:data-automation-project/736764fec041',
#         'stage': 'LIVE'
#     },
#      blueprints=[
#         {
#             'blueprintArn': 'arn:aws:bedrock:us-east-1:050752609444:blueprint/9c6933e98655',
#             'version': '1',
#             'stage':'LIVE'
#         },
#     ],
#      dataAutomationProfileArn='arn:aws:bedrock:us-east-1:050752609444:data-automation-profile/us.data-automation-v1',
   
# )
# print(response)
# temp='arn:aws:bedrock:us-east-1:050752609444:data-automation-invocation/55abe9b3-7885-42cb-9a2c-e428888d73d0'
 
# response1 = client.get_data_automation_status(
#     invocationArn=temp
# )
# s3url=response1['outputConfiguration']['s3Uri']
 
# match = re.search(r'([a-f0-9\-]{36})', s3url)
# uuid=''
# if match:
#     uuid1 = match.group(1)
#     print(uuid1)
# #s3://bucket-for-henessy/results//55abe9b3-7885-42cb-9a2c-e428888d73d0/0/custom_output/0/result.json
# #s3://bucket-for-henessy/results//55abe9b3-7885-42cb-9a2c-e428888d73d0/0/custom_output/0/result.json
# final_required_s3=f"s3://bucket-for-henessy/results//{uuid1}/0/custom_output/0/result.json"
# print(final_required_s3)
import boto3
import os
import json
from urllib.parse import urlparse
import re
import time
from dotenv import load_dotenv

load_dotenv()

def invoke_bedrock_data_automation(image_s3_uri, output_base_s3_uri):
    blueprints={
    "poa_sign.pdf":'arn:aws:bedrock:us-east-1:050752609444:blueprint/c6c8017c5f2c',
    # "title.pdf":"arn:aws:bedrock:us-east-1:943143228843:blueprint/af53ca55f1a3",
    "Used_Car_Trade.pdf":"arn:aws:bedrock:us-east-1:050752609444:blueprint/f2e2f4d28403"
    }
    final_version='1'
    if image_s3_uri.endswith('poa_sign.pdf'):
        final_blueprint=blueprints['poa_sign.pdf']
        final_version='1'
    # elif image_s3_uri.endswith('title.pdf'):
    #     final_blueprint=blueprints['title.pdf']
    elif image_s3_uri.endswith('Used_Car_Trade.pdf'):
        final_blueprint=blueprints['Used_Car_Trade.pdf']

    client = boto3.client('bedrock-data-automation-runtime')
 
    # Step 1: Invoke the Data Automation Blueprint
    response = client.invoke_data_automation_async(
        inputConfiguration={
            's3Uri': image_s3_uri
        },
        outputConfiguration={
            's3Uri': output_base_s3_uri
        },
        # dataAutomationConfiguration={
        #     'dataAutomationProjectArn': 'arn:aws:bedrock:us-east-1:050752609444:data-automation-project/736764fec041',
        #     'stage': 'LIVE'
        # },
        
        
        blueprints=[
            {
                'blueprintArn': final_blueprint,
                'version': final_version,
                'stage': 'LIVE'
            },
        ],
        dataAutomationProfileArn='arn:aws:bedrock:us-east-1:050752609444:data-automation-profile/us.data-automation-v1'
    )
 
    invocation_arn = response['invocationArn']
    print(f"Invocation started: {invocation_arn}")
 
    # Step 2: Poll until the status is SUCCEEDED or FAILED
    while True:
        status_response = client.get_data_automation_status(invocationArn=invocation_arn)
        status = status_response.get('status')
        print(f"Status: {status}")
 
        if status in ['Success', 'Failed']:
            break
        time.sleep(5)
 
    if status != 'Success':
        raise RuntimeError(f"Data automation failed: {status_response}")
 
    # Step 3: Extract UUID from the output S3 URI
    output_s3 = status_response['outputConfiguration']['s3Uri']
    match = re.search(r'([a-f0-9\-]{36})', output_s3)
    if not match:
        raise ValueError("UUID not found in output S3 URI.")
    uuid = match.group(1)
 
    # Step 4: Construct the final required S3 path
    final_s3_uri = f"{output_base_s3_uri}/{uuid}/0/custom_output/0/result.json"
    print(f"Final result S3 URI: {final_s3_uri}")
    return final_s3_uri
 


def create_s3_client_from_bedrock():
    
    bedrock = boto3.client(
        "bedrock-runtime",
        region_name=os.getenv("AWS_REGION", "us-east-1")
    )

    credentials = bedrock._request_signer._credentials  
    s3_client = boto3.client(
        "s3",
        region_name=os.getenv("AWS_REGION", "us-east-1"),
        aws_access_key_id=credentials.access_key,
        aws_secret_access_key=credentials.secret_key,
 
    )
    return s3_client

def fetch_result_from_s3(s3_uri: str):
    try:
        if s3_uri.startswith("s3://"):
            s3_uri = s3_uri.replace("s3://", "https://")
        url = urlparse(s3_uri)
        bucket = url.hostname
        key = url.path.lstrip("/")

        print(f'Fetching result from S3 - Bucket: "{bucket}", Key: "{key}"')

        s3_client = create_s3_client_from_bedrock()

        response = s3_client.get_object(Bucket=bucket, Key=key)
        body = response["Body"].read().decode("utf-8")
        result = json.loads(body)

        # print(result.get("inference_result"))
        return result.get("inference_result")

    except Exception as e:
        print(f"Error fetching from S3: {str(e)}")
        raise





