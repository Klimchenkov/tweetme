import os
from dotenv import load_dotenv, find_dotenv
from storages.backends.s3boto3 import S3Boto3Storage

load_dotenv(find_dotenv())

YANDEX_CLIENT_DOCS_BUCKET_NAME = os.environ['YANDEX_CLIENT_DOCS_BUCKET_NAME']

class ClientDocsStorage(S3Boto3Storage):
    bucket_name = YANDEX_CLIENT_DOCS_BUCKET_NAME
    file_overwrite = False