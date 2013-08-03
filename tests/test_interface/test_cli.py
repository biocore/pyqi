#!/usr/bin/env python

#-----------------------------------------------------------------------------
# Copyright (c) 2013, The BiPy Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------

__author__ = "Daniel McDonald"
__copyright__ = "Copyright 2013, The QIIME Project"
__credits__ = ["Greg Caporaso", "Daniel McDonald", "Doug Wendel",
                       "Jai Ram Rideout"]
__license__ = "BSD"
__version__ = "0.1.0-dev"
__maintainer__ = "Daniel McDonald"
__email__ = "mcdonadt@colorado.edu"

from unittest import TestCase, main
from qcli.interface.cli import OutputHandler, CLOption

class OutputHandlerTests(TestCase):
    def test_init(self):
        # why...
        obj = OutputHandler('a','b')
        self.assertEqual(obj.OptionName, 'a')
        self.assertEqual(obj.Function, 'b')

if __name__ == '__main__':
    main()
