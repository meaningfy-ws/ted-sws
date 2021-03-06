#!/usr/bin/python3

# __init__.py
# Date:  29/01/2022
# Author: Eugeniu Costetchi
# Email: costezki.eugen@gmail.com

""" """

import pytest

from ted_sws.core.model.notice import Notice, NoticeStatus, UnsupportedStatusTransition


def test_illegal_status_transitions(indexed_notice):
    """
        Test a few illegal downstream transitions.
    :param raw_notice:
    :return:
    """

    with pytest.raises(UnsupportedStatusTransition):
        indexed_notice.update_status_to(NoticeStatus.TRANSFORMED)

    with pytest.raises(UnsupportedStatusTransition):
        indexed_notice.update_status_to(NoticeStatus.PACKAGED)

    with pytest.raises(UnsupportedStatusTransition):
        indexed_notice.update_status_to(NoticeStatus.VALIDATED)

    with pytest.raises(UnsupportedStatusTransition):
        indexed_notice.update_status_to(NoticeStatus.PUBLISHED)

    with pytest.raises(UnsupportedStatusTransition):
        indexed_notice.update_status_to(NoticeStatus.PUBLICLY_AVAILABLE)


def test_notice_status_upstream_transition(indexed_notice):
    """
        Downstream transitions constraints checked.

    :param raw_notice:
    :return:
    """
    indexed_notice.update_status_to(NoticeStatus.INDEXED)
    indexed_notice.update_status_to(NoticeStatus.NORMALISED_METADATA)
    indexed_notice.update_status_to(NoticeStatus.INELIGIBLE_FOR_TRANSFORMATION)
    indexed_notice.update_status_to(NoticeStatus.ELIGIBLE_FOR_TRANSFORMATION)
    indexed_notice.update_status_to(NoticeStatus.PREPROCESSED_FOR_TRANSFORMATION)
    indexed_notice.update_status_to(NoticeStatus.TRANSFORMED)
    indexed_notice.update_status_to(NoticeStatus.DISTILLED)
    indexed_notice.update_status_to(NoticeStatus.VALIDATED)
    indexed_notice.update_status_to(NoticeStatus.INELIGIBLE_FOR_PACKAGING)
    indexed_notice.update_status_to(NoticeStatus.ELIGIBLE_FOR_PACKAGING)
    indexed_notice.update_status_to(NoticeStatus.PACKAGED)
    indexed_notice.update_status_to(NoticeStatus.INELIGIBLE_FOR_PUBLISHING)
    indexed_notice.update_status_to(NoticeStatus.ELIGIBLE_FOR_PUBLISHING)
    indexed_notice.update_status_to(NoticeStatus.PUBLISHED)
    indexed_notice.update_status_to(NoticeStatus.PUBLICLY_UNAVAILABLE)
    indexed_notice.update_status_to(NoticeStatus.PUBLICLY_AVAILABLE)


def test_notice_status_transition_below_packaged(publicly_available_notice):
    """
        Notice status transition below PACKAGING should remove the METS manifestation
    :param publicly_available_notice:
    :return:
    """
    publicly_available_notice.update_status_to(NoticeStatus.ELIGIBLE_FOR_PACKAGING)
    assert publicly_available_notice.mets_manifestation is None
    assert publicly_available_notice.rdf_manifestation is not None
    assert publicly_available_notice.normalised_metadata is not None
    assert publicly_available_notice.xml_manifestation is not None
    assert publicly_available_notice.original_metadata is not None
    assert publicly_available_notice.distilled_rdf_manifestation is not None
    assert publicly_available_notice.preprocessed_xml_manifestation is not None


def test_notice_status_transition_below_transformed(publicly_available_notice):
    """
        Notice status transition below TRANSFORMED should remove the RDF and METS manifestations.
    :param publicly_available_notice:
    :return:
    """
    publicly_available_notice.update_status_to(NoticeStatus.ELIGIBLE_FOR_TRANSFORMATION)
    assert publicly_available_notice.mets_manifestation is None
    assert publicly_available_notice.rdf_manifestation is None
    assert publicly_available_notice.normalised_metadata is not None
    assert publicly_available_notice.xml_manifestation is not None
    assert publicly_available_notice.original_metadata is not None


def test_notice_status_transition_below_normalised_metadata(publicly_available_notice):
    """
    Notice status transition below TRANSFORMED should remove the normalised metadata and the RDF and METS
    manifestations. :param publicly_available_notice: :return:
    """
    publicly_available_notice.update_status_to(NoticeStatus.RAW)
    assert publicly_available_notice.mets_manifestation is None
    assert publicly_available_notice.rdf_manifestation is None
    assert publicly_available_notice.normalised_metadata is None
    assert publicly_available_notice.xml_manifestation is not None
    assert publicly_available_notice.original_metadata is not None


def test_notice_status_transition_check_preprocessed_and_distilled_state(indexed_notice, publicly_available_notice):
    """
    
    :param raw_notice:
    :param publicly_available_notice:
    :return:
    """
    assert indexed_notice.status == NoticeStatus.INDEXED
    indexed_notice._status = NoticeStatus.ELIGIBLE_FOR_TRANSFORMATION
    indexed_notice.set_preprocessed_xml_manifestation(
        preprocessed_xml_manifestation=publicly_available_notice.preprocessed_xml_manifestation)
    assert indexed_notice.status == NoticeStatus.PREPROCESSED_FOR_TRANSFORMATION
    indexed_notice.set_preprocessed_xml_manifestation(
        preprocessed_xml_manifestation=publicly_available_notice.preprocessed_xml_manifestation)
    indexed_notice.update_status_to(NoticeStatus.TRANSFORMED)
    indexed_notice.set_distilled_rdf_manifestation(
        distilled_rdf_manifestation=publicly_available_notice.distilled_rdf_manifestation)
    assert indexed_notice.status == NoticeStatus.DISTILLED
    indexed_notice.set_distilled_rdf_manifestation(
        distilled_rdf_manifestation=publicly_available_notice.distilled_rdf_manifestation)


def test_notice_status_conversion_from_string():
    assert NoticeStatus["RAW"] == NoticeStatus.RAW
