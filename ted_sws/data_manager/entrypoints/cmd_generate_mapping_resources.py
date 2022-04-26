import json
import os
from pathlib import Path

import click

from ted_sws.core.adapters.cmd_runner import CmdRunner as BaseCmdRunner, DEFAULT_MAPPINGS_PATH
from ted_sws.core.adapters.sparql_triple_store import SPARQLTripleStore, TripleStoreABC
from ted_sws.resources import QUERIES_PATH, MAPPING_FILES_PATH
from ted_sws.core.adapters.logger import LOG_INFO_TEXT

DEFAULT_OUTPUT_PATH = '{mappings_path}/{mapping_suite_id}/transformation/resources'
CMD_NAME = "NORMALISATION_RESOURCE_GENERATOR"

"""
USAGE:
# normalisation_resource_generator --help
"""


class CmdRunner(BaseCmdRunner):
    """
    Keeps the logic to be used by Resources Generator CMD
    """

    def __init__(
            self,
            queries_folder,
            output_folder,
            triple_store: TripleStoreABC = SPARQLTripleStore()
    ):
        super().__init__(name=CMD_NAME)
        self.queries_folder_path = Path(os.path.realpath(queries_folder))
        self.output_folder_path = Path(os.path.realpath(output_folder))
        self.triple_store = triple_store

    def run_cmd(self):
        error = None
        try:
            query_files_paths = list(self.queries_folder_path.rglob("*.rq"))

            for query_file_path in query_files_paths:
                json_file_name = query_file_path.stem + ".json"
                path = self.output_folder_path / json_file_name
                json_content = self.triple_store.with_query_from_file(
                    sparql_query_file_path=str(query_file_path)).fetch_tree()
                with open(path, 'w') as outfile:
                    json.dump(json_content, outfile)
                self.log("Generated resource :: " + LOG_INFO_TEXT.format(json_file_name))
        except Exception as e:
            error = e

        return self.run_cmd_result(error)


def run(mapping_suite_id=None,
        opt_queries_folder: str = str(QUERIES_PATH),
        opt_output_folder: str = str(MAPPING_FILES_PATH),
        opt_mappings_path: str = DEFAULT_MAPPINGS_PATH,
        triple_store: TripleStoreABC = SPARQLTripleStore()):
    """
    This method will generate a json file for each ran SPARQL query in the resources folder
    :param mapping_suite_id:
    :param triple_store:
    :param opt_queries_folder:
    :param opt_output_folder:
    :param opt_mappings_path:
    :return:
    """
    queries_folder = opt_queries_folder

    if opt_output_folder and not mapping_suite_id:
        output_folder = opt_output_folder
    else:
        output_folder = DEFAULT_OUTPUT_PATH.format(
            mappings_path=opt_mappings_path,
            mapping_suite_id=mapping_suite_id
        )

    cmd = CmdRunner(
        queries_folder=queries_folder,
        output_folder=output_folder,
        triple_store=triple_store
    )
    cmd.run()


@click.command()
@click.argument('mapping-suite-id', nargs=1, required=False)
@click.option('--opt-queries-folder', default=str(QUERIES_PATH))
@click.option('--opt-output-folder', default=str(MAPPING_FILES_PATH))
@click.option('-m', '--opt-mappings-path', default=DEFAULT_MAPPINGS_PATH)
def main(mapping_suite_id, opt_queries_folder, opt_output_folder, opt_mappings_path):
    run(mapping_suite_id, opt_queries_folder, opt_output_folder, opt_mappings_path, SPARQLTripleStore())


if __name__ == '__main__':
    main()
