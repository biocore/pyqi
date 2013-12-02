#!/usr/bin/env python

#-----------------------------------------------------------------------------
# Copyright (c) 2013, The BiPy Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------
from __future__ import division

__credits__ = ["Greg Caporaso", "Daniel McDonald", "Doug Wendel",
               "Jai Ram Rideout"]

from unittest import TestCase, main
from pyqi.core.command import CommandIn, CommandOut, ParameterCollection, Command
from pyqi.core.exception import (IncompetentDeveloperError, 
                                 UnknownParameterError, 
                                 MissingParameterError)

class CommandTests(TestCase):
    def setUp(self):
        class stubby(Command):
            CommandIns = ParameterCollection([
                            CommandIn('a',int,'', Required=True),
                            CommandIn('b',int,'', Required=False, Default=5),
                            CommandIn('c',int,'', Required=False, Default=10,
                                      ValidateValue=lambda x: x == 10)])
            def run(self, **kwargs):
                return {}
        self.stubby = stubby

    def test_init(self):
        """Jog the init"""
        c = Command()
        self.assertEqual(len(c.CommandIns), 0)
        self.assertEqual(len(c.CommandOuts), 0)
        with self.assertRaises(NotImplementedError):
            _ = c()

    def test_subclass_init(self):
        """Exercise the subclassing"""
        class foo(Command):
            Parameters = ParameterCollection([CommandIn('a', str, 'help1',
                                                        Required=True),
                                              CommandIn('b', str, 'help2',
                                                        Required=False)])
            def run(self, **kwargs):
                return {}

        obs = foo()

        self.assertEqual(len(obs.Parameters), 2)
        self.assertEqual(obs.run(bar={'a':10}), {})

    def test_validate_kwargs(self):
        stub = self.stubby()
        kwargs = {'a':10, 'b':20}
        
        # should work
        stub._validate_kwargs(kwargs)

        kwargs = {'b':20}
        self.assertRaises(MissingParameterError, stub._validate_kwargs, kwargs)
        
        kwargs = {'a':10, 'b':20, 'c':10}
        stub._validate_kwargs(kwargs)
        kwargs = {'a':10, 'b':20, 'c':20}
        self.assertRaises(ValueError, stub._validate_kwargs, kwargs)

    def test_set_defaults(self):
        stub = self.stubby()
        kwargs = {'a':10}
        exp = {'a':10,'b':5,'c':10}
        
        stub._set_defaults(kwargs)

        self.assertEqual(kwargs, exp)

class ParameterTests(TestCase):
    def test_init(self):
        """Jog the init"""
        obj = CommandIn('a', str, 'help', Required=False)
        self.assertEqual(obj.Name, 'a')
        self.assertEqual(obj.DataType, str)
        self.assertEqual(obj.Description, 'help')
        self.assertEqual(obj.Required, False)
        self.assertEqual(obj.Default, None)
        self.assertEqual(obj.DefaultDescription, None)
        self.assertRaises(IncompetentDeveloperError, CommandIn, 'a', str,
                          'help', True, 'x')

class ParameterCollectionTests(TestCase):
    def setUp(self):
        self.pc = ParameterCollection([CommandIn('foo',str, 'help')])
    
    def test_init(self):
        """Jog the init"""
        params = [CommandIn('a', str, 'help', Required=False),
                  CommandIn('b', float, 'help2', Required=True)]
        obj = ParameterCollection(params)

        self.assertEqual(obj.Parameters, params)
        self.assertEqual(obj['a'], params[0])
        self.assertEqual(obj['b'], params[1])

        # Duplicate Parameter names.
        params.append(CommandIn('a', int, 'help3'))
        with self.assertRaises(IncompetentDeveloperError):
            _ = ParameterCollection(params)

    def test_getitem(self):
        self.assertRaises(UnknownParameterError, self.pc.__getitem__, 'bar')
        self.assertEqual(self.pc['foo'].Name, 'foo') # make sure we can getitem

    def test_setitem(self):
        self.assertRaises(TypeError, self.pc.__setitem__, 'bar', 10)

if __name__ == '__main__':
    main()
