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
                                           HTMLDownload, HTMLPage)
from pyqi.core.interfaces.optparse.input_handler import string_list_handler
from pyqi.core.interfaces.HTMLInterface.output_handler import newline_list_of_strings
from pyqi.core.command import (make_command_in_collection_lookup_f,
    make_command_out_collection_lookup_f)
from pyqi.commands.make_command import CommandConstructor

cmd_in_lookup = make_command_in_collection_lookup_f(CommandConstructor)
cmd_out_lookup = make_command_out_collection_lookup_f(CommandConstructor)

usage_examples = []

inputs = [
    HTMLInterfaceOption(Parameter=cmd_in_lookup('name')),
    HTMLInterfaceOption(Parameter=cmd_in_lookup('author')),
    HTMLInterfaceOption(Parameter=cmd_in_lookup('email')),
    HTMLInterfaceOption(Parameter=cmd_in_lookup('license')),
    HTMLInterfaceOption(Parameter=cmd_in_lookup('copyright')),
    HTMLInterfaceOption(Parameter=cmd_in_lookup('version'), Name='command-version'),
    HTMLInterfaceOption(Parameter=cmd_in_lookup('credits'),
                   Handler=string_list_handler,
                   Help='comma-separated list of other authors'),
    HTMLInterfaceOption(Parameter=None,
                   Name='download-file',
                   Required=True,
                   Help='The name of the file to download which conatins generated Python code. (e.g. MyCommand.py)')
]

outputs = HTMLDownload(Parameter=cmd_out_lookup('result'),
                   Handler=newline_list_of_strings,
                   FilenameLookup='download-file',
                   FileExtension='.py')

#Comment out the above and uncomment the below for an example of a page.

#     HTMLPage(Parameter=cmd_out_lookup('result'),
#              Handler=newline_list_of_strings) 
    

