#!/usr/bin/env python

#-----------------------------------------------------------------------------
# Copyright (c) 2013, The BiPy Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------

__author__ = "Daniel McDonald"
__copyright__ = "Copyright 2013, The pyqi project"
__credits__ = ["Daniel McDonald", "Jai Ram Rideout", "Doug Wendel", "Greg Caporaso"]
__license__ = "BSD"
__version__ = "0.2.0"
__maintainer__ = "Daniel McDonald"
__email__ = "mcdonadt@colorado.edu"

from pyqi.core.interfaces.optparse import (OptparseOption,
                                           OptparseUsageExample,
                                           OptparseResult)
from pyqi.core.interfaces.optparse.output_handler import write_string
from pyqi.core.command import make_parameter_collection_lookup_f
from pyqi.commands.make_bash_completion import CommandConstructor

param_lookup = make_parameter_collection_lookup_f(CommandConstructor)

usage_examples = [
    OptparseUsageExample(ShortDesc="Create a bash completion script",
                         LongDesc="Create a bash completion script for use with a pyqi driver",
                         Ex="%prog --command-config-module pyqi.interfaces.optparse.config --driver-name pyqi -o ~/.bash_completion.d/pyqi")
]

inputs = [
    OptparseOption(Parameter=param_lookup('command_config_module')),
    OptparseOption(Parameter=param_lookup('driver_name')),
    OptparseOption(Parameter=None,
                   InputType='new_filepath',
                   ShortName='o',
                   Name='output-fp',
                   Required=True,
                   Help='output filepath')
]

outputs = [
    OptparseResult(ResultKey='result',
                   OutputHandler=write_string,
                   OptionName='output-fp')
]
