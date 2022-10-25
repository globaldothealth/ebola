from datetime import datetime
import json
import logging
import os
import sys
from urllib.parse import urlparse

import boto3
from pymongo import MongoClient
from pymongo.errors import PyMongoError
import pygsheets


DOCUMENT_ID = os.environ.get("DOCUMENT_ID")

S3 = boto3.resource("s3")
LOCALSTACK_URL = os.environ.get("LOCALSTACK_URL")

if LOCALSTACK_URL:
	S3 = boto3.resource("s3", endpoint_url=LOCALSTACK_URL)

S3_BUCKET = os.environ.get("S3_BUCKET")
S3_FOLDER = os.environ.get("S3_FOLDER")

DB_CONNECTION = os.environ.get("DB_CONNECTION")
DATABASE_NAME = os.environ.get("DATABASE_NAME")
GH_COLLECTION = os.environ.get("GH_COLLECTION")

MINIMUM_DATA = ["ID", "Date_confirmation", "Curator_initials", "Notes", "Country", "Status"]

PRIVATE_FIELDS = [
"Curator_initials", "Source", "Source_II", "Source_III", "Source_IV", "Source_V", "Source_VI", "Pathogen_status"
]

TODAY = datetime.today()


def setup_logger():
    h = logging.StreamHandler(sys.stdout)
    rootLogger = logging.getLogger()
    rootLogger.addHandler(h)
    rootLogger.setLevel(logging.DEBUG)


def get_data():
	logging.info("Getting data from Google Sheets")
	client = pygsheets.authorize(service_account_env_var="GOOGLE_CREDENTIALS")
	spreadsheet = client.open_by_key(DOCUMENT_ID)

	return spreadsheet[0].get_all_records()


def clean_data(data):
	logging.info("Cleaning data")
	for case in data:
		for field in PRIVATE_FIELDS:
			case.pop(field)
	return data


def format_data(data):
	logging.info("Formatting data")
	csv_data = ""
	column_names = data[0].keys()
	for name in column_names:
		csv_data += f"{name},"
	csv_data += "\n"
	for row in data:
		for val in row.values():
			csv_data += f"{str(val).replace(',', ';')},"
		csv_data += "\n"
	return csv_data


def store_data(csv_data):
	logging.info("Uploading data to S3")
	try:
		S3.Object(S3_BUCKET, f"{S3_FOLDER}/{TODAY}.csv").put(Body=csv_data)
		S3.Object(S3_BUCKET, f"latest.csv").put(Body=csv_data)
	except Exception as exc:
		logging.exception(f"An exception occurred while trying to upload files")
		raise


def data_to_db(data):
	logging.info("Adding data to the database")
	try:
		client = MongoClient(DB_CONNECTION)
		database = client[DATABASE_NAME]
		for entry in data:
			find = {"ID": entry["ID"]}
			update = {"$set": entry}
			database[GH_COLLECTION].update_one(find, update, upsert=True)
	except PyMongoError:
		logging.exception("An error occurred while trying to insert data")
		raise


if __name__ == "__main__":
	setup_logger()
	logging.info("Starting Ebola data ingestion")
	data = get_data()
	data = clean_data(data)
	csv_data = format_data(data)
	store_data(csv_data)
	data_to_db(data)
	logging.info("Work complete")
