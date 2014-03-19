#!/usr/bin/env python

#-----------------------------------------------------------------------------
# Copyright (c) 2013, The BiPy Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------

__credits__ = ["Daniel McDonald", "Greg Caporaso", "Doug Wendel",
               "Jai Ram Rideout"]

import os
import sys

from pyqi.util import is_py2

if is_py2():
    from StringIO import StringIO
else:
    from io import StringIO

from shutil import rmtree
from tempfile import mkdtemp
from unittest import TestCase, main
from pyqi.core.interfaces.optparse.output_handler import (write_string,
        write_list_of_strings, print_list_of_strings)
from pyqi.core.exception import IncompetentDeveloperError

class OutputHandlerTests(TestCase):
    def setUp(self):
        self.output_dir = mkdtemp()
        self.fp = os.path.join(self.output_dir, 'test_file.txt')

    def tearDown(self):
        rmtree(self.output_dir)

    def test_write_string(self):
        """Correctly writes a string to file."""
        # can't write without a path
        self.assertRaises(IncompetentDeveloperError, write_string, 'a','b')

        write_string('foo', 'bar', self.fp)
        with open(self.fp, 'U') as obs_f:
            obs = obs_f.read()

        self.assertEqual(obs, 'bar\n')

    def test_write_list_of_strings(self):
        """Correctly writes a list of strings to file."""
        # can't write without a path
        self.assertRaises(IncompetentDeveloperError, write_list_of_strings,
                          'a', ['b', 'c'])

        write_list_of_strings('foo', ['bar', 'baz'], self.fp)
        with open(self.fp, 'U') as obs_f:
            obs = obs_f.read()

        self.assertEqual(obs, 'bar\nbaz\n')

    def test_print_list_of_strings(self):
        """Correctly prints a list of strings."""
        # Save stdout and replace it with something that will capture the print
        # statement. Note: this code was taken from here:
        # http://stackoverflow.com/questions/4219717/how-to-assert-output-
        #     with-nosetest-unittest-in-python/4220278#4220278
        saved_stdout = sys.stdout
        try:
            out = StringIO()
            sys.stdout = out
            print_list_of_strings('this is ignored', ['foo', 'bar', 'baz'])

            exp = 'foo\nbar\nbaz\n'
            obs = out.getvalue()
            self.assertEqual(obs, exp)
        finally:
            sys.stdout = saved_stdout


if __name__ == '__main__':
    main()
