#!/usr/bin/env python

#-----------------------------------------------------------------------------
# Copyright (c) 2013, The BiPy Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------

from __future__ import division
from qcli.core.command import Command, Parameter

__author__ = "Daniel McDonald"
__copyright__ = "Copyright 2013, the QCLI project"
__credits__ = ["Daniel McDonald", "Jai Ram Rideout", "Greg Caporaso",
               "Doug Wendel"]
__license__ = "BSD"
__version__ = "0.1"
__maintainer__ = "Daniel McDonald"
__email__ = "mcdonadt@colorado.edu"
__status__ = "Development"

header = """#!/usr/bin/env

from qcli.interface.cli import CLOption, UsageExample, ParameterConversion
from %(mod)s import CommandConstructor

usage_examples = [
    ]

param_conversions = {
    %(param_conversions)s
    }

additional_options = [
    ]
"""

param_fmt = """\t\t'%(name)s':ParameterConversion(ShortName="MUST BE DEFINED",
\t\t\t\t\tLongName='%(name)s',
\t\t\t\t\tCLType=%(type)s),
"""

class MakeCLI(Command):
    BriefDescription = "Consume a Command, stub out a CLI configuration"
    LongDescription = """Construct and stub out the basic CLI configuration for a given Command"""

    def run(self, **kwargs):
        prms = kwargs['command']._get_parameters()
        pc = ''.join([param_fmt % {'name':p.Name, 'type':p.Type} for p in prms])
        header_format = {'mod':kwargs['mod'], 'param_conversions': pc}

        return {'result': header % header_format}

    def _get_parameters(self):
        return [Parameter(Name='command',Required=True,Type=Command,
                          Help='some required parameter'),
                Parameter(Name='mod',Required=True,Type=str,
                          Help='the command source module')]

CommandConstructor = MakeCLI
