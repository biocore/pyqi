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
from qcli.interface.cli import OutputHandler, CLOption, UsageExample, \
        ParameterConversion
from qcli.core.exception import IncompetentDeveloperError

class OutputHandlerTests(TestCase):
    def test_init(self):
        # why...
        obj = OutputHandler('a','b')
        self.assertEqual(obj.OptionName, 'a')
        self.assertEqual(obj.Function, 'b')

class CLOptionTests(TestCase):
    def test_init(self):
        obj = CLOption('a','b','c','d',str)
        self.assertEqual(obj.Type, 'a')
        self.assertEqual(obj.Help, 'b')
        self.assertEqual(obj.Name, 'c')
        self.assertEqual(obj.LongName, 'd')
        self.assertEqual(obj.CLType, str)

    def test_str(self):
        obj = CLOption('a','b','c','d',str)
        exp = '--d'
        obs = str(obj)
        self.assertEqual(obs, exp)

        obj = CLOption('a','b','c','d',str, ShortName='e')
        exp = '-e/--d'
        obs = str(obj)
        self.assertEqual(obs, exp)

    def test_fromParameter(self):
        from qcli.core.command import Parameter
        p = Parameter(Type='a',Help='b',Name='c',Required=False)
        obj = CLOption.fromParameter(p, LongName='d',CLType=str)
        self.assertEqual(obj.Type,'a')
        self.assertEqual(obj.Help,'b')
        self.assertEqual(obj.Name,'c')
        self.assertEqual(obj.Required,False)

class UsageExampleTests(TestCase):
    def test_init(self):
        obj = UsageExample(ShortDesc='a', LongDesc='b', Ex='c')
        self.assertEqual(obj.ShortDesc, 'a')
        self.assertEqual(obj.LongDesc, 'b')
        self.assertEqual(obj.Ex, 'c')

        self.assertRaises(IncompetentDeveloperError, UsageExample, 'a', 'b')

class ParameterConversionTests(TestCase):
    def test_init(self):
        obj = ParameterConversion('a',str,CLAction='store')
        self.assertEqual(obj.LongName, 'a')
        self.assertEqual(obj.CLType, str)
        self.assertEqual(obj.CLAction, 'store')

        self.assertRaises(IncompetentDeveloperError, ParameterConversion, 'a',
                          'not valid')

if __name__ == '__main__':
    main()
