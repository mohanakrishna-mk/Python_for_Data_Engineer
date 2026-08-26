import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

import aws


def test_get_secret_boto3(monkeypatch):
    class FakeClient:
        def get_secret_value(self, SecretId):
            return {
                "SecretString": '{"clientId":"id","clientSecret":"secret"}'
            }

    class FakeBoto3:
        def client(self, service_name, region_name):
            assert service_name == "secretsmanager"
            return FakeClient()

    monkeypatch.setattr(aws, "boto3", FakeBoto3())

    result = asyncio.run(
        aws.get_secret("symantic", "ap-south-1")
    )

    assert result["clientId"] == "id"


def test_upload_s3_boto3(monkeypatch):
    class FakeClient:
        def put_object(self, **kwargs):
            return {"ETag": "test"}

    class FakeBoto3:
        def client(self, service_name, region_name):
            assert service_name == "s3"
            return FakeClient()

    monkeypatch.setattr(aws, "boto3", FakeBoto3())

    result = asyncio.run(
        aws.upload_s3(
            "bucket",
            "key",
            b"data",
            "ap-south-1",
        )
    )

    assert result["ETag"] == "test"
