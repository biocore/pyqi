#!/usr/bin/env

from qcli.interface.cli import CLOption, UsageExample, ParameterConversion
from qcli.qcli_command.make_cli import CommandConstructor

usage_examples = [
    ]

param_conversions = {
            'command':ParameterConversion(ShortName='c',
                    LongName='existing_command',
                    CLType=str),
            'mod':ParameterConversion(ShortName='m',
                    LongName='mod',
                    CLType=str),
    }

additional_options = [
    ]
