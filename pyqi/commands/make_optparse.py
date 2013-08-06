#!/usr/bin/env python

#-----------------------------------------------------------------------------
# Copyright (c) 2013, The BiPy Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------

from __future__ import division
from pyqi.core.command import Command, Parameter, ParameterCollection

__author__ = "Daniel McDonald"
__copyright__ = "Copyright 2013, the QCLI project"
__credits__ = ["Daniel McDonald", "Jai Ram Rideout", "Greg Caporaso",
               "Doug Wendel"]
__license__ = "BSD"
__version__ = "0.1.0-dev"
__maintainer__ = "Daniel McDonald"
__email__ = "mcdonadt@colorado.edu"

header = """#!/usr/bin/env python

from pyqi.core.interfaces.optparse import (OptparseOption, OptparseUsageExample,
        OptparseOption, OptparseResult)
from %(mod)s import CommandConstructor

# Examples of how the command can be used from the command line
usage_examples = [
    OptparseUsageExample(ShortDesc="A short single sentence description of the example",
                         LongDesc="A longer, more detailed description",
                         Ex="%%prog --foo --bar some_file")
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
%(input_fmt)s
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

### currently filling out by Parameter, but commenting out the implied stuff
input_fmt = """    OptparseOption(InputType=%(datatype)s,
                    Parameter=CommandConstructor.Parameters['%(name)s'],
                    # Name='%(name)s', # implied by Parameter
                    # Required=%(required)s, # implied by Parameter
                    # ShortName=None, # must be defined if desired
                    # Help='%(help)s', # implied by Parameter
                    InputHandler=None), # must be defined if desired
"""

class MakeOptparse(Command):
    BriefDescription = "Consume a Command, stub out an Optparse configuration"
    LongDescription = """Construct and stub out the basic Optparse configuration for a given Command. This template provides comments and examples of what to fill in."""
    Parameters = ParameterCollection([
        Parameter(Name='command',Required=True,DataType=Command,
                  Help='An existing Command'),
        Parameter(Name='mod',Required=True,DataType=str,
                  Help='the command source module')
        ])

    def run(self, **kwargs):
        param_formatted = []
        
        # construct inputs based off of parameters
        for param in kwargs['command'].Parameters.values():
            fmt = {'name':param.Name, 'datatype':param.DataType, 
                   'required':str(param.Required), 'help':param.Help}
            param_formatted.append(input_fmt % fmt)
        
        param_formatted = ''.join(param_formatted)
        header_format = {'mod':kwargs['mod'], 'input_fmt': param_formatted}
        
        return {'result': header % header_format}

CommandConstructor = MakeOptparse
