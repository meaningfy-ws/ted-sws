import pandas as pd

from ted_sws.core.model.notice import NoticeStatus
from ted_sws.data_manager.adapters.mapping_suite_repository import MappingSuiteRepositoryInFileSystem
from ted_sws.metadata_normaliser.services.metadata_normalizer import MetadataNormaliser
from ted_sws.notice_eligibility.services.notice_eligibility import create_eligibility_df, check_package, \
    notice_eligibility_checker, notice_eligibility_checker_by_id


def test_non_eligibility_by_notice(file_system_repository_path, raw_notice):
    mapping_suite_repository = MappingSuiteRepositoryInFileSystem(repository_path=file_system_repository_path)
    MetadataNormaliser(notice=raw_notice).normalise_metadata()
    notice_eligibility_checker(notice=raw_notice, mapping_suite_repository=mapping_suite_repository)
    assert raw_notice.status == NoticeStatus.INELIGIBLE_FOR_TRANSFORMATION


def test_eligibility_by_notice(file_system_repository_path, notice_2020):
    mapping_suite_repository = MappingSuiteRepositoryInFileSystem(repository_path=file_system_repository_path)
    MetadataNormaliser(notice=notice_2020).normalise_metadata()
    notice_checker = notice_eligibility_checker(notice=notice_2020, mapping_suite_repository=mapping_suite_repository)
    notice_id, mapping_suite_identifier = notice_checker
    assert notice_id == "408313-2020"
    assert mapping_suite_identifier == "test_package2"
    assert notice_2020.status == NoticeStatus.ELIGIBLE_FOR_TRANSFORMATION


def test_eligibility_by_notice_id(file_system_repository_path, notice_2020, notice_repository):
    MetadataNormaliser(notice=notice_2020).normalise_metadata()
    notice_repository.add(notice_2020)
    mapping_suite_repository = MappingSuiteRepositoryInFileSystem(repository_path=file_system_repository_path)
    notice_checker = notice_eligibility_checker_by_id(notice_id="408313-2020",
                                                      mapping_suite_repository=mapping_suite_repository,
                                                      notice_repository=notice_repository)
    notice_id, mapping_suite_identifier = notice_checker

    assert notice_id == "408313-2020"
    assert mapping_suite_identifier == "test_package2"
    assert notice_2020.status == NoticeStatus.ELIGIBLE_FOR_TRANSFORMATION


def test_create_eligibility_df(file_system_repository_path):
    mapping_suite_repository = MappingSuiteRepositoryInFileSystem(repository_path=file_system_repository_path)
    mapping_suite = mapping_suite_repository.get("test_package")
    eligibility_df = create_eligibility_df(metadata_constraint=mapping_suite.metadata_constraints)
    assert isinstance(eligibility_df, pd.DataFrame)
    assert len(eligibility_df.index) == 9
    assert "form_number" in eligibility_df.columns
    assert "legal_basis" in eligibility_df.columns
    assert "year" in eligibility_df.columns


def test_check_mapping_suite(file_system_repository_path, normalised_metadata_object):
    mapping_suite_repository = MappingSuiteRepositoryInFileSystem(repository_path=file_system_repository_path)
    is_valid = check_package(mapping_suite=mapping_suite_repository.get("test_package"),
                             notice_metadata=normalised_metadata_object)
    assert isinstance(is_valid, bool)
    assert is_valid
    normalised_metadata_object.legal_basis_directive = "http://publications.europa.eu/resource/authority/legal-basis/32009L0081"
    is_valid = check_package(mapping_suite=mapping_suite_repository.get("test_package"),
                             notice_metadata=normalised_metadata_object)
    assert not is_valid
