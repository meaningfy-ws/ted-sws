import os
from pathlib import Path

import logging
from ted_sws.event_manager.adapters.logger import Logger
from ted_sws.notice_transformer.entrypoints.cli.cmd_mapping_runner import run as cli_run

TEST_LOGGER = Logger(name="TEST_MAPPING_RUNNER", level=logging.INFO)
TEST_LOGGER.get_logger().propagate = True


def post_process(fake_repository_path, fake_mapping_suite_id):
    output_dir_path = fake_repository_path / fake_mapping_suite_id / "output"
    for r in os.listdir(output_dir_path):
        output_notice_dir_path = output_dir_path / r
        output_notice_path = output_notice_dir_path / "notice.ttl"
        assert os.path.isdir(output_notice_dir_path)
        assert os.path.isfile(output_notice_path)
        os.remove(output_notice_path)
        os.rmdir(output_notice_dir_path)


def test_cmd_mapping_runner(caplog, fake_rml_mapper, fake_mapping_suite_id, fake_repository_path):
    cli_run(
        mapping_suite_id=fake_mapping_suite_id,
        opt_mappings_folder=fake_repository_path,
        rml_mapper=fake_rml_mapper,
        logger=TEST_LOGGER
    )
    assert fake_mapping_suite_id in caplog.text
    assert "SUCCESS" in caplog.text
    post_process(fake_repository_path, fake_mapping_suite_id)


def test_cmd_mapping_runner_with_invalid_serialization(caplog, fake_rml_mapper, fake_mapping_suite_id,
                                                       fake_repository_path):
    cli_run(
        mapping_suite_id=fake_mapping_suite_id,
        serialization_format="invalid-turtle",
        opt_mappings_folder=fake_repository_path,
        rml_mapper=fake_rml_mapper,
        logger=TEST_LOGGER
    )
    assert "No such serialization format" in caplog.text

    cli_run(
        opt_mapping_suite_id=fake_mapping_suite_id,
        opt_mappings_folder=fake_repository_path,
        opt_serialization_format="invalid-turtle",
        rml_mapper=fake_rml_mapper,
        logger=TEST_LOGGER
    )
    assert "No such serialization format" in caplog.text


def test_cmd_mapping_runner_with_not_package(caplog, fake_rml_mapper, fake_not_mapping_suite_id,
                                             fake_fail_repository_path):
    cli_run(
        mapping_suite_id=fake_not_mapping_suite_id,
        opt_mappings_folder=fake_fail_repository_path,
        rml_mapper=fake_rml_mapper,
        logger=TEST_LOGGER
    )
    assert "FAILED" in caplog.text
    assert "Not a MappingSuite" in caplog.text


def test_cmd_mapping_runner_with_failed_package(caplog, fake_rml_mapper, fake_failed_mapping_suite_id,
                                                fake_fail_repository_path):
    cli_run(
        mapping_suite_id=fake_failed_mapping_suite_id,
        opt_mappings_folder=fake_fail_repository_path,
        rml_mapper=fake_rml_mapper,
        logger=TEST_LOGGER
    )
    assert "FAILED" in caplog.text


def test_cmd_mapping_runner_with_no_suite_id(caplog, fake_rml_mapper, fake_repository_path):
    cli_run(
        opt_mappings_folder=fake_repository_path,
        rml_mapper=fake_rml_mapper,
        logger=TEST_LOGGER
    )
    assert "SUCCESS" in caplog.text

    fs_repository_path = Path(os.path.realpath(fake_repository_path))
    for suite_id in os.listdir(fs_repository_path):
        post_process(fake_repository_path, suite_id)
