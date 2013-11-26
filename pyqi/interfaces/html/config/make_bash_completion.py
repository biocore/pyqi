#!/usr/bin/env python

#-----------------------------------------------------------------------------
# Copyright (c) 2013, The BiPy Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------

__author__ = "Evan Bolyen"
__copyright__ = "Copyright 2013, The pyqi project"
__credits__ = ["Evan Bolyen"]
__license__ = "BSD"
__version__ = "0.2.0-dev"
__maintainer__ = "Evan Bolyen"
__email__ = "ebolyen@gmail.com"

from pyqi.core.interfaces.html import (HTMLInputOption, HTMLDownload, HTMLPage)
from pyqi.core.interfaces.html.output_handler import newline_list_of_strings
from pyqi.core.command import (make_command_in_collection_lookup_f,
    make_command_out_collection_lookup_f)
from pyqi.commands.make_bash_completion import CommandConstructor

cmd_in_lookup = make_command_in_collection_lookup_f(CommandConstructor)
cmd_out_lookup = make_command_out_collection_lookup_f(CommandConstructor)

inputs = [
    HTMLInputOption(Parameter=cmd_in_lookup('command_config_module'), Required=True),
    HTMLInputOption(Parameter=cmd_in_lookup('driver_name'), Required=True),
    HTMLInputOption(Parameter=None,
                   Name='download-file',
                   Required=True,
                   Help='The name of the bash completion script to download. (e.g. my_file)')
]

outputs = [ HTMLDownload(Parameter=cmd_out_lookup('result'),
                   FilenameLookup='download-file',
                   FileExtension='.sh') ]

