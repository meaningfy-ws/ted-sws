import pytest

from ted_sws.core.model.notice import NoticeStatus
from ted_sws.metadata_normaliser.resources.mapping_files_registry import MappingFilesRegistry
from ted_sws.metadata_normaliser.services.metadata_normalizer import normalise_notice, normalise_notice_by_id, \
    MetadataNormaliser, ExtractedMetadataNormaliser
from ted_sws.core.service.metadata_constraints import filter_df_by_variables
from ted_sws.metadata_normaliser.services.xml_manifestation_metadata_extractor import XMLManifestationMetadataExtractor


def test_metadata_normaliser_by_notice(raw_notice):
    notice = normalise_notice(raw_notice)
    assert notice.normalised_metadata
    assert notice.normalised_metadata.title
    assert notice.status == NoticeStatus.NORMALISED_METADATA


def test_metadata_normaliser_by_notice_id(notice_id, notice_repository, notice_2018):
    notice_repository.add(notice_2018)
    with pytest.raises(AttributeError):
        notice = normalise_notice_by_id(notice_id=notice_2018.ted_id, notice_repository=notice_repository)
        assert notice.normalised_metadata
        assert notice.normalised_metadata.title
        assert notice.status == NoticeStatus.NORMALISED_METADATA


def test_metadata_normaliser_by_wrong_notice_id(notice_repository):
    notice_id = "wrong-notice-id"
    with pytest.raises(ValueError):
        normalise_notice_by_id(notice_id=notice_id, notice_repository=notice_repository)


def test_metadata_normaliser(raw_notice):
    notice = raw_notice
    MetadataNormaliser(notice=notice).normalise_metadata()

    assert notice.normalised_metadata
    assert notice.normalised_metadata.title
    assert notice.status == NoticeStatus.NORMALISED_METADATA


def test_normalise_form_number(raw_notice):
    extracted_metadata = XMLManifestationMetadataExtractor(xml_manifestation=raw_notice.xml_manifestation).to_metadata()
    extracted_metadata_normaliser = ExtractedMetadataNormaliser(extracted_metadata=extracted_metadata)
    assert "18" == extracted_metadata.extracted_form_number
    assert "F18" == extracted_metadata_normaliser.normalise_form_number(value=extracted_metadata.extracted_form_number)


def test_normalise_legal_basis(raw_notice):
    extracted_metadata = XMLManifestationMetadataExtractor(xml_manifestation=raw_notice.xml_manifestation).to_metadata()
    extracted_metadata_normaliser = ExtractedMetadataNormaliser(extracted_metadata=extracted_metadata)
    assert "2009/81/EC" == extracted_metadata.legal_basis_directive
    assert "32009L0081" == extracted_metadata_normaliser.normalise_legal_basis_value(
        value=extracted_metadata.legal_basis_directive)


def test_get_map_value(raw_notice):
    extracted_metadata = XMLManifestationMetadataExtractor(xml_manifestation=raw_notice.xml_manifestation).to_metadata()
    extracted_metadata_normaliser = ExtractedMetadataNormaliser(extracted_metadata=extracted_metadata)
    value = extracted_metadata_normaliser.get_map_value(mapping=MappingFilesRegistry().countries, value="DE")
    assert value == "http://publications.europa.eu/resource/authority/country/DEU"


def test_filter_df_by_variables():
    df = MappingFilesRegistry().ef_notice_df
    filtered_df = filter_df_by_variables(df=df, form_type="planning",
                                         eform_notice_type="pin-only")

    assert len(filtered_df.index) == 3
    assert "32014L0024" in filtered_df["eform_legal_basis"].values


def test_get_form_type_and_notice_type(raw_notice):
    extracted_metadata = XMLManifestationMetadataExtractor(xml_manifestation=raw_notice.xml_manifestation).to_metadata()
    extracted_metadata_normaliser = ExtractedMetadataNormaliser(extracted_metadata=extracted_metadata)
    form_type, notice_type = extracted_metadata_normaliser.get_form_type_and_notice_type(
        ef_map=MappingFilesRegistry().ef_notice_df,
        sf_map=MappingFilesRegistry().sf_notice_df,
        form_number="F02", extracted_notice_type=None,
        legal_basis="32014L0023", document_type_code="Y")

    assert "competition" == form_type
    assert "cn-standard" == notice_type
