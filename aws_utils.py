import boto3
import os
from dotenv import load_dotenv
load_dotenv()

S3_BUCKET = os.getenv("S3_BUCKET")
DYNAMODB_TABLE = os.getenv("DYNAMODB_TABLE")

session = boto3.Session(
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION")
)

s3 = session.client("s3")
dynamodb = session.resource("dynamodb")

def upload_to_s3(file_obj, filename, bucket_name):
    s3.upload_fileobj(file_obj, bucket_name, f"incoming/{filename}")
    return f"Uploaded {filename} to S3."

def generate_presigned_url(bucket_name, key, expires_in=3600):
    try:
        url = s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket_name, 'Key': key},
            ExpiresIn=expires_in
        )
        return url
    except Exception as e:
        return str(e)

def fetch_receipts(table_name):
    table = dynamodb.Table(table_name)
    response = table.scan()
    items = response.get("Items", [])

    for item in items:
        if isinstance(item.get("items"), list):
            item["items"] = "\n".join([
                f"{i.get('name', 'Item')} - {i.get('price', '')}"
                for i in item["items"]
            ])
        if "s3_path" in item:
            key = item["s3_path"].split("s3://")[1].split("/", 1)[1]
            item["s3_url"] = generate_presigned_url(S3_BUCKET, key)
    return items

