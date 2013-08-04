#!/usr/bin/env python

#-----------------------------------------------------------------------------
# Copyright (c) 2013, The BiPy Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------

from __future__ import division
from pyqi.pyqi_command.make_cli import MakeCLI
from pyqi.core.command import Parameter
from unittest import TestCase, main

__author__ = "Daniel McDonald"
__copyright__ = "Copyright 2013, The QCLI Project"
__credits__ = ["Daniel McDonald", "Jai Ram Rideout", "Doug Wendel", "Greg Caporaso"]
__license__ = "BSD"
__version__ = "0.1.0-dev"
__maintainer__ = "Daniel McDonald"
__email__ = "mcdonadt@colorado.edu"

class MakeCLITests(TestCase):
    def setUp(self):
        pass

    def test_init(self):
        obj = MakeCLI()

    def test_run(self):
        obj = MakeCLI()
        exp = win_text
        
        pc = Parameter(Name='DUN', Required=True, Type=str, Help="")

        class stubby:
            def _get_parameters(self):
                return [pc]

        obs = obj.run(**{'mod':'foobar', 'command':stubby()})
        self.assertEqual(obs['result'], exp) 

win_text = """#!/usr/bin/env python

from pyqi.interface.cli import CLOption, UsageExample, ParameterConversion
from foobar import CommandConstructor

# How you can use the command from the command line
usage_examples = [
    ]

# Parameter conversions tell the interface how to describe command line 
# options
param_conversions = {
            'DUN':ParameterConversion(ShortName="MUST BE DEFINED",
                    LongName='DUN',
                    CLType=<type 'str'>),

    }

# The output map associated keys in the results returned from Command.run
# without output handlers
output_map = {
    }

# In case there are interface specific bits such as output files
additional_options = [
    ]

"""

if __name__ == '__main__':
    main()
