#!/usr/bin/env python

#-----------------------------------------------------------------------------
# Copyright (c) 2013, The BiPy Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------

from __future__ import division
from pyqi.commands.make_optparse import MakeOptparse
from pyqi.core.command import Parameter, ParameterCollection
from unittest import TestCase, main

__author__ = "Daniel McDonald"
__copyright__ = "Copyright 2013, The QCLI Project"
__credits__ = ["Daniel McDonald", "Jai Ram Rideout", "Doug Wendel", "Greg Caporaso"]
__license__ = "BSD"
__version__ = "0.1.0-dev"
__maintainer__ = "Daniel McDonald"
__email__ = "mcdonadt@colorado.edu"

class MakeOptparseTests(TestCase):
    def setUp(self):
        pass

    def test_init(self):
        obj = MakeOptparse()

    def test_run(self):
        obj = MakeOptparse()
        exp = win_text

        class stubby:
            Parameters = ParameterCollection([Parameter(Name='DUN',
                    Required=True, DataType=str, Help='')])

        obs = obj.run(**{'mod':'foobar', 'command':stubby()})
        self.assertEqual(obs['result'], exp)


win_text = """#!/usr/bin/env python

from pyqi.core.interfaces.optparse import (OptparseOption, OptparseUsageExample,
        OptparseOption, OptparseResult)
from foobar import CommandConstructor

# Examples of how the command can be used from the command line
usage_examples = [
    OptparseUsageExample(ShortDesc="A short single sentence description of the example",
                         LongDesc="A longer, more detailed description",
                         Ex="%prog --foo --bar some_file")
    ]

# Inputs map command line arguments and values onto Parameters. It is possible to
# define options here that do not exist as parameters, e.g., an output file
inputs = [
    # An example option that has a direct relationship with a Parameter 
    #OptparseOption(InputType=str, # can be non-primitive, handled by InputHandler
### do we want to define a helper method, get_param = lambda x: CommandConstructor.Parameters[x]
### and drop it in each config file via the template?
    #               Parameter=CommandConstructor.Parameters['name_of_a_parameter'],
    #               # Required, implied by Parameter. Can be promoted by setting True
    #               # Name, implied by Parameter
    #               ShortName='n', # a parameter short name, can be None
    #               # Help, implied by Parameter
    #               InputHandler=None), # Apply a function to the input value
    # An example option that does not have an associated Parameter
    #OptparseOption(InputType='new_filepath',
    #               Parameter=None,
    #               Required=True,
    #               Name='output_fp',
    #               ShortName='o',
    #               Help='Output file path',
    #               InputHandler=None)
    OptparseOption(InputType=<type 'str'>,
                    Parameter=CommandConstructor.Parameters['DUN'],
                    # Name='DUN', # implied by Parameter
                    # Required=True, # implied by Parameter
                    # ShortName=None, # must be defined if desired
                    # Help='', # implied by Parameter
                    InputHandler=None), # must be defined if desired

    ]

# Outputs map result keys to output options and handlers. It is not necessary
# to gave an associated option.
outputs = [
    # An example option that maps to a result key
    #OptparseResult(OutputType=None, # undefined at this time
    #               Parameter=CommandConstructor.Parameters['name_of_a_parameter'],
    #               # Name, implied by Parameter
    #               OutputHandler=f, # a function applied to the value at ResultKey
    #               ResultKey='some_result'),
    # An example option that does not map to a result key
    #OptparseResult(OutputType=None,
    #               Parameter=None, # no Command.Parameter associated
    #               Name='output_fp',
    #               OutputHandler=write_string,
    #               ResultKey='some_other_result')
    ]
"""


if __name__ == '__main__':
    main()
