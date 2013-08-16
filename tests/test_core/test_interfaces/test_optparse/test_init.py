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
from pyqi.core.interfaces.optparse import (OptparseResult, OptparseOption,
                                           OptparseUsageExample,
                                           OptparseInterface, optparse_factory,
                                           optparse_main)
from pyqi.core.exception import IncompetentDeveloperError
from pyqi.core.command import Command, Parameter, ParameterCollection

class OptparseResultTests(TestCase):
    # Nothing to test yet
    pass

class OptparseOptionTests(TestCase):
    def setUp(self):
        p = Parameter('number', int, 'some int', Required=False, Default=42,
                      DefaultDescription='forty-two')
        # With associated parameter.
        self.opt1 = OptparseOption(p, int)

        # Without associated parameter.
        self.opt2 = OptparseOption(None, int, InputHandler=None, ShortName='n',
                                   Name='number', Required=False,
                                   Help='help!!!')

    def test_init(self):
        self.assertEqual(self.opt1.InputType, int)
        self.assertEqual(self.opt1.Help, 'some int')
        self.assertEqual(self.opt1.Name, 'number')
        self.assertEqual(self.opt1.Default, 42)
        self.assertEqual(self.opt1.DefaultDescription, 'forty-two')
        self.assertEqual(self.opt1.ShortName, None)
        self.assertEqual(self.opt1.Required, False)

    def test_str(self):
        exp = '--number'
        obs = str(self.opt1)
        self.assertEqual(obs, exp)

        exp = '-n/--number'
        obs = str(self.opt2)
        self.assertEqual(obs, exp)

class OptparseUsageExampleTests(TestCase):
    def test_init(self):
        obj = OptparseUsageExample(ShortDesc='a', LongDesc='b', Ex='c')
        self.assertEqual(obj.ShortDesc, 'a')
        self.assertEqual(obj.LongDesc, 'b')
        self.assertEqual(obj.Ex, 'c')

        with self.assertRaises(IncompetentDeveloperError):
            _ = OptparseUsageExample('a', 'b', Ex=None)

def oh(key, data, opt_value=None):
    return data * 2

class OptparseInterfaceTests(TestCase):
    def setUp(self):
        self.interface = fabulous()
    
    def test_init(self):
        self.assertRaises(IncompetentDeveloperError, OptparseInterface)

    def test_validate_usage_examples(self):
        with self.assertRaises(IncompetentDeveloperError):
            _ = NoUsageExamples()

    # TODO: this test should be migrated to tests for the Interface baseclass
    # if/when they exist.
    def test_validate_inputs(self):
        with self.assertRaises(IncompetentDeveloperError):
            _ = DuplicateOptionMappings()

    def test_input_handler(self):
        obs = self.interface._input_handler(['--c','foo'])
        self.assertEqual(obs.items(), [('c', 'foo')])

    def test_build_usage_lines(self):
        obs = self.interface._build_usage_lines([])
        self.assertEqual(obs, usage_lines)

    def test_output_handler(self):
        results = {'itsaresult':20}
        obs = self.interface._output_handler(results)
        self.assertEqual(obs, {'itsaresult':40})

class GeneralTests(TestCase):
    def setUp(self):
        self.obj = optparse_factory(ghetto,
                [OptparseUsageExample('a','b','c')],
                [OptparseOption(InputType=str,
                                Parameter=ghetto.Parameters['c'],
                                ShortName='n')],
                [OptparseResult(ResultKey='itsaresult', OutputHandler=oh)])

    def test_optparse_factory(self):
        # exercise it
        _ = self.obj()

    def test_optparse_main(self):
        # exercise it
        _ = optparse_main(self.obj, ['testing', '--c', 'bar'])

class ghetto(Command):
    Parameters = ParameterCollection([Parameter('c', str, 'b')])

    def run(self, **kwargs):
        return {'itsaresult':10}

class fabulous(OptparseInterface):
    CommandConstructor = ghetto

    def _get_inputs(self):
        return [OptparseOption(InputType=str,
                Parameter=self.CommandConstructor.Parameters['c'],
                ShortName='n')]

    def _get_usage_examples(self):
        return [OptparseUsageExample('a','b','c')]

    def _get_outputs(self):
        return [OptparseResult(ResultKey='itsaresult', OutputHandler=oh)]

# Doesn't have any usage examples...
class NoUsageExamples(fabulous):
    def _get_usage_examples(self):
        return []

# More than one option mapping to the same Parameter...
class DuplicateOptionMappings(fabulous):
    def _get_inputs(self):
        return [
            OptparseOption(InputType=str,
            Parameter=self.CommandConstructor.Parameters['c'], ShortName='n'),

            OptparseOption(Parameter=self.CommandConstructor.Parameters['c'],
            Name='i-am-a-duplicate')
        ]

usage_lines = """usage: %prog [options] {}

[] indicates optional input (order unimportant)
{} indicates required input (order unimportant)



Example usage: 
Print help message and exit
 %prog -h

a: b
 c"""


if __name__ == '__main__':
    main()
