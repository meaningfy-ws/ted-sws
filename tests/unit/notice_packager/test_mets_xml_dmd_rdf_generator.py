from . import helper
from ted_sws.notice_packager.adapters import mets_xml_dmd_rdf_generator as tpl_generator

TEST_TPL = "196390_2016-0.mets.xml.dmd.rdf"


def test_tpl_generator():
    data = {
        "notice": {
            "id": "196390_2016",
            "lang": ["en"]
        },
        "work": {
            "do_not_index": "true",
            "work_date_document": "2021-08-01",
            "work_created_by_agent": "PUBL",
            "work_dataset_published_by_agent": "PUBL",
            "datetime_transmission": "2021-08-01T00:01:00",
            "work_title": {
                "en": "eProcurement notice 196390_2016"
            },
            "work_date_creation": "2016-01-01",
            "work_id": "http://data.europa.eu/a4g/resource/2016/196390_2016",
            "work_dataset_version": "20160101-0",
            "work_dataset_keyword": [
                "eProcurement",
                "notice"
            ],
            "work_dataset_has_frequency_publication_frequency": "OTHER"
        },
        "expression": {
            "expression_title": {
                "en": "eProcurement notice 196390_2016"
            },
            "expression_uses_language": "ENG"
        },
        "manifestation": {
            "manifestation_distribution_tpl": "196390_2016_rdf",
            "manifestation_type": "E_PROCUREMENT_ONTOLOGY",
            "manifestation_date_publication": "2021-08-01",
            "manifestation_distribution_has_status_distribution_status": "COMPLETED",
            "manifestation_distribution_has_media_type_concept_media_type": "RDF"
        }
    }

    helper.test(tpl_generator, data, TEST_TPL)





