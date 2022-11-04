import logging
import os

import boto3
from flask import Flask, render_template, redirect, request
import serverless_wsgi

from logger import setup_logger


LOCALSTACK_URL = os.environ.get("LOCALSTACK_URL")
S3_BUCKET = os.environ.get("S3_BUCKET")

ARCHIVES = "archive"

FOLDERS = [ARCHIVES]

LATEST_FILES = ["latest.csv"]

FLASK_HOST = os.environ.get("FLASK_HOST", "0.0.0.0")
FLASK_PORT = os.environ.get("FLASK_PORT", 5000)
FLASK_DEBUG = os.environ.get("FLASK_DEBUG", False)

APP = Flask(__name__)


@APP.route("/")
def home():
    return render_template("index.html", files=LATEST_FILES)


@APP.route(f"/{ARCHIVES}")
def get_archive_files():
    try:
        files = [f.split("/")[1] for f in list_bucket_contents(ARCHIVES)]
        logging.debug(f"Files in {ARCHIVES} folder: {files}")
        return render_template("folder.html", folder=ARCHIVES, files=files)
    except Exception as exc:
        return f"Exception: {exc}"


def list_bucket_contents(folder: str) -> list[str]:
    logging.debug(f"Listing bucket contents for folder {folder}")
    client = create_s3_client()
    response = client.list_objects(Bucket=S3_BUCKET,
                                 Prefix=f"{folder}/",
                                 Delimiter="/"
                                )
    contents = []
    for obj in response.get("Contents", []):
        contents.append(obj.get("Key"))

    logging.debug(f"Listed objects for prefix {folder}: {contents}")
    return contents


@APP.route("/url")
def get_presigned_url():
    args = request.args
    folder = args.get('folder', '')
    file_name = args.get('file_name', '')
    target = ""
    if not folder:
        target = file_name
    else:
        target = f"{folder}/{file_name}"
    logging.debug(f"Creating presigned URL for {target}")
    client = create_s3_client()
    params = {"Bucket": S3_BUCKET, "Key": f"{target}"}
    return redirect(client.generate_presigned_url("get_object", Params=params, ExpiresIn=60))


def create_s3_client() -> object:
    if LOCALSTACK_URL:
        logging.debug(f"Creating an S3 client using Localstack at {LOCALSTACK_URL}")
        return boto3.client("s3", endpoint_url=LOCALSTACK_URL)
    logging.debug("Creating an S3 client using AWS")
    return boto3.client("s3")


def handler(event, context):
    return serverless_wsgi.handle_request(APP, event, context)


if __name__ == "__main__":
    setup_logger()
    logging.info("Starting Flask...")
    APP.run(FLASK_HOST, FLASK_PORT, debug=FLASK_DEBUG)
