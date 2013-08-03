#!/usr/bin/env python

from qcli.interface.cli import CLOption, UsageExample, ParameterConversion
from qcli.qcli_command.make_cli import CommandConstructor

def command_handler(x):
    module, klass = x.rsplit('.',1)
    mod = __import__(module, fromlist=[klass])
    return getattr(mod, klass)()

usage_examples = [UsageExample(ShortDesc='Stub out a CLI configuration',
                               LongDesc="""Consume an existing Command object and produce the base CLI configuration""",
                               Ex="%prog -c MakeCLI -m qcli.qcli_command -o make_cli.py")
    ]

param_conversions = {
            'command':ParameterConversion(ShortName='c',
                    LongName='command',
                    CLType=str,
                    InHandler=command_handler),
            'mod':ParameterConversion(ShortName='m',
                    LongName='mod',
                    CLType=str),
    }

additional_options = [
        CLOption(Type='output_file',
                 Help='the resulting configuration file',
                 Name='output_fp',
                 Required=True,
                 LongName='output-fp',
                 CLType='new_filepath',
                 ShortName='o',
                 ResultName='result')
    ]
