import os

import pytest

from airflow.models import DagBag
from airflow.utils import db
import logging

from pymongo import MongoClient

from ted_sws import config
from ted_sws.data_manager.adapters.notice_repository import NoticeRepository
from ted_sws.mapping_suite_processor.services.conceptual_mapping_processor import \
    mapping_suite_processor_from_github_expand_and_load_package_in_mongo_db
from tests import TESTS_PATH

AIRFLOW_DAG_FOLDER = TESTS_PATH.parent.resolve() / "dags"

MAPPING_SUITE_ID = "package_F03_test"


@pytest.fixture(scope="session")
def dag_bag():
    os.environ["AIRFLOW_HOME"] = str(AIRFLOW_DAG_FOLDER)
    os.environ["AIRFLOW__CORE__LOAD_EXAMPLES"] = "False"
    # Initialising the Airflow DB so that it works properly with the new AIRFLOW_HOME
    logging.disable(logging.CRITICAL)
    db.resetdb()
    db.initdb()
    logging.disable(logging.NOTSET)
    dag_bag = DagBag(dag_folder=AIRFLOW_DAG_FOLDER, include_examples=False,
                     read_dags_from_db=False)
    return dag_bag


@pytest.fixture
def mapping_suite_id():
    return MAPPING_SUITE_ID


@pytest.fixture
def mongodb_client():
    mongodb_client = MongoClient(config.MONGO_DB_AUTH_URL)
    mongodb_client.drop_database(config.MONGO_DB_AGGREGATES_DATABASE_NAME)
    return mongodb_client


@pytest.fixture
def notice_repository(mongodb_client, mapping_suite_id):
    mapping_suite_processor_from_github_expand_and_load_package_in_mongo_db(
        mapping_suite_package_name=mapping_suite_id,
        mongodb_client=mongodb_client,
        load_test_data=True
    )
    return NoticeRepository(mongodb_client=mongodb_client)
