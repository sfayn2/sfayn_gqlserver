import os
from dotenv import load_dotenv

load_dotenv()

AWS_ACCESS_KEY_ID=os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY=os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME="josnin"
AWS_S3_ENDPOINT_URL="https://sgp1.digitaloceanspaces.com"
AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": "max-age=86400"
}
AWS_LOCATION = "static"

DEFAULT_FILE_STORAGE = "sfayn_gqlserver.cdn.backends.MediaRootS3Boto3Storage"
STATICFILES_STORAGE = "sfayn_gqlserver.cdn.backends.StaticRootS3Boto3Storage"
