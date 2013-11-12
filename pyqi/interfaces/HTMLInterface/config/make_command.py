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
__version__ = "0.2.0-dev"
__maintainer__ = "Daniel McDonald"
__email__ = "mcdonadt@colorado.edu"

from pyqi.core.interfaces.HTMLInterface import (HTMLInterfaceOption,
                                           HTMLDownload, HTMLPage,
                                           HTMLInterfaceUsageExample)
from pyqi.core.interfaces.optparse.input_handler import string_list_handler
from pyqi.core.interfaces.HTMLInterface.output_handler import newline_list_of_strings
from pyqi.core.command import (make_command_in_collection_lookup_f,
    make_command_out_collection_lookup_f)
from pyqi.commands.make_command import CommandConstructor

cmd_in_lookup = make_command_in_collection_lookup_f(CommandConstructor)
cmd_out_lookup = make_command_out_collection_lookup_f(CommandConstructor)

usage_examples = [
    HTMLInterfaceUsageExample(ShortDesc="Basic Command",
                         LongDesc="Create a basic Command with appropriate attribution",
                         Ex='%prog -n example -a "some author" -c "Copyright 2013, The pyqi project" -e "foo@bar.com" -l BSD --command-version "0.1" --credits "someone else","and another person" -o example.py')
]

inputs = [
    HTMLInterfaceOption(Parameter=cmd_in_lookup('name'),
                   ShortName='n'),
    HTMLInterfaceOption(Parameter=cmd_in_lookup('author'),
                   ShortName='a'),
    HTMLInterfaceOption(Parameter=cmd_in_lookup('email'),
                   ShortName='e'),
    HTMLInterfaceOption(Parameter=cmd_in_lookup('license'),
                   ShortName='l'),
    HTMLInterfaceOption(Parameter=cmd_in_lookup('copyright'),
                   ShortName='c'),
    HTMLInterfaceOption(Parameter=cmd_in_lookup('version'), Name='command-version'),
    HTMLInterfaceOption(Parameter=cmd_in_lookup('credits'),
                   Handler=string_list_handler,
                   Help='comma-separated list of other authors'),
    #OptparseOption(Parameter=cmd_in_lookup('test_code'),
    #              Type=None, Action='store_true'),
    HTMLInterfaceOption(Parameter=None,
                   Type='new_filepath',
                   ShortName='o',
                   Name='download-file',
                   Required=True,
                   Help='The name of the file to download which conatins generated Python code. (e.g. MyCommand.py)')
]

outputs = [
    ### InputName is used to tie this output to output-fp, which is an input...
    HTMLDownload(Parameter=cmd_out_lookup('result'),
                   Handler=newline_list_of_strings,
                   FilenameLookup='download-file',
                   FileExtension='.py')
    
]
