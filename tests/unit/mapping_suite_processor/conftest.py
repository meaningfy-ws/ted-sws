import mongomock
import pymongo
import pytest

from tests import TEST_DATA_PATH


@pytest.fixture
def file_system_repository_path():
    return TEST_DATA_PATH / "notice_transformer" / "mapping_suite_processor_repository"

@pytest.fixture
@mongomock.patch(servers=(('server.example.com', 27017),))
def mongodb_client():
    return pymongo.MongoClient('server.example.com')