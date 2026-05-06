import io
import os
from datetime import datetime, timezone

import boto3
import pandas as pd
from pymongo import MongoClient


def env(name: str, default: str = "") -> str:
    value = os.getenv(name, default).strip()
    if not value:
        raise ValueError(f"Missing env var: {name}")
    return value


def load_collection(client: MongoClient, db_name: str, collection_name: str) -> pd.DataFrame:
    collection = client[db_name][collection_name]
    rows = list(collection.find({}, {"_id": 0}))
    return pd.DataFrame(rows)


def to_buffer(df: pd.DataFrame, output_format: str) -> tuple[io.BytesIO, str]:
    buffer = io.BytesIO()
    if output_format == "json":
        payload = df.to_json(orient="records", date_format="iso", force_ascii=False)
        buffer.write(payload.encode("utf-8"))
        return buffer, "json"

    csv_payload = df.to_csv(index=False)
    buffer.write(csv_payload.encode("utf-8"))
    return buffer, "csv"


def upload_to_s3(s3_client, bucket: str, key: str, payload: io.BytesIO) -> None:
    payload.seek(0)
    s3_client.upload_fileobj(payload, bucket, key)


def main() -> None:
    service_name = env("SERVICE_NAME")
    mongo_uri = env("MONGO_URI")
    mongo_database = env("MONGO_DATABASE")
    collections_raw = env("COLLECTIONS")
    bucket = env("S3_BUCKET")
    region = env("AWS_REGION", "us-east-1")
    s3_prefix = env("S3_PREFIX", "raw")
    output_format = env("OUTPUT_FORMAT", "csv").lower()

    if output_format not in {"csv", "json"}:
        raise ValueError("OUTPUT_FORMAT must be csv or json")

    collections = [c.strip() for c in collections_raw.split(",") if c.strip()]
    if not collections:
        raise ValueError("COLLECTIONS must include at least one collection")

    mongo_client = MongoClient(mongo_uri)
    s3_client = boto3.client("s3", region_name=region)
    ingestion_ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    for collection_name in collections:
        df = load_collection(mongo_client, mongo_database, collection_name)
        payload, extension = to_buffer(df, output_format)
        key = f"{s3_prefix}/{service_name}/{collection_name}/ingestion_ts={ingestion_ts}/{collection_name}.{extension}"
        upload_to_s3(s3_client, bucket, key, payload)
        print(f"Uploaded: s3://{bucket}/{key} rows={len(df)}")


if __name__ == "__main__":
    main()
