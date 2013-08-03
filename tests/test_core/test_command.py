#!/usr/bin/env python

#-----------------------------------------------------------------------------
# Copyright (c) 2013, The BiPy Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------
from __future__ import division

__author__ = "Daniel McDonald"
__copyright__ = "Copyright 2013, The QCLI Project"
__credits__ = ["Greg Caporaso", "Daniel McDonald", "Doug Wendel",
               "Jai Ram Rideout"]
__license__ = "BSD"
__version__ = "0.1.0-dev"
__maintainer__ = "Daniel McDonald"
__email__ = "wasade@gmail.com"

from unittest import TestCase, main
from qcli.core.command import Parameter, Command
from qcli.core.exception import IncompetentDeveloperError

class CommandTests(TestCase):
    pass

class ParameterTests(TestCase):
    def test_init(self):
        obj = Parameter('a','b','c',False)
        self.assertEqual(obj.Type, 'a')
        self.assertEqual(obj.Help, 'b')
        self.assertEqual(obj.Name, 'c')
        self.assertEqual(obj.Required, False)
        self.assertEqual(obj.Default, None)
        self.assertEqual(obj.DefaultDescription, None)
        self.assertRaises(IncompetentDeveloperError, Parameter, 'a','b','c',
                            True,'x')
if __name__ == '__main__':
    main()

