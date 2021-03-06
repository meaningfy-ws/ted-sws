from datetime import datetime, timezone
from typing import Optional, List, Union, Any, Dict

from ted_sws.core.model import PropertyBaseModel
from ted_sws.event_manager.adapters.log import LoggedBy
from ted_sws.event_manager.adapters.logger import Logger, logger as root_logger

MESSAGE_TYPE = Union[List[str], str]
DICT_TYPE = Union[Dict[str, Any], None]

EOL = "\n"


class Message(PropertyBaseModel):
    title: Optional[str] = None
    message: Optional[MESSAGE_TYPE] = None

    class Config:
        arbitrary_types_allowed = True
        use_enum_values = True


class Log(Message):
    name: str = __name__
    level: int = None
    logger: Logger = root_logger


class DBProcessLogRequest(PropertyBaseModel):
    POSITIONAL_OR_KEYWORD: DICT_TYPE = {}
    VAR_POSITIONAL: DICT_TYPE = {}
    VAR_KEYWORD: DICT_TYPE = {}


class DBProcessLogResponse(PropertyBaseModel):
    RESULT: Optional[str]


class DBProcessLog(Message):
    created_at: datetime = datetime.now(timezone.utc)
    year: datetime = datetime.now(timezone.utc).year
    month: datetime = datetime.now(timezone.utc).month
    day: datetime = datetime.now(timezone.utc).day
    path: Optional[str] = None
    name: Optional[str] = None
    request: Optional[Union[DBProcessLogRequest, DICT_TYPE]] = None
    started_at: datetime = datetime.now(timezone.utc)
    duration: Optional[int] = None
    ended_at: Optional[datetime] = None
    response: Optional[DBProcessLogResponse] = None
    logs: Optional[str] = None
    logged_by: Optional[LoggedBy] = None
