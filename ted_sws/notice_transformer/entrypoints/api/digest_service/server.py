import logging
import subprocess

import click

from ted_sws import config
from ted_sws.event_manager.adapters.logger import Logger, LOG_INFO_LEVEL
from ted_sws.event_manager.model.message_bus import message_bus
from ted_sws.event_manager.model.message import Log
from ted_sws.notice_transformer.entrypoints.api.digest_service.main import API_PREFIX

API_HOST: str = config.ID_MANAGER_API_HOST
API_PORT: int = config.ID_MANAGER_API_PORT


@click.command()
@click.option('-h', '--host', default=API_HOST)
@click.option('-p', '--port', default=API_PORT, type=int)
def api_server_start(host, port):
    logger = Logger(name="ID_MANAGER_API_SERVER", level=LOG_INFO_LEVEL)
    logger.add_console_handler(formatter=logging.Formatter(
        "[%(asctime)s] - %(name)s - %(levelname)s:\n%(message)s",
        "%Y-%m-%d %H:%M:%S"
    ))
    bash_script = f"uvicorn --host {host} --port {port} ted_sws.id_manager.entrypoints.api.main:app --reload"
    message_bus.handle(Log(
        message=f"{bash_script}\n###\nSee http://{host}:{port}{API_PREFIX}/docs for API usage.\n###",
        logger=logger)
    )
    subprocess.run(bash_script, shell=True, capture_output=True)
