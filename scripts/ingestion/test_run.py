import os

import boto3
from pymongo import MongoClient
import pytest

from run import (DB_CONNECTION, DATABASE_NAME, GH_COLLECTION, S3_BUCKET, LOCALSTACK_URL,
	clean_data, format_data, data_to_db, store_data)

CASE = {
    "ID": 1,
    "Date_confirmation": "2021-05-12",
    "Curator_initials": "ZZ",
    "Notes": "example note",
    "Country": "Uganda",
    "Status": "confirmed"
}

CLEAN_CASE = CASE.copy()
del CLEAN_CASE["Curator_initials"]
CLEAN_DATA = [CLEAN_CASE]

CSV_DATA = """
ID,Date_confirmation,Notes,Country,Status,
1,2021-05-12,example note,Uganda,confirmed,
"""


def get_contents(file_name: str) -> str:
	s3 = boto3.resource("s3", endpoint_url=LOCALSTACK_URL)
	obj = s3.Object(S3_BUCKET, file_name)
	return obj.get()["Body"].read().decode("utf-8")


def get_db_records(collection: str) -> list[dict]:
	db = MongoClient(DB_CONNECTION)[DATABASE_NAME][collection]
	cursor = db.find({})
	return [record for record in cursor]


def test_clean_data():
    assert clean_data([CASE]) == CLEAN_DATA


def test_format_data():
	assert format_data(CLEAN_DATA) == CSV_DATA


@pytest.mark.skipif(not os.environ.get("DOCKERIZED", False),
						reason="Running e2e tests outside of mock environment disabled")
def test_store_data():
	store_data(CSV_DATA)
	assert get_contents("latest.csv") == CSV_DATA


@pytest.mark.skipif(not os.environ.get("DOCKERIZED", False),
						reason="Running e2e tests outside of mock environment disabled")
def test_data_to_db():
	data_to_db(CLEAN_DATA)
	db_records = get_db_records(GH_COLLECTION)
	del db_records[0]["_id"]
	assert db_records == CLEAN_DATA
