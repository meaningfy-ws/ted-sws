from pymongo import MongoClient

from dags.load_mapping_suite_in_mongodb import \
    FETCH_MAPPING_SUITE_PACKAGE_FROM_GITHUB_INTO_MONGODB, MAPPING_SUITE_PACKAGE_NAME_DAG_PARAM_KEY
from ted_sws import config
from ted_sws.data_manager.adapters.mapping_suite_repository import MappingSuiteRepositoryMongoDB
from tests.unit.dags import run_task

MAPPING_SUITE_ID = "package_F03_test"


def test_loading_mapping_suite_in_mongodb(dag_bag):
    assert dag_bag.import_errors == {}
    dag = dag_bag.get_dag(dag_id="load_mapping_suite_in_mongodb")
    worker_dag = dag_bag.get_dag(dag_id="worker_single_notice_process_orchestrator")
    assert dag is not None
    assert worker_dag is not None
    mongodb_client = MongoClient(config.MONGO_DB_AUTH_URL)
    mongodb_client.drop_database(config.MONGO_DB_AGGREGATES_DATABASE_NAME)
    assert dag.has_task(FETCH_MAPPING_SUITE_PACKAGE_FROM_GITHUB_INTO_MONGODB)
    fetch_step = dag.get_task(FETCH_MAPPING_SUITE_PACKAGE_FROM_GITHUB_INTO_MONGODB)
    assert fetch_step
    mapping_suite_repository = MappingSuiteRepositoryMongoDB(mongodb_client=mongodb_client)
    mapping_suite = mapping_suite_repository.get(reference=MAPPING_SUITE_ID)
    assert mapping_suite is None
    task_instance = run_task(dag=dag, task=fetch_step,
                             conf={MAPPING_SUITE_PACKAGE_NAME_DAG_PARAM_KEY: MAPPING_SUITE_ID, "load_test_data": True})
    mapping_suite = mapping_suite_repository.get(reference=MAPPING_SUITE_ID)
    assert mapping_suite is not None
    assert task_instance.state == "success"
    mongodb_client.drop_database(config.MONGO_DB_AGGREGATES_DATABASE_NAME)
