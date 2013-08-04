#!/usr/bin/env python

#-----------------------------------------------------------------------------
# Copyright (c) 2013, The BiPy Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------

from __future__ import division
from pyqi.core.command import Command, Parameter

__author__ = "Daniel McDonald"
__copyright__ = "Copyright 2013, the QCLI project"
__credits__ = ["Daniel McDonald", "Jai Ram Rideout", "Greg Caporaso",
               "Doug Wendel"]
__license__ = "BSD"
__version__ = "0.1.0-dev"
__maintainer__ = "Daniel McDonald"
__email__ = "mcdonadt@colorado.edu"

header = """#!/usr/bin/env python

from pyqi.interface.cli import CLOption, UsageExample, ParameterConversion
from %(mod)s import CommandConstructor

# How you can use the command from the command line
usage_examples = [
    ]

# Parameter conversions tell the interface how to describe command line 
# options
param_conversions = {
    %(param_conversions)s
    }

# The output map associated keys in the results returned from Command.run
# without output handlers
output_map = {
    }

# In case there are interface specific bits such as output files
additional_options = [
    ]

"""

param_fmt = """        '%(name)s':ParameterConversion(ShortName="MUST BE DEFINED",
                    LongName='%(name)s',
                    CLType=%(type)s),
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
                          Help='An existing Command'),
                Parameter(Name='mod',Required=True,Type=str,
                          Help='the command source module')]
    
CommandConstructor = MakeCLI
