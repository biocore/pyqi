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
__copyright__ = "Copyright 2013, The pyqi project"
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
        
        pc = Parameter(Name='DUN', Required=True, DataType=str, Description="")

        class stubby:
            Parameters = ParameterCollection([pc])

        obs = obj.run(**{'command_module':'foobar', 'command':stubby()})
        
        self.assertEqual(obs['result'], exp) 

win_text = """#!/usr/bin/env python

from pyqi.core.interfaces.optparse import (OptparseUsageExample,
                                           OptparseOption, OptparseResult)
from pyqi.core.command import make_parameter_collection_lookup_f
from foobar import CommandConstructor

# If you need access to input or output handlers provided by pyqi, consider
# importing from the following modules:
# pyqi.core.interfaces.optparse.input_handler
# pyqi.core.interfaces.optparse.output_handler
# pyqi.interfaces.optparse.input_handler
# pyqi.interfaces.optparse.output_handler

# Convenience function for looking up parameters by name.
param_lookup = make_parameter_collection_lookup_f(CommandConstructor)

# Examples of how the command can be used from the command line using an
# optparse interface.
usage_examples = [
    OptparseUsageExample(ShortDesc="A short single sentence description of the example",
                         LongDesc="A longer, more detailed description",
                         Ex="%prog --foo --bar some_file")
]

# inputs map command line arguments and values onto Parameters. It is possible
# to define options here that do not exist as parameters, e.g., an output file.
inputs = [
    # An example option that has a direct relationship with a Parameter.
    # OptparseOption(Parameter=param_lookup('name_of_a_parameter'),
    #                InputType='existing_filepath', # the optparse type of input
    #                InputAction='store', # the optparse action
    #                InputHandler=None, # Apply a function to the input value to convert it into the type expected by Parameter.DataType
    #                ShortName='n', # a parameter short name, can be None
    #                # Name='foo', # implied by Parameter.Name. Can be overwritten here if desired
    #                # Required=False, # implied by Parameter.Required. Can be promoted by setting True
    #                # Help='help', # implied by Parameter.Description. Can be overwritten here if desired
    #                # Default=None, # implied by Parameter.Default. Can be overwritten here if desired
    #                # DefaultDescription=None, # implied by Parameter.DefaultDescription. Can be overwritten here if desired
    #                convert_to_dashed_name=True), # whether the Name (either implied by Parameter or defined above) should have underscores converted to dashes when displayed to the user
    #
    # An example option that does not have an associated Parameter.
    # OptparseOption(Parameter=None,
    #                InputType='new_filepath',
    #                InputAction='store',
    #                InputHandler=None, # we don't need an InputHandler because this option isn't being converted into a format that a Parameter expects
    #                ShortName='o',
    #                Name='output-fp',
    #                Required=True,
    #                Help='output filepath')

    OptparseOption(Parameter=param_lookup('DUN'),
                   InputType=<type 'str'>,
                   InputAction='store', # default is 'store', change if desired
                   InputHandler=None, # must be defined if desired
                   ShortName=None), # must be defined if desired
                   # Name='DUN', # implied by Parameter
                   # Required=True, # implied by Parameter
                   # Help='', # implied by Parameter
                   

]

# outputs map result keys to output options and handlers. It is not necessary
# to supply an associated option, but if you do, it must be an option from the
# inputs list (above).
outputs = [
    # An example option that maps to a result key.
    # OptparseResult(ResultKey='some_result',
    #                OutputHandler=write_string, # a function applied to the value at ResultKey
    #
    #                # the name of the option (defined in inputs, above), whose
    #                # value will be made available to OutputHandler. This name
    #                # can be either an underscored or dashed version of the
    #                # option name (e.g., 'output_fp' or 'output-fp')
    #                OptionName='output-fp'), 
    #
    # An example option that does not map to a result key.
    # OptparseResult(ResultKey='some_other_result',
    #                OutputHandler=print_string)
]
"""

if __name__ == '__main__':
    main()
