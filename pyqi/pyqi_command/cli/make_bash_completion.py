#!/usr/bin/env python

#-----------------------------------------------------------------------------
# Copyright (c) 2013, The BiPy Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------

from pyqi.interface.cli import CLOption, UsageExample, ParameterConversion, OutputHandler
from pyqi.pyqi_command.make_bash_completion import CommandConstructor
from pyqi.interface.output_handler.cli import write_string

__author__ = "Daniel McDonald"
__copyright__ = "Copyright 2013, The QCLI Project"
__credits__ = ["Daniel McDonald", "Jai Ram Rideout", "Doug Wendel", "Greg Caporaso"]
__license__ = "BSD"
__version__ = "0.1.0-dev"
__maintainer__ = "Daniel McDonald"
__email__ = "mcdonadt@colorado.edu"

# How you can use the command from the command line
usage_examples = [UsageExample(ShortDesc="Create a bash completion script",
                               LongDesc="Create a bash completion script for use with a QCLI driver",
                               Ex="%prog --command_cfg_directory pyqi.pyqi_command.pyqi --driver_name pyqi -o ~/.bash_completion.d/pyqi")
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

