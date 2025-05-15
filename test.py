# import streamlit as st
# import boto3
# import os
# from botocore.exceptions import NoCredentialsError

# # S3 configuration
# S3_BUCKET = 'bucket-for-henessy'
# S3_REGION = 'us-east-1'  # e.g., 'us-east-1'

# # Initialize S3 client
# s3_client = boto3.client('s3', region_name=S3_REGION)


# def upload_to_s3(file, filename):
#     try:
#         s3_client.upload_fileobj(file, S3_BUCKET, filename)
#         return True
#     except NoCredentialsError:
#         st.error("AWS credentials not found.")
#         return False
#     except Exception as e:
#         st.error(f"Error uploading file: {e}")
#         return False

# # Streamlit UI
# st.title("📁 File Uploader to S3")
# uploaded_file = st.file_uploader("Choose a file", type=None)
# if uploaded_file is not None:
#     st.write("File name:", uploaded_file.name)
#     s3_key=f"results/{uploaded_file.name}"
    
#     uploaded_url=f's3://bucket-for-henessy/{s3_key}'
#     if st.button("Upload to S3"):
#         with st.spinner("Uploading..."):
#             success = upload_to_s3(uploaded_file, s3_key)
#             if success:
#                 st.write(f"this is the S3 URL:{uploaded_url}")
#                 st.success(f"✅ Uploaded {uploaded_file.name} to S3 bucket '{S3_BUCKET}'")


import boto3
session = boto3.Session()
credentials = session.get_credentials()
frozen_creds = credentials.get_frozen_credentials()
print("Access Key:", frozen_creds.access_key)
print("Secret Key:", frozen_creds.secret_key)
print("Session Token:", frozen_creds.token)