from typing import List
import xml.etree.ElementTree as ET
from io import StringIO

from ted_sws.domain.model.metadata import ExtractedMetadata


def extract_text_from_element(element: ET.Element) -> str:
    """
    Extract text from an element in the XML structure
    :param element:
    :return: str
    """
    if element is not None:
        return element.text


def extract_attribute_from_element(element: ET.Element, attrib_key: str) -> str:
    """
    Extract attribute value from an element in the XML structure
    :param element:
    :param attrib_key:
    :return:
    """
    if element is not None:
        return element.attrib[attrib_key]


def extract_code_and_value_from_element(element: ET.Element) -> EncodedValue:
    """
    Extract code attribute and text values from an element in the XML structure
    :param element:
    :return:
    """
    if element is not None:
        return EncodedValue(code=extract_attribute_from_element(element=element, attrib_key="CODE"),
                            value=extract_text_from_element(element=element))


class XMLManifestationMetadataExtractor:
    """
      Extracting metadata from xml manifestation
    """

    def __init__(self, manifestation_root, namespaces):
        self.manifestation_root = manifestation_root
        self.namespaces = namespaces

    @property
    def title(self):
        title_translations = []
        title_elements = self.manifestation_root.findall(
            self.xpath_registry.xpath_title_elements,
            namespaces=self.namespaces)
        for title in title_elements:
            language = title.find(".").attrib["LG"]
            title_country = LanguageTaggedString(
                text=extract_text_from_element(
                    element=title.find(self.xpath_registry.xpath_title_country, namespaces=self.namespaces)),
                language=language)
            title_city = LanguageTaggedString(
                text=extract_text_from_element(
                    element=title.find(self.xpath_registry.xpath_title_town, namespaces=self.namespaces)),
                language=language)

            title_text = LanguageTaggedString(
                text=extract_text_from_element(element=title.find(self.xpath_registry.xpath_title_text_first,
                                                                  namespaces=self.namespaces)) or extract_text_from_element(
                    element=title.find(self.xpath_registry.xpath_title_text_second, namespaces=self.namespaces)),
                language=language)
            title_translations.append(
                CompositeTitle(title=title_text, title_city=title_city, title_country=title_country))

        return title_translations

    @property
    def notice_publication_number(self):
        return self.manifestation_root.attrib["DOC_ID"]

    @property
    def publication_date(self):
        return extract_text_from_element(element=self.manifestation_root.find(
            self.xpath_registry.xpath_publication_date,
            namespaces=self.namespaces))

    @property
    def ojs_type(self):
        return extract_text_from_element(element=self.manifestation_root.find(
            self.xpath_registry.xpath_ojs_type,
            namespaces=self.namespaces))

    @property
    def ojs_issue_number(self):
        return extract_text_from_element(element=self.manifestation_root.find(
            self.xpath_registry.xpath_ojs_issue_number,
            namespaces=self.namespaces))

    @property
    def city_of_buyer(self):
        return [title.title_city for title in self.title]

    @property
    def name_of_buyer(self):
        buyer_name_elements = self.manifestation_root.findall(
            self.xpath_registry.xpath_name_of_buyer_elements,
            namespaces=self.namespaces)

        return [LanguageTaggedString(text=extract_text_from_element(element=buyer_name.find(".")),
                                     language=extract_attribute_from_element(element=buyer_name.find("."),
                                                                             attrib_key="LG")) for
                buyer_name in buyer_name_elements]

    @property
    def eu_institution(self):
        return self.type_of_buyer.value if self.type_of_buyer.code == "5" else "-"

    @property
    def country_of_buyer(self):
        return extract_attribute_from_element(element=self.manifestation_root.find(
            self.xpath_registry.xpath_country_of_buyer,
            namespaces=self.namespaces), attrib_key="VALUE")

    @property
    def original_language(self):
        return extract_text_from_element(element=self.manifestation_root.find(
            self.xpath_registry.xpath_original_language,
            namespaces=self.namespaces))

    @property
    def document_sent_date(self):
        return extract_text_from_element(element=self.manifestation_root.find(
            self.xpath_registry.xpath_document_sent_date,
            namespaces=self.namespaces))

    @property
    def type_of_buyer(self):
        return extract_code_and_value_from_element(element=self.manifestation_root.find(
            self.xpath_registry.xpath_type_of_buyer,
            namespaces=self.namespaces))

    @property
    def deadline_for_submission(self):
        return extract_text_from_element(element=self.manifestation_root.find(
            self.xpath_registry.xpath_deadline_for_submission,
            namespaces=self.namespaces))

    @property
    def type_of_contract(self):
        return extract_code_and_value_from_element(element=self.manifestation_root.find(
            self.xpath_registry.xpath_type_of_contract,
            namespaces=self.namespaces))

    @property
    def type_of_procedure(self):
        return extract_code_and_value_from_element(element=self.manifestation_root.find(
            self.xpath_registry.xpath_type_of_procedure,
            namespaces=self.namespaces))

    @property
    def notice_type(self):
        return extract_code_and_value_from_element(element=self.manifestation_root.find(
            self.xpath_registry.xpath_notice_type,
            namespaces=self.namespaces))

    @property
    def regulation(self):
        return extract_code_and_value_from_element(element=self.manifestation_root.find(
            self.xpath_registry.xpath_regulation,
            namespaces=self.namespaces))

    @property
    def type_of_bid(self):
        return extract_code_and_value_from_element(element=self.manifestation_root.find(
            self.xpath_registry.xpath_type_of_bid,
            namespaces=self.namespaces))

    @property
    def award_criteria(self):
        return extract_code_and_value_from_element(element=self.manifestation_root.find(
            self.xpath_registry.xpath_award_criteria,
            namespaces=self.namespaces))

    @property
    def common_procurement(self):
        common_procurement_elements = self.manifestation_root.findall(
            self.xpath_registry.xpath_common_procurement_elements,
            namespaces=self.namespaces)
        return [extract_code_and_value_from_element(element=element) for element in common_procurement_elements]

    @property
    def place_of_performance(self):
        place_of_performance_elements = self.manifestation_root.findall(
            self.xpath_registry.xpath_place_of_performance_first,
            namespaces=self.namespaces) or self.manifestation_root.findall(
            self.xpath_registry.xpath_place_of_performance_second,
            namespaces=self.namespaces) or self.manifestation_root.findall(
            self.xpath_registry.xpath_place_of_performance_third,
            namespaces=self.namespaces)

        return [extract_code_and_value_from_element(element=element) for element in place_of_performance_elements]

    @property
    def internet_address(self):
        return extract_text_from_element(element=self.manifestation_root.find(
            self.xpath_registry.xpath_internet_address,
            namespaces=self.namespaces))

    @property
    def legal_basis_directive(self):
        return extract_attribute_from_element(element=self.manifestation_root.find(
            self.xpath_registry.xpath_legal_basis_directive_first,
            namespaces=self.namespaces), attrib_key="VALUE") or extract_attribute_from_element(
            element=self.manifestation_root.find(
                self.xpath_registry.xpath_legal_basis_directive_second,
                namespaces=self.namespaces), attrib_key="VALUE") or extract_text_from_element(
            element=self.manifestation_root.find(
                self.xpath_registry.xpath_legal_basis_directive_third,
                namespaces=self.namespaces))

    def to_metadata(self) -> ExtractedMetadata:
        """
         Creating extracted metadata
        :return:
        """
        metadata = ExtractedMetadata()
        metadata.title = self.title
        metadata.notice_publication_number = self.notice_publication_number
        metadata.publication_date = self.publication_date
        metadata.ojs_issue_number = self.ojs_issue_number
        metadata.city_of_buyer = self.city_of_buyer
        metadata.name_of_buyer = self.name_of_buyer
        metadata.original_language = self.original_language
        metadata.country_of_buyer = self.country_of_buyer
        metadata.type_of_buyer = self.type_of_buyer
        metadata.eu_institution = self.eu_institution
        metadata.document_sent_date = self.document_sent_date
        metadata.type_of_contract = self.type_of_contract
        metadata.type_of_procedure = self.type_of_procedure
        metadata.notice_type = self.notice_type
        metadata.regulation = self.regulation
        metadata.type_of_bid = self.type_of_bid
        metadata.award_criteria = self.award_criteria
        metadata.common_procurement = self.common_procurement
        metadata.place_of_performance = self.place_of_performance
        metadata.internet_address = self.internet_address
        metadata.legal_basis_directive = self.legal_basis_directive
        return metadata
