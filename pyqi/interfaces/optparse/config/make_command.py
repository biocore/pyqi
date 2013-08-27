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
__version__ = "0.2.0"
__maintainer__ = "Daniel McDonald"
__email__ = "mcdonadt@colorado.edu"

from pyqi.core.interfaces.optparse import (OptparseOption,
                                           OptparseResult,
                                           OptparseUsageExample)
from pyqi.core.interfaces.optparse.input_handler import string_list_handler
from pyqi.core.interfaces.optparse.output_handler import write_list_of_strings
from pyqi.core.command import make_parameter_collection_lookup_f
from pyqi.commands.make_command import CommandConstructor

param_lookup = make_parameter_collection_lookup_f(CommandConstructor)

usage_examples = [
    OptparseUsageExample(ShortDesc="Basic Command",
                         LongDesc="Create a basic Command with appropriate attribution",
                         Ex='%prog -n example -a "some author" -c "Copyright 2013, The pyqi project" -e "foo@bar.com" -l BSD --command-version "0.1" --credits "someone else","and another person" -o example.py')
]

inputs = [
    OptparseOption(Parameter=param_lookup('name'),
                   ShortName='n'),
    OptparseOption(Parameter=param_lookup('author'),
                   ShortName='a'),
    OptparseOption(Parameter=param_lookup('email'),
                   ShortName='e'),
    OptparseOption(Parameter=param_lookup('license'),
                   ShortName='l'),
    OptparseOption(Parameter=param_lookup('copyright'),
                   ShortName='c'),
    OptparseOption(Parameter=param_lookup('version'), Name='command-version'),
    OptparseOption(Parameter=param_lookup('credits'),
                   InputHandler=string_list_handler,
                   Help='comma-separated list of other authors'),
    OptparseOption(Parameter=param_lookup('test_code'),
                   InputType=None, InputAction='store_true'),
    OptparseOption(Parameter=None,
                   InputType='new_filepath',
                   ShortName='o',
                   Name='output-fp',
                   Required=True,
                   Help='output filepath to store generated Python code')
]

outputs = [
    OptparseResult(ResultKey='result',
                   OutputHandler=write_list_of_strings,
                   OptionName='output-fp')
]
