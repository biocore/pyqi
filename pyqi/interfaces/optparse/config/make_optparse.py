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


from pyqi.core.command import Command
from pyqi.core.interfaces.optparse import (OptparseOption, OptparseUsageExample,
    OptparseResult)
from pyqi.core.interfaces.optparse.output_handler import write_string
from pyqi.core.interfaces.optparse.input_handler import command_handler
from pyqi.commands.make_optparse import CommandConstructor

# Examples of how the command can be used from the command line
usage_examples = [
    OptparseUsageExample(ShortDesc="Fill in an Optparse config template",
                         LongDesc="Construct the beginning of an Optparse configuration file based on the Parameters required by the Command",
                         Ex="%prog -c pyqi.commands.make_optparse.MakeOptparse -m pyqi.commands.make_optparse -o pyqi/interfaces/optparse/config/make_optparse.py")
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
    OptparseOption(InputType=Command,
                    Parameter=CommandConstructor.Parameters['command'],
                    # Name='command', # implied by Parameter
                    # Required=True, # implied by Parameter
                    ShortName='c', # must be defined if desired
                    # Help='An existing Command', # implied by Parameter
                    InputHandler=command_handler), # must be defined if desired
    OptparseOption(InputType=str,
                    Parameter=CommandConstructor.Parameters['mod'],
                    # Name='mod', # implied by Parameter
                    # Required=True, # implied by Parameter
                    ShortName='m', # must be defined if desired
                    # Help='the command source module', # implied by Parameter
                    InputHandler=None), # must be defined if desired
    OptparseOption(InputType=str,
                   Parameter=None,
                   Name='output_fp',
                   Required=True,
                   ShortName='o',
                   Help='The output file',
                   InputHandler=None)
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
    OptparseResult(OutputType=None,
                   Parameter=None,
                   Name='output_fp',
                   OutputHandler=write_string,
                   ResultKey='result')
    ]
