import boto3
import uuid
from botocore.exceptions import ClientError
from app.core.config import settings
from fastapi import UploadFile, HTTPException

# Initialize S3 only if keys are present
s3_client = None
if settings.AWS_ACCESS_KEY_ID and settings.AWS_SECRET_ACCESS_KEY:
    s3_client = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_REGION
    )

def upload_image_to_s3(file: UploadFile, folder: str = "uploads") -> str:
    if not s3_client or not settings.AWS_BUCKET_NAME:
        print("Warning: AWS credentials missing. Skipping real upload.")
        # Fallback fake URL so your frontend doesn't break during local testing
        return f"https://mock-s3-bucket.s3.amazonaws.com/{folder}/{file.filename}"
        
    try:
        file_extension = file.filename.split(".")[-1]
        unique_filename = f"{folder}/{uuid.uuid4()}.{file_extension}"
        
        s3_client.upload_fileobj(
            file.file,
            settings.AWS_BUCKET_NAME,
            unique_filename,
            ExtraArgs={"ContentType": file.content_type}
        )
        
        # Generate the S3 URL
        url = f"https://{settings.AWS_BUCKET_NAME}.s3.{settings.AWS_REGION}.amazonaws.com/{unique_filename}"
        return url
    except ClientError as e:
        print(f"S3 Upload Error: {e}")
        raise HTTPException(status_code=500, detail="Failed to upload image to AWS S3")
