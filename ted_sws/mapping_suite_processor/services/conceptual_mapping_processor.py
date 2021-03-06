import pathlib
import tempfile

from pymongo import MongoClient

from ted_sws import config
from ted_sws.core.model.manifestation import XMLManifestation
from ted_sws.core.model.notice import Notice
from ted_sws.data_manager.adapters.mapping_suite_repository import MappingSuiteRepositoryInFileSystem, \
    MappingSuiteRepositoryMongoDB
from ted_sws.data_manager.adapters.notice_repository import NoticeRepository
from ted_sws.mapping_suite_processor.adapters.github_package_downloader import GitHubMappingSuitePackageDownloader

CONCEPTUAL_MAPPINGS_FILE_NAME = "conceptual_mappings.xlsx"
CONCEPTUAL_MAPPINGS_ASSERTIONS = "cm_assertions"
SHACL_SHAPE_INJECTION_FOLDER = "ap_data_shape"
SHACL_SHAPE_RESOURCES_FOLDER = "shacl_shapes"
SHACL_SHAPE_FILE_NAME = "ePO_shacl_shapes.rdf"
MAPPING_FILES_RESOURCES_FOLDER = "mapping_files"
SPARQL_QUERIES_RESOURCES_FOLDER = "queries"
SPARQL_QUERIES_INJECTION_FOLDER = "business_queries"
PROD_ARCHIVE_SUFFIX = "prod"
DEMO_ARCHIVE_SUFFIX = "demo"


def mapping_suite_processor_load_package_in_mongo_db(mapping_suite_package_path: pathlib.Path,
                                                     mongodb_client: MongoClient,
                                                     load_test_data: bool = False,
                                                     git_last_commit_hash: str = None
                                                     ):
    """
        This feature allows you to upload a mapping suite package to MongoDB.
    :param mapping_suite_package_path:
    :param mongodb_client:
    :param load_test_data:
    :param git_last_commit_hash:
    :return:
    """
    mapping_suite_repository_path = mapping_suite_package_path.parent
    mapping_suite_package_name = mapping_suite_package_path.name
    mapping_suite_repository_in_file_system = MappingSuiteRepositoryInFileSystem(
        repository_path=mapping_suite_repository_path)
    mapping_suite_in_memory = mapping_suite_repository_in_file_system.get(reference=mapping_suite_package_name)

    if git_last_commit_hash is not None:
        mapping_suite_in_memory.git_latest_commit_hash = git_last_commit_hash

    if load_test_data:
        tests_data = mapping_suite_in_memory.transformation_test_data.test_data
        notice_repository = NoticeRepository(mongodb_client=mongodb_client)
        for test_data in tests_data:
            notice_repository.add(notice=Notice(ted_id=test_data.file_name.split(".")[0],
                                                xml_manifestation=XMLManifestation(object_data=test_data.file_content)))

    mapping_suite_repository_mongo_db = MappingSuiteRepositoryMongoDB(mongodb_client=mongodb_client)
    mapping_suite_repository_mongo_db.add(mapping_suite=mapping_suite_in_memory)


def mapping_suite_processor_from_github_expand_and_load_package_in_mongo_db(mapping_suite_package_name: str,
                                                                            mongodb_client: MongoClient,
                                                                            load_test_data: bool = False
                                                                            ):
    """
        This feature is intended to download a mapping_suite_package from GitHub and process it for upload to MongoDB.
    :param mapping_suite_package_name:
    :param mongodb_client:
    :param load_test_data:
    :return:
    """
    default_github_repository_url = "https://github.com/meaningfy-ws/ted-sws-artefacts.git"
    mapping_suite_package_downloader = GitHubMappingSuitePackageDownloader(
        github_repository_url=config.GITHUB_TED_SWS_ARTEFACTS_URL or default_github_repository_url)
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_dir_path = pathlib.Path(tmp_dir)
        git_last_commit_hash = mapping_suite_package_downloader.download(
            mapping_suite_package_name=mapping_suite_package_name,
            output_mapping_suite_package_path=tmp_dir_path)
        mapping_suite_package_path = tmp_dir_path / mapping_suite_package_name
        mapping_suite_processor_load_package_in_mongo_db(mapping_suite_package_path=mapping_suite_package_path,
                                                         mongodb_client=mongodb_client,
                                                         load_test_data=load_test_data,
                                                         git_last_commit_hash=git_last_commit_hash
                                                         )
