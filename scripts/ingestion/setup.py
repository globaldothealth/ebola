import logging
import os
from time import sleep

import boto3
import requests
from pymongo import MongoClient
from pymongo.errors import PyMongoError


LOCALSTACK_URL = os.environ.get("AWS_ENDPOINT", "http://localstack:4566")
S3_BUCKET = os.environ.get("S3_BUCKET", "test")

DB_CONNECTION = os.environ.get("DB_CONNECTION", "test")
DATABASE_NAME = os.environ.get("DB_NAME", "monkeypox")

GH_COLLECTION = os.environ.get("GH_COLLECTION", "gh")

MAX_ATTEMPTS = 42
WAIT_TIME = 5


def wait_for_localstack():
	logging.info("Waiting for localstack")
	healthcheck_url = "".join([LOCALSTACK_URL, "/health"])
	counter = 0
	while counter < MAX_ATTEMPTS:
		try:
			response = requests.get(healthcheck_url)
			s3_status = response.json().get("services", {}).get("s3")
			if s3_status in ["available", "ready"]:
				return
		except requests.exceptions.ConnectionError:
			pass
		counter += 1
		sleep(WAIT_TIME)
	raise Exception("Localstack not available")


def wait_for_database():
	logging.info("Waiting for database")
	counter = 0
	while counter < MAX_ATTEMPTS:
		try:
			client = MongoClient(DB_CONNECTION)
			logging.info(f"Connected with access to: {client.list_database_names()}")
			return
		except PyMongoError:
			logging.info(f"Database service not ready yet, retrying in {WAIT_TIME} seconds")
			pass
		counter += 1
		sleep(WAIT_TIME)
	raise Exception("Database service not available")


def create_bucket(bucket_name:str) -> None:
	logging.info(f"Creating S3 bucket {bucket_name}")
	s3_client = boto3.client("s3", endpoint_url=LOCALSTACK_URL)
	s3_client.create_bucket(Bucket=bucket_name)


def create_database():
	logging.info(f"Creating {DATABASE_NAME} database, or confirming it exists")
	client = MongoClient(DB_CONNECTION)
	database = client[DATABASE_NAME]
	logging.info("Creating collections")
	_ = database[GH_COLLECTION]


if __name__ == "__main__":
	logging.info("Starting local/testing setup script")
	wait_for_localstack()
	wait_for_database()
	create_database()
	create_bucket(S3_BUCKET)
	logging.info("Done")