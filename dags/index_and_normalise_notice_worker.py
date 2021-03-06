from airflow.decorators import dag, task
from airflow.operators.python import get_current_context
from pymongo import MongoClient

from dags import DEFAULT_DAG_ARGUMENTS
from dags.dags_utils import pull_dag_upstream, push_dag_downstream
from ted_sws import config
from ted_sws.data_manager.adapters.notice_repository import NoticeRepository
from ted_sws.data_sampler.services.notice_xml_indexer import index_notice
from ted_sws.event_manager.adapters.event_log_decorator import event_log
from ted_sws.event_manager.adapters.event_logger import EventLogger
from ted_sws.event_manager.model.event_message import NoticeEventMessage
from ted_sws.event_manager.services.logger_from_context import get_logger_from_dag_context, \
    handle_event_message_metadata_dag_context
from ted_sws.notice_metadata_processor.services.metadata_normalizer import normalise_notice_by_id

NOTICE_ID = "notice_id"


@dag(default_args=DEFAULT_DAG_ARGUMENTS,
     schedule_interval=None,
     tags=['worker', 'index_and_normalise_notice'])
def index_and_normalise_notice_worker():
    """

    :return:
    """

    @task
    @event_log(is_loggable=False)
    def index_notice_step(**context_args):
        """

        :return:
        """
        event_logger: EventLogger = get_logger_from_dag_context(context_args)
        event_message = NoticeEventMessage()
        event_message.start_record()

        context = get_current_context()
        dag_params = context["dag_run"].conf
        notice_id = dag_params[NOTICE_ID]

        push_dag_downstream(key=NOTICE_ID, value=notice_id)
        mongodb_client = MongoClient(config.MONGO_DB_AUTH_URL)
        notice_repository = NoticeRepository(mongodb_client=mongodb_client)
        notice = notice_repository.get(reference=notice_id)
        indexed_notice = index_notice(notice=notice)
        notice_repository.update(notice=indexed_notice)

        handle_event_message_metadata_dag_context(event_message, context)
        event_message.notice_id = notice_id
        event_message.end_record()
        event_logger.info(event_message)

    @task
    @event_log(is_loggable=False)
    def normalise_notice_metadata_step(**context_args):
        """

        :return:
        """
        event_logger: EventLogger = get_logger_from_dag_context(context_args)
        event_message = NoticeEventMessage()
        event_message.start_record()

        notice_id = pull_dag_upstream(NOTICE_ID)

        mongodb_client = MongoClient(config.MONGO_DB_AUTH_URL)
        notice_repository = NoticeRepository(mongodb_client=mongodb_client)
        normalised_notice = normalise_notice_by_id(notice_id=notice_id, notice_repository=notice_repository)
        notice_repository.update(notice=normalised_notice)

        handle_event_message_metadata_dag_context(event_message, get_current_context())
        event_message.notice_id = notice_id
        event_message.end_record()
        event_logger.info(event_message)

    index_notice_step() >> normalise_notice_metadata_step()


dag = index_and_normalise_notice_worker()
