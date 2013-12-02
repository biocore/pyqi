#!/usr/bin/env python
from __future__ import division

__author__ = "Daniel McDonald"
__copyright__ = "123"
__credits__ = ["Daniel McDonald"]
__license__ = "asd"
__version__ = "123"
__maintainer__ = "Daniel McDonald"
__email__ = "masdasd"

from pyqi.core.interfaces.optparse import (OptparseUsageExample,
                                           OptparseOption, OptparseResult)
from pyqi.core.command import (make_command_in_collection_lookup_f,
                               make_command_out_collection_lookup_f)
from pyqi.commands.make_release import CommandConstructor

# Convenience function for looking up parameters by name.
cmd_in_lookup = make_command_in_collection_lookup_f(CommandConstructor)
cmd_out_lookup = make_command_out_collection_lookup_f(CommandConstructor)

usage_examples = [
    OptparseUsageExample(ShortDesc="Make a release",
                         LongDesc="Make a release, tag it, update version "
                                  "strings and upload to pypi",
                         Ex="%prog --package-name=pyqi --real-run")
]

inputs = [
    OptparseOption(Parameter=cmd_in_lookup('package_name'),
                   Type=str,
                   Action='store', # default is 'store', change if desired
                   Handler=None, # must be defined if desired
                   ShortName=None, # must be defined if desired
                   Name='package-name', # implied by Parameter
                   ),
    OptparseOption(Parameter=cmd_in_lookup('real_run'),
                   Action='store_true', # default is 'store', change if desired
                   Handler=None, # must be defined if desired
                   ShortName=None, # must be defined if desired
                   Name='real-run', # implied by Parameter
                   ),
]

outputs = []
