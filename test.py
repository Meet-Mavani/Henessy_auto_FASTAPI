import boto3

def download_file_from_s3(bucket_name, object_key, local_file_path):
    """
    Download a file from an S3 bucket
    
    Parameters:
        bucket_name (str): Name of the S3 bucket
        object_key (str): The key of the object in the S3 bucket (file path)
        local_file_path (str): Local path where the file will be saved
    
    Returns:
        bool: True if download was successful, False otherwise
    """
    try:
        # Create an S3 client
        s3_client = boto3.client('s3')
        
        # Download the file
        s3_client.download_file(bucket_name, object_key, local_file_path)
        
        print(f"Successfully downloaded {object_key} to {local_file_path}")
        return True
    
    except Exception as e:
        print(f"Error downloading file: {e}")
        return False

# Example usage
if __name__ == "__main__":
    # Replace these with your actual values
    bucket = "bda-input-bucket-9876"
    s3_file_key = "sahil3/title.pdf"
    download_path = "C:/Users/MeetMavani/Desktop/Henessy Auto POC/Code_of_FASTAPI/files"
    
    download_file_from_s3(bucket, s3_file_key, download_path)