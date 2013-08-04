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
__version__ = "0.1-dev"
__maintainer__ = "Daniel McDonald"
__email__ = "mcdonadt@colorado.edu"

from unittest import TestCase, main
from pyqi.interface.input_handler.cli import command_handler
from pyqi.pyqi_command.make_cli import MakeCLI

class CLIInputHandlerTests(TestCase):
    def setUp(self):
        pass

    def test_command_handler(self):
        exp = MakeCLI()
        obs = command_handler('pyqi.pyqi_command.make_cli.MakeCLI')
        self.assertEqual(type(obs), type(exp))

if __name__ == '__main__':
    main()
