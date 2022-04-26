#!/usr/bin/python3

import os
from pathlib import Path
from typing import Tuple, List

import click

from ted_sws.core.adapters.cmd_runner import CmdRunner as BaseCmdRunner, DEFAULT_MAPPINGS_PATH
from ted_sws.core.adapters.logger import LOG_INFO_TEXT, LOG_WARN_TEXT
from ted_sws.data_manager.entrypoints import cmd_generate_mapping_resources
from ted_sws.mapping_suite_processor.entrypoints import cmd_yarrrml2rml_converter, cmd_sparql_generator, \
    cmd_metadata_generator
from ted_sws.notice_transformer.entrypoints import cmd_mapping_suite_transformer

DEFAULT_COMMANDS: Tuple = (
    'normalisation_resource_generator',
    'metadata_generator',
    'yarrrml2rml_converter',
    'sparql_generator',
    'transformer'
)
CMD_NAME = "CMD_MAPPING_SUITE_PROCESSOR"

"""
USAGE:
# mapping_suite_processor --help
"""


class CmdRunner(BaseCmdRunner):
    """
    Keeps the logic to be used by Mapping Suite Processor
    """

    def __init__(
            self,
            mapping_suite_id,
            mappings_path,
            commands: List[str]
    ):
        super().__init__(name=CMD_NAME)
        self.mapping_suite_id = mapping_suite_id
        self.mappings_path = mappings_path
        self.commands = commands
        print("K :: ", commands, type(commands))

        mapping_suite_path = Path(os.path.realpath(mappings_path)) / Path(mapping_suite_id)
        if not mapping_suite_path.is_dir():
            error_msg = f"No such MappingSuite[{mapping_suite_id}]"
            self.log_failed_msg(error_msg)
            raise FileNotFoundError(error_msg)

    def _cmd(self, cmd: str):
        if cmd == 'cmd_generate_mapping_resources':
            cmd_generate_mapping_resources.run(
                mapping_suite_id=self.mapping_suite_id,
                opt_mappings_path=self.mappings_path
            )
        elif cmd == 'cmd_metadata_generator':
            cmd_metadata_generator.run(
                mapping_suite_id=self.mapping_suite_id,
                opt_mappings_path=self.mappings_path
            )
        elif cmd == 'cmd_yarrrml2rml_converter':
            cmd_yarrrml2rml_converter.run(
                mapping_suite_id=self.mapping_suite_id,
                opt_mappings_path=self.mappings_path
            )
        elif cmd == 'cmd_sparql_generator':
            cmd_sparql_generator.run(
                mapping_suite_id=self.mapping_suite_id,
                opt_mappings_path=self.mappings_path
            )
        elif cmd == 'cmd_mapping_suite_transformer':
            cmd_mapping_suite_transformer.run(
                mapping_suite_id=self.mapping_suite_id,
                opt_mappings_path=self.mappings_path
            )

    def run_cmd(self):
        self.log("Running " + LOG_INFO_TEXT.format(f"MappingSuite[{self.mapping_suite_id}]") + " processing ... ")
        self.log(LOG_WARN_TEXT.format("#######"))

        for cmd in self.commands:
            self._cmd(cmd)

        self.log(LOG_WARN_TEXT.format("#######"))


def run(mapping_suite_id, opt_mappings_path=DEFAULT_MAPPINGS_PATH, opt_commands=DEFAULT_COMMANDS):
    cmd = CmdRunner(
        mapping_suite_id=mapping_suite_id,
        mappings_path=opt_mappings_path,
        commands=list(opt_commands)
    )
    cmd.run()


@click.command()
@click.argument('mapping-suite-id', nargs=1, required=True)
@click.option('-c', '--opt-commands', default=DEFAULT_COMMANDS, type=click.Choice(DEFAULT_COMMANDS), multiple=True)
@click.option('-m', '--opt-mappings-path', default=DEFAULT_MAPPINGS_PATH)
def main(mapping_suite_id, opt_mappings_path, opt_commands):
    """
    Processes Mapping Suite (identified by mapping-suite-id):
    - normalisation_resource_generator
    - metadata_generator
    - yarrrml2rml_converter
    - sparql_generator
    - transformer
    """
    run(mapping_suite_id, opt_mappings_path, opt_commands)


if __name__ == '__main__':
    main()
