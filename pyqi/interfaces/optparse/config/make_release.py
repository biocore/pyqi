#!/usr/bin/env python
from __future__ import division

__credits__ = ["Daniel McDonald"]

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
    OptparseOption(Parameter=cmd_in_lookup('package_name')),
    OptparseOption(Parameter=cmd_in_lookup('real_run'), Action='store_true'),
]

outputs = []
