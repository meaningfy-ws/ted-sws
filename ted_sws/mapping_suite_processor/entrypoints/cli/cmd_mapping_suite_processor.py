#!/usr/bin/python3

import os
from pathlib import Path
from typing import Tuple, List

import click

from ted_sws.core.adapters.cmd_runner import CmdRunner as BaseCmdRunner, DEFAULT_MAPPINGS_PATH
from ted_sws.data_manager.entrypoints.cli import cmd_generate_mapping_resources
from ted_sws.event_manager.adapters.log import SeverityLevelType
from ted_sws.event_manager.adapters.logger import LOG_INFO_TEXT, LOG_WARN_TEXT
from ted_sws.mapping_suite_processor.entrypoints.cli import cmd_yarrrml2rml_converter, cmd_metadata_generator, \
    cmd_sparql_generator, cmd_resources_injector

DEFAULT_COMMANDS: Tuple = (
    'normalisation_resource_generator',
    'resources_injector',
    'metadata_generator',
    'yarrrml2rml_converter',
    'sparql_generator'
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

        mapping_suite_path = Path(os.path.realpath(mappings_path)) / Path(mapping_suite_id)
        if not mapping_suite_path.is_dir():
            error_msg = f"No such MappingSuite[{mapping_suite_id}]"
            self.log_failed_msg(error_msg)
            raise FileNotFoundError(error_msg)

    def _cmd(self, cmd: str):
        if cmd == 'normalisation_resource_generator':
            cmd_generate_mapping_resources.run(
                mapping_suite_id=self.mapping_suite_id,
                opt_mappings_folder=self.mappings_path
            )
        elif cmd == 'resources_injector':
            cmd_resources_injector.run(
                mapping_suite_id=self.mapping_suite_id,
                opt_mappings_folder=self.mappings_path
            )
        elif cmd == 'metadata_generator':
            cmd_metadata_generator.run(
                mapping_suite_id=self.mapping_suite_id,
                opt_mappings_folder=self.mappings_path
            )
        elif cmd == 'yarrrml2rml_converter':
            cmd_yarrrml2rml_converter.run(
                mapping_suite_id=self.mapping_suite_id,
                opt_mappings_folder=self.mappings_path
            )
        elif cmd == 'sparql_generator':
            cmd_sparql_generator.run(
                mapping_suite_id=self.mapping_suite_id,
                opt_mappings_folder=self.mappings_path
            )

    def run_cmd(self):
        self.log("Running " + LOG_WARN_TEXT.format(self.commands) + " for " + LOG_INFO_TEXT.format(
            f"MappingSuite[{self.mapping_suite_id}]"
        ) + " ... ")
        self.log(LOG_WARN_TEXT.format("#######"))

        for cmd in self.commands:
            self.log(LOG_WARN_TEXT.format("# " + cmd), SeverityLevelType.WARNING)
            self._cmd(cmd)

        self.log(LOG_WARN_TEXT.format("#######"))


def run(mapping_suite_id, opt_mappings_folder=DEFAULT_MAPPINGS_PATH, opt_commands=DEFAULT_COMMANDS):
    cmd = CmdRunner(
        mapping_suite_id=mapping_suite_id,
        mappings_path=opt_mappings_folder,
        commands=list(opt_commands)
    )
    cmd.run()


@click.command()
@click.argument('mapping-suite-id', nargs=1, required=True)
@click.option('-c', '--opt-commands', default=DEFAULT_COMMANDS, type=click.Choice(DEFAULT_COMMANDS), multiple=True)
@click.option('-m', '--opt-mappings-folder', default=DEFAULT_MAPPINGS_PATH)
def main(mapping_suite_id, opt_mappings_folder, opt_commands):
    """
    Processes Mapping Suite (identified by mapping-suite-id):
    - normalisation_resource_generator
    - resources_injector
    - metadata_generator
    - yarrrml2rml_converter
    - sparql_generator
    """
    run(mapping_suite_id, opt_mappings_folder, opt_commands)


if __name__ == '__main__':
    main()
