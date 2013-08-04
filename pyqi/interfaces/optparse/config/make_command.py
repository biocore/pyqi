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

from pyqi.interface.cli import CLOption, UsageExample, ParameterConversion, \
        OutputHandler
from pyqi.pyqi_command.make_command import CommandConstructor
from pyqi.interface.output_handler.cli import write_string

usage_examples = [
        UsageExample(ShortDesc="Basic function",
                     LongDesc="Create a basic function with appropriate attribution",
                     Ex='%prog -n example -a "some author" -c "Copyright 2013, The QCLI Project" -e "foo@bar.com" -l BSD --func_version "0.1" --credits "someone else","and another person" -o example.py')
        ]

param_conversions = {
        'name':ParameterConversion(ShortName='n',
                                     LongName='name',
                                     CLType=str),
        'email':ParameterConversion(ShortName='e',
                                     LongName='email',
                                     CLType=str),
        'author':ParameterConversion(ShortName='a',
                                     LongName='author',
                                     CLType=str),
        'license':ParameterConversion(ShortName='l',
                                     LongName='license',
                                     CLType=str),
        'copyright':ParameterConversion(ShortName='c',
                                     LongName='copyright',
                                     CLType=str),
        'credits':ParameterConversion(ShortName=None,
                                     LongName='credits',
                                     CLType=str),
        'func_version':ParameterConversion(ShortName=None,
                                     LongName='func_version',
                                     CLType=str),
        }

additional_options = [
        CLOption(Type='output_file',
                 Help='the resulting Python file',
                 Name='output_fp',
                 Required=True,
                 LongName='output-fp',
                 CLType='new_filepath',
                 ShortName='o',
                 ResultName='result')
        ]

output_map = {'result':OutputHandler(OptionName='output_fp',
                                     Function=write_string)}
