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
from pyqi.core.command import CommandIn, ParameterCollection
from unittest import TestCase, main

__credits__ = ["Daniel McDonald", "Jai Ram Rideout", "Doug Wendel",
    "Greg Caporaso"]

class MakeOptparseTests(TestCase):
    def setUp(self):
        self.cmd = MakeOptparse()

    def test_run(self):
        exp = win_text

        pc = CommandIn(Name='DUN', Required=True, DataType=str, Description="")
        bool_param = CommandIn(Name='imabool', DataType=bool,
                               Description='zero or one', Required=False)

        class stubby:
            CommandIns = ParameterCollection([pc, bool_param])
            CommandOuts = ParameterCollection([])

        obs = self.cmd(**{'command_module':'foobar',
                          'command':stubby(),
                          'author': 'bob',
                          'email': 'bob@bob.bob',
                          'license': 'very permissive license',
                          'copyright': 'what\'s that?',
                          'version': '1.0'
        })

        self.assertEqual(obs['result'], exp.splitlines())

win_text = """#!/usr/bin/env python
from __future__ import division

__author__ = "bob"
__copyright__ = "what's that?"
__credits__ = ["bob"]
__license__ = "very permissive license"
__version__ = "1.0"
__maintainer__ = "bob"
__email__ = "bob@bob.bob"

from pyqi.core.interfaces.optparse import (OptparseUsageExample,
                                           OptparseOption, OptparseResult)
from pyqi.core.command import (make_command_in_collection_lookup_f,
                               make_command_out_collection_lookup_f)
from foobar import CommandConstructor

# If you need access to input or output handlers provided by pyqi, consider
# importing from the following modules:
# pyqi.core.interfaces.optparse.input_handler
# pyqi.core.interfaces.optparse.output_handler
# pyqi.interfaces.optparse.input_handler
# pyqi.interfaces.optparse.output_handler

# Convenience function for looking up parameters by name.
cmd_in_lookup = make_command_in_collection_lookup_f(CommandConstructor)
cmd_out_lookup = make_command_out_collection_lookup_f(CommandConstructor)

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
    # OptparseOption(Parameter=cmd_in_lookup('name_of_a_command_in'),
    #                Type='existing_filepath', # the optparse type of input
    #                Action='store', # the optparse action
    #                Handler=None, # Apply a function to the input value to convert it into the type expected by Parameter.DataType
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
    #                Type='new_filepath',
    #                Action='store',
    #                Handler=None, # we don't need a Handler because this option isn't being converted into a format that a Parameter expects
    #                ShortName='o',
    #                Name='output-fp',
    #                Required=True,
    #                Help='output filepath')

    OptparseOption(Parameter=cmd_in_lookup('DUN'),
                   Type=str,
                   Action='store', # default is 'store', change if desired
                   Handler=None, # must be defined if desired
                   ShortName=None, # must be defined if desired
                   # Name='DUN', # implied by Parameter
                   # Required=True, # implied by Parameter
                   # Help='', # implied by Parameter
                   ),
    OptparseOption(Parameter=cmd_in_lookup('imabool'),
                   Type=None,
                   Action='store_true', # default is 'store', change if desired
                   Handler=None, # must be defined if desired
                   ShortName=None, # must be defined if desired
                   # Name='imabool', # implied by Parameter
                   # Required=False, # implied by Parameter
                   # Help='zero or one', # implied by Parameter
                   # Default=None, # implied by Parameter
                   # DefaultDescription=None, # implied by Parameter),
]

# outputs map result keys to output options and handlers. It is not necessary
# to supply an associated option, but if you do, it must be an option from the
# inputs list (above).
outputs = [
    # An example option that maps to a CommandIn.
    # OptparseResult(Parameter=cmd_out_lookup('name_of_a_command_out'),
    #                Handler=write_string, # a function applied to the output of the Command
    #                # the name of the option (defined in inputs, above), whose
    #                # value will be made available to Handler. This name
    #                # can be either an underscored or dashed version of the
    #                # option name (e.g., 'output_fp' or 'output-fp')
    #                InputName='output-fp'),
    #
    # An example option that does not map to a CommandIn.
    # OptparseResult(Parameter=cmd_out_lookup('some_other_result'),
    #                Handler=print_string)

]
"""

if __name__ == '__main__':
    main()
