import datetime

from airflow.operators.trigger_dagrun import TriggerDagRunOperator

from dags import DEFAULT_DAG_ARGUMENTS
from airflow.decorators import dag, task
from airflow.operators.python import get_current_context
from pymongo import MongoClient

from dags.index_and_normalise_notice_worker import NOTICE_ID
from ted_sws import config
from ted_sws.core.model.notice import NoticeStatus
from ted_sws.data_manager.adapters.notice_repository import NoticeRepository

from ted_sws.notice_fetcher.adapters.ted_api import TedAPIAdapter, TedRequestAPI
from ted_sws.notice_fetcher.services.notice_fetcher import NoticeFetcher

DATE_WILD_CARD_KEY = "date_wild_card"


@dag(default_args=DEFAULT_DAG_ARGUMENTS, schedule_interval=None, tags=['worker', 'fetch_notices_per_day'])
def fetch_notices_per_day_worker():
    @task
    def fetch_notices_and_trigger_index_and_normalise_notice_worker():
        context = get_current_context()
        dag_conf = context["dag_run"].conf

        if DATE_WILD_CARD_KEY not in dag_conf.keys():
            raise "Config key [date] is not present in dag context"

        mongodb_client = MongoClient(config.MONGO_DB_AUTH_URL)
        notice_ids = NoticeFetcher(notice_repository=NoticeRepository(mongodb_client=mongodb_client),
                                   ted_api_adapter=TedAPIAdapter(
                                       request_api=TedRequestAPI())).fetch_notices_by_date_wild_card(
            wildcard_date=dag_conf[DATE_WILD_CARD_KEY])  # "20220203*"
        for notice_id in notice_ids:
            restart_dag_operator = True
            while restart_dag_operator:
                restart_dag_operator = False
                try:
                    TriggerDagRunOperator(
                        task_id=f'trigger_index_and_normalise_notice_worker_dag_{notice_id}',
                        trigger_dag_id="index_and_normalise_notice_worker",
                        trigger_run_id=notice_id,
                        execution_date=datetime.datetime.now().replace(tzinfo=datetime.timezone.utc),
                        conf={NOTICE_ID: notice_id}
                    ).execute(context=context)
                except:
                    restart_dag_operator = True
                    print("trigger dag operator restarted !!!")

    fetch_notices_and_trigger_index_and_normalise_notice_worker()


dag = fetch_notices_per_day_worker()