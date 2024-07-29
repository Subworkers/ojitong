import boto3
from urllib.parse import urlparse

class S3ImageUploader:
    def __init__(self***REMOVED***:
        self.s3_client = boto3.client('s3'***REMOVED***

    def _parse_s3_path(self, s3_path***REMOVED***:
        # bucket, key 파싱
        parsed_s3 = urlparse(s3_path***REMOVED***
        bucket_name = parsed_s3.netloc
        key_prefix = parsed_s3.path.lstrip('/'***REMOVED***
        return bucket_name, key_prefix

    def upload_image(self, image_stream, s3_path, extra_args={'ContentType': 'image/png'***REMOVED******REMOVED***:
        bucket_name, key_prefix = self._parse_s3_path(s3_path***REMOVED***
        self.s3_client.upload_fileobj(image_stream, Bucket=bucket_name, Key=key_prefix, ExtraArgs=extra_args***REMOVED***
        print(f"Image successfully uploaded to {bucket_name***REMOVED***/{key_prefix***REMOVED***"***REMOVED***