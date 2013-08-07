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
from pyqi.core.command import Parameter, ParameterCollection, Command
from pyqi.core.exception import IncompetentDeveloperError

class CommandTests(TestCase):
    def test_init(self):
        """Jog the init"""
        c = Command()
        self.assertEqual(len(c.Parameters), 0)
        with self.assertRaises(NotImplementedError):
            _ = c()

    def test_subclass_init(self):
        """Exercise the subclassing"""
        class foo(Command):
            Parameters = ParameterCollection([Parameter(str,'help1','a',True),
                    Parameter(str,'help2','b',False)])
            def run(self, **kwargs):
                return {}

        obs = foo()

        self.assertEqual(len(obs.Parameters), 2)
        self.assertEqual(obs.run(bar={'a':10}), {})

class ParameterTests(TestCase):
    def test_init(self):
        """Jog the init"""
        obj = Parameter(str,'help','a',False)
        self.assertEqual(obj.DataType, str)
        self.assertEqual(obj.Help, 'help')
        self.assertEqual(obj.Name, 'a')
        self.assertEqual(obj.Required, False)
        self.assertEqual(obj.Default, None)
        self.assertEqual(obj.DefaultDescription, None)
        self.assertRaises(IncompetentDeveloperError, Parameter, str, 'help',
                'a', True, 'x')


if __name__ == '__main__':
    main()
