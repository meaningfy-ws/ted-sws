class XpathRegistry:
    """
        Holds xpath's to the elements necessary to extract metadata from XML manifestation
    """

    @property
    def xpath_title_elements(self):
        return "manifestation_ns:TRANSLATION_SECTION/manifestation_ns:ML_TITLES/"

    @property
    def xpath_title_town(self):
        return "manifestation_ns:TI_TOWN"

    @property
    def xpath_title_country(self):
        return "manifestation_ns:TI_CY"

    @property
    def xpath_title_text_first(self):
        return "manifestation_ns:TI_TEXT/manifestation_ns:P"

    @property
    def xpath_title_text_second(self):
        return "manifestation_ns:TI_TEXT"

    @property
    def xpath_publication_date(self):
        return "manifestation_ns:CODED_DATA_SECTION/manifestation_ns:REF_OJS/manifestation_ns:DATE_PUB"

    @property
    def xpath_ojs_type(self):
        return "manifestation_ns:CODED_DATA_SECTION/manifestation_ns:REF_OJS/manifestation_ns:COLL_OJ"

    @property
    def xpath_ojs_issue_number(self):
        return "manifestation_ns:CODED_DATA_SECTION/manifestation_ns:REF_OJS/manifestation_ns:NO_OJ"

    @property
    def xpath_name_of_buyer_elements(self):
        return "manifestation_ns:TRANSLATION_SECTION/manifestation_ns:ML_AA_NAMES/"

    @property
    def xpath_country_of_buyer(self):
        return "manifestation_ns:CODED_DATA_SECTION/manifestation_ns:NOTICE_DATA/manifestation_ns:ISO_COUNTRY"

    @property
    def xpath_original_language(self):
        return "manifestation_ns:CODED_DATA_SECTION/manifestation_ns:NOTICE_DATA/manifestation_ns:LG_ORIG"

    @property
    def xpath_document_sent_date(self):
        return "manifestation_ns:CODED_DATA_SECTION/manifestation_ns:CODIF_DATA/manifestation_ns:DS_DATE_DISPATCH"

    @property
    def xpath_type_of_buyer(self):
        return "manifestation_ns:CODED_DATA_SECTION/manifestation_ns:CODIF_DATA/manifestation_ns:AA_AUTHORITY_TYPE"

    @property
    def xpath_deadline_for_submission(self):
        return "manifestation_ns:CODED_DATA_SECTION/manifestation_ns:CODIF_DATA/manifestation_ns:DT_DATE_FOR_SUBMISSION"

    @property
    def xpath_type_of_contract(self):
        return "manifestation_ns:CODED_DATA_SECTION/manifestation_ns:CODIF_DATA/manifestation_ns:NC_CONTRACT_NATURE"

    @property
    def xpath_type_of_procedure(self):
        return "manifestation_ns:CODED_DATA_SECTION/manifestation_ns:CODIF_DATA/manifestation_ns:PR_PROC"

    @property
    def xpath_notice_type(self):
        return "manifestation_ns:CODED_DATA_SECTION/manifestation_ns:CODIF_DATA/manifestation_ns:TD_DOCUMENT_TYPE"

    @property
    def xpath_regulation(self):
        return "manifestation_ns:CODED_DATA_SECTION/manifestation_ns:CODIF_DATA/manifestation_ns:RP_REGULATION"

    @property
    def xpath_type_of_bid(self):
        return "manifestation_ns:CODED_DATA_SECTION/manifestation_ns:CODIF_DATA/manifestation_ns:TY_TYPE_BID"

    @property
    def xpath_award_criteria(self):
        return "manifestation_ns:CODED_DATA_SECTION/manifestation_ns:CODIF_DATA/manifestation_ns:AC_AWARD_CRIT"

    @property
    def xpath_common_procurement_elements(self):
        return "manifestation_ns:CODED_DATA_SECTION/manifestation_ns:NOTICE_DATA/manifestation_ns:ORIGINAL_CPV"

    @property
    def xpath_place_of_performance_first(self):
        return "manifestation_ns:CODED_DATA_SECTION/manifestation_ns:NOTICE_DATA/manifestation_ns:PERFORMANCE_NUTS"
    
    @property
    def xpath_place_of_performance_second(self):
        return "manifestation_ns:CODED_DATA_SECTION/manifestation_ns:NOTICE_DATA/nuts:PERFORMANCE_NUTS"
    
    @property
    def xpath_place_of_performance_third(self):
        return "manifestation_ns:CODED_DATA_SECTION/manifestation_ns:NOTICE_DATA/manifestation_ns:ORIGINAL_NUTS"

    @property
    def xpath_internet_address(self):
        return "manifestation_ns:CODED_DATA_SECTION/manifestation_ns:NOTICE_DATA/manifestation_ns:IA_URL_GENERAL"

    @property
    def xpath_legal_basis_directive_first(self):
        return "manifestation_ns:CODED_DATA_SECTION/manifestation_ns:CODIF_DATA/manifestation_ns:DIRECTIVE"
    
    @property
    def xpath_legal_basis_directive_second(self):
        return "manifestation_ns:FORM_SECTION/*/manifestation_ns:LEGAL_BASIS"
    
    @property
    def xpath_legal_basis_directive_third(self):
        return "manifestation_ns:FORM_SECTION/*/manifestation_ns:LEGAL_BASIS_OTHER/manifestation_ns:P/manifestation_ns:FT"

    @property
    def xpath_form_number(self):
        return "manifestation_ns:FORM_SECTION/*[1]"