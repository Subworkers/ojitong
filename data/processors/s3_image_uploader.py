import boto3
from urllib.parse import urlparse

class S3ImageUploader:
    def __init__(self):
        self.s3_client = boto3.client('s3')

    def _parse_s3_path(self, s3_path):
        # bucket, key 파싱
        parsed_s3 = urlparse(s3_path)
        bucket_name = parsed_s3.netloc
        key_prefix = parsed_s3.path.lstrip('/')
        return bucket_name, key_prefix

    def upload_image(self, image_stream, s3_path, extra_args={'ContentType': 'image/png'}):
        bucket_name, key_prefix = self._parse_s3_path(s3_path)
        self.s3_client.upload_fileobj(image_stream, Bucket=bucket_name, Key=key_prefix, ExtraArgs=extra_args)
        print(f"Image successfully uploaded to {bucket_name}/{key_prefix}")