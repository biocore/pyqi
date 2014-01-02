#!/usr/bin/env python

#-----------------------------------------------------------------------------
# Copyright (c) 2013, The BiPy Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------

__credits__ = ["Daniel McDonald", "Jai Ram Rideout", "Doug Wendel",
    "Greg Caporaso"]

from pyqi.core.interfaces.optparse import (OptparseOption,
                                           OptparseUsageExample,
                                           OptparseResult)
from pyqi.core.interfaces.optparse.output_handler import write_string
from pyqi.core.command import (make_command_in_collection_lookup_f,
        make_command_out_collection_lookup_f)
from pyqi.commands.make_bash_completion import CommandConstructor

cmd_in_lookup = make_command_in_collection_lookup_f(CommandConstructor)
cmd_out_lookup = make_command_out_collection_lookup_f(CommandConstructor)

usage_examples = [
    OptparseUsageExample(ShortDesc="Create a bash completion script",
                         LongDesc="Create a bash completion script for use with a pyqi driver",
                         Ex="%prog --command-config-module pyqi.interfaces.optparse.config --driver-name pyqi -o ~/.bash_completion.d/pyqi")
]

inputs = [
    OptparseOption(Parameter=cmd_in_lookup('command_config_module')),
    OptparseOption(Parameter=cmd_in_lookup('driver_name')),
    OptparseOption(Parameter=None,
                   Type='new_filepath',
                   ShortName='o',
                   Name='output-fp',
                   Required=True,
                   Help='output filepath')
]

outputs = [
    OptparseResult(Parameter=cmd_out_lookup('result'),
                   Handler=write_string,
                   InputName='output-fp')
]
