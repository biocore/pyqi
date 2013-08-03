#!/usr/bin/env python

from qcli.interface.cli import CLOption, UsageExample, ParameterConversion, OutputHandler
from qcli.qcli_command.make_bash_completion import CommandConstructor
from qcli.interface.output_handler.cli import write_string

# How you can use the command from the command line
usage_examples = [UsageExample(ShortDesc="Create a bash completion script",
                               LongDesc="Create a bash completion script for use with a QCLI driver",
                               Ex="%prog --command_cfg_directory qcli.qcli_command.qcli --driver_name qcli -o ~/.bash_completion.d/qcli")
    ]

# Parameter conversions tell the interface how to describe command line 
# options
param_conversions = {
    		'command_cfg_directory':ParameterConversion(ShortName=None,
					LongName='command_cfg_directory',
					CLType=str),
		'driver_name':ParameterConversion(ShortName=None,
					LongName='driver_name',
					CLType=str),

    }

# The output map associated keys in the results returned from Command.run
# without output handlers
output_map = {'result':OutputHandler(OptionName='output_fp',
                                     Function=write_string)
    }

# In case there are interface specific bits such as output files
additional_options = [CLOption(Type='output_file',
                 Help='the resulting configuration file',
                 Name='output_fp',
                 Required=True,
                 LongName='output_fp',
                 CLType='new_filepath',
                 ShortName='o')
    ]

