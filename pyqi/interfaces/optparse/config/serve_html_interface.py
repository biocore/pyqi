#!/usr/bin/env python

#-----------------------------------------------------------------------------
# Copyright (c) 2013, The BiPy Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------

__credits__ = ["Evan Bolyen"]

from pyqi.core.interfaces.optparse import (OptparseOption,
                                           OptparseResult,
                                           OptparseUsageExample)
from pyqi.core.interfaces.optparse.input_handler import string_list_handler
from pyqi.core.interfaces.optparse.output_handler import print_string
from pyqi.core.command import make_command_in_collection_lookup_f, make_command_out_collection_lookup_f
from pyqi.commands.serve_html_interface import CommandConstructor

cmdin_lookup = make_command_in_collection_lookup_f(CommandConstructor)
cmdout_lookup = make_command_out_collection_lookup_f(CommandConstructor)



usage_examples = [
    OptparseUsageExample(ShortDesc="Start html interface",
                         LongDesc="Starts an html interface server on the specified --port and --interface-module",
                         Ex='%prog -p 8080 -m pyqi.interfaces.html.config')
]

inputs = [
    OptparseOption(Parameter=cmdin_lookup('port'),
                   ShortName='p',
                   Type=int),

    OptparseOption(Parameter=cmdin_lookup('interface_module'),
                   ShortName='m',
                   Required=True)
]

outputs = [
    OptparseResult(Parameter=cmdout_lookup('result'),
                   Handler=print_string)
]
