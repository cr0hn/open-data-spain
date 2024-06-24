import io

import orjson

from minio import Minio as MinioClient

from django.conf import settings


def upload_json_to_s3(object_name: str, content: dict):
    minio = MinioClient(
        settings.MINIO_HOST,
        access_key=settings.MINIO_ACCESS_KEY,
        secret_key=settings.MINIO_SECRET_KEY,
        secure=settings.MINIO_SECURE
    )

    minio_data = io.BytesIO()
    minio_data_length = minio_data.write(orjson.dumps(content, option=orjson.OPT_INDENT_2))
    minio_data.seek(0)

    minio.put_object(
        bucket_name=settings.MINIO_BUCKET,
        object_name=object_name,
        data=minio_data,
        length=minio_data_length
    )


__all__ = ('upload_json_to_s3',)
