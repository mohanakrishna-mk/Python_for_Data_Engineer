import asyncio
import json

import boto3


def _get_secret_sync(secret_name: str, region: str) -> dict:
    client = boto3.client(
        "secretsmanager",
        region_name=region,
    )

    response = client.get_secret_value(
        SecretId=secret_name,
    )

    secret_string = response.get("SecretString")

    if not secret_string:
        raise RuntimeError(
            f"Secret '{secret_name}' has no SecretString"
        )

    return json.loads(secret_string)


async def get_secret(secret_name: str, region: str) -> dict:
    """Official boto3 call executed off the FastAPI event loop."""
    return await asyncio.to_thread(
        _get_secret_sync,
        secret_name,
        region,
    )


def _upload_s3_sync(
    bucket: str,
    key: str,
    file_bytes: bytes,
    region: str,
):
    client = boto3.client(
        "s3",
        region_name=region,
    )

    return client.put_object(
        Bucket=bucket,
        Key=key,
        Body=file_bytes,
    )


async def upload_s3(
    bucket: str,
    key: str,
    file_bytes: bytes,
    region: str,
):
    """Official boto3 call executed off the FastAPI event loop."""
    return await asyncio.to_thread(
        _upload_s3_sync,
        bucket,
        key,
        file_bytes,
        region,
    )
