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
__credits__ = ["Daniel McDonald", "Greg Caporaso", "Doug Wendel",
               "Jai Ram Rideout"]
__license__ = "BSD"
__version__ = "0.1.0-dev"
__maintainer__ = "Daniel McDonald"
__email__ = "mcdonadt@colorado.edu"

from pyqi.core.command import Command
from pyqi.core.interfaces.optparse import (OptparseOption, OptparseUsageExample,
    OptparseResult)
from pyqi.core.interfaces.optparse.output_handler import write_string
from pyqi.core.interfaces.optparse.input_handler import command_handler
from pyqi.core.command import make_parameter_collection_lookup_f
from pyqi.commands.make_optparse import CommandConstructor

param_lookup = make_parameter_collection_lookup_f(CommandConstructor)

usage_examples = [
    OptparseUsageExample(ShortDesc="Fill in an optparse config template",
                         LongDesc="Construct the beginning of an optparse configuration file based on the Parameters required by the Command",
                         Ex="%prog -c pyqi.commands.make_optparse.MakeOptparse -m pyqi.commands.make_optparse -o pyqi/interfaces/optparse/config/make_optparse.py")
]

inputs = [
    OptparseOption(Parameter=param_lookup('command'),
                   ShortName='c',
                   InputHandler=command_handler),
    OptparseOption(Parameter=param_lookup('command_module'),
                   ShortName='m'),
    OptparseOption(Parameter=None,
                   InputType='new_filepath',
                   ShortName='o',
                   Name='output-fp',
                   Required=True,
                   Help='output filepath to store generated optparse Python configuration file')
]

outputs = [
    OptparseResult(ResultKey='result',
                   OutputHandler=write_string,
                   OptionName='output-fp')
]
