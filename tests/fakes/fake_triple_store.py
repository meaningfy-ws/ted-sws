import pandas as pd

from ted_sws.data_manager.adapters.sparql_endpoint import TripleStoreEndpointABC


class FakeTripleStoreEndpoint(TripleStoreEndpointABC):
    def with_query(self, sparql_query: str, substitution_variables: dict = None,
                   sparql_prefixes: str = "") -> 'TripleStoreEndpointABC':
        return self

    def with_query_from_file(self, sparql_query_file_path: str, substitution_variables: dict = None,
                             prefixes: str = "") -> 'TripleStoreEndpointABC':
        return self

    def fetch_tabular(self) -> pd.DataFrame:
        return pd.DataFrame()

    def fetch_tree(self) -> dict:
        return {"results": "awesome results"}
