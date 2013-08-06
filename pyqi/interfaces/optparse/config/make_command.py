#!/usr/bin/env python

#-----------------------------------------------------------------------------
# Copyright (c) 2013, The BiPy Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------

__author__ = "Daniel McDonald"
__copyright__ = "Copyright 2013, The QCLI Project"
__credits__ = ["Daniel McDonald", "Greg Caporaso", "Doug Wendel",
               "Jai Ram Rideout"]
__license__ = "BSD"
__version__ = "0.1.0-dev"
__maintainer__ = "Daniel McDonald"
__email__ = "mcdonadt@colorado.edu"

from pyqi.core.interfaces.optparse import (OptparseOption,
                                           OptparseResult,
                                           OptparseUsageExample)
from pyqi.core.interfaces.optparse.output_handler import write_string
from pyqi.commands.make_command import CommandConstructor

usage_examples = [
    OptparseUsageExample(ShortDesc="Basic function",
                         LongDesc="Create a basic function with appropriate attribution",
                         Ex='%prog -n example -a "some author" -c "Copyright 2013, The QCLI Project" -e "foo@bar.com" -l BSD --func_version "0.1" --credits "someone else","and another person" -o example.py')
]

inputs = [
    OptparseOption(InputType=str,
                   Parameter=CommandConstructor.Parameters['name'],
                   ShortName='n'),
    OptparseOption(InputType=str,
                   Parameter=CommandConstructor.Parameters['email'],
                   ShortName='e'),
    OptparseOption(InputType=str,
                   Parameter=CommandConstructor.Parameters['author'],
                   ShortName='a'),
    OptparseOption(InputType=str,
                   Parameter=CommandConstructor.Parameters['license'],
                   ShortName='l'),
    OptparseOption(InputType=str,
                   Parameter=CommandConstructor.Parameters['copyright'],
                   ShortName='c'),
    OptparseOption(InputType=str,
                   Parameter=CommandConstructor.Parameters['func_version'],
                   ShortName=None),
    OptparseOption(InputType=str,
                   Parameter=CommandConstructor.Parameters['credits'],
                   ShortName=None),
    OptparseOption(InputType='new_filepath',
                   Help='the resulting Python file',
                   Name='output_fp',
                   Required=True,
                   ShortName='o')
]

outputs = [
    OptparseResult(OutputType=None,
                   Parameters=None,
                   Name='output_fp',
                   OutputHandler=write_string,
                   ResultKey='result')
    ]
