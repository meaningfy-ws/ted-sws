import abc
import datetime
import os
from pathlib import Path

from ted_sws.data_manager.adapters.mapping_suite_repository import METADATA_FILE_NAME
from ted_sws.event_manager.adapters.event_handler import EventWriterToFileHandler, EventWriterToConsoleHandler, \
    EventWriterToMongoDBHandler
from ted_sws.event_manager.adapters.event_handler_config import CLILoggerConfig
from ted_sws.event_manager.adapters.event_logger import EventLogger
from ted_sws.event_manager.adapters.log import SeverityLevelType
from ted_sws.event_manager.adapters.logger import LOG_ERROR_TEXT, LOG_SUCCESS_TEXT
from ted_sws.event_manager.model.event_message import EventMessage, EventMessageLogSettings
from ted_sws.event_manager.services.logger_from_context import get_env_logger

DEFAULT_MAPPINGS_PATH = 'mappings'
DEFAULT_OUTPUT_PATH = 'output'


class CmdRunnerABC(abc.ABC):
    @abc.abstractmethod
    def on_begin(self):
        """
        Do before running the command
        :return:
        """

    @abc.abstractmethod
    def run(self):
        """
        Wrapper for running the command
        :return:
        """

    @abc.abstractmethod
    def run_cmd(self):
        """
        Run the command
        :return:
        """

    @abc.abstractmethod
    def on_end(self):
        """
        Do after running the command
        :return:
        """


class CmdRunner(CmdRunnerABC):
    def __init__(self, name=__name__, logger: EventLogger = None):
        self.name = name
        self.begin_time = None
        self.end_time = None

        if logger is None:
            logger = get_env_logger(EventLogger(CLILoggerConfig(name=name)), is_cli=True)

        self.logger = logger

    def get_logger(self) -> EventLogger:
        return self.logger

    @staticmethod
    def _now() -> str:
        return str(datetime.datetime.now())

    def log(self, message: str, severity_level: SeverityLevelType = SeverityLevelType.INFO):
        self.logger.log(severity_level, EventMessage(**{"message": message}),
                        handler_type=EventWriterToConsoleHandler,
                        settings=EventMessageLogSettings(**{"briefly": True}))

        self.logger.log(severity_level,
                        EventMessage(**{"message": message, "caller_name": __name__ + "." + self.name}),
                        handler_type=[EventWriterToFileHandler, EventWriterToMongoDBHandler])

    def log_failed_error(self, error: Exception):
        self.log(LOG_ERROR_TEXT.format("FAILED"))
        self.log(LOG_ERROR_TEXT.format("FAILED" + ' :: ' + type(error).__name__ + ' :: ' + str(error)))

    def log_failed_msg(self, msg: str = None):
        self.log(LOG_ERROR_TEXT.format('FAILED') + (' :: ' + msg if msg is not None else ""))

    def log_success_msg(self, msg: str = None):
        self.log(LOG_SUCCESS_TEXT.format("DONE"))
        self.log(LOG_SUCCESS_TEXT.format('SUCCESS') + (' :: ' + msg if msg is not None else ""))

    def on_begin(self):
        self.begin_time = datetime.datetime.now()
        self.log("CMD :: BEGIN :: {now}".format(now=self._now()))

    def run(self):
        self.on_begin()
        self.run_cmd()
        self.on_end()

    def run_cmd(self):
        pass

    def run_cmd_result(self, error: Exception = None, msg: str = None, errmsg: str = None) -> bool:
        if error:
            self.log_failed_error(error)
            if errmsg is not None:
                self.log_failed_msg(errmsg)
            return False
        else:
            self.log_success_msg(msg)
            return True

    def on_end(self):
        self.end_time = datetime.datetime.now()
        self.log("CMD :: END :: {now} :: [{time}]".format(
            now=str(self.end_time),
            time=self.end_time - self.begin_time
        ))


class CmdRunnerForMappingSuite(CmdRunner):
    repository_path: Path

    def is_mapping_suite(self, suite_id):
        suite_path = self.repository_path / Path(suite_id)
        return os.path.isdir(suite_path) and any(f == METADATA_FILE_NAME for f in os.listdir(suite_path))
