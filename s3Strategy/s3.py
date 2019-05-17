import boto3
import logging
from botocore.exceptions import ClientError

class storage():
    def __init__(self):
        self.client = boto3.client('s3')

    def create_bucket(self, bucket_name):
        try:
            response =self.client.create_bucket(Bucket=bucket_name)
        except ClientError as e:
            logging.error(e)
            return False
        return response

    def list_bucket(self):
        response = self.client.list_buckets()
        print('Existing Buckets:')
        print(response)
        for bucket in response['Buckets']:
            print(f' {bucket["Name"]}')

    def upload_file(self, file_name, bucket, object_name=None):
         # if the object name is not available file name is used for object name
         if object_name is None:
             object_name = file_name

         try:
             response = self.client.upload_file(file_name, bucket, object_name)
         except ClientError as e:
             logging.error(e)
             return False
         return response


    def download_file(self, bucket, file_name, object_name):
        response =self.client.download_file(bucket, object_name, file_name)
        return response

    def get_object_url(self, file_name):
        key = self.client.get_key(file_name)
        url = key.generate_url(3600,query_auth =True, force_http = True)
        print(url)

