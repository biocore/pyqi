#!/usr/bin/env python

#-----------------------------------------------------------------------------
# Copyright (c) 2013, The BiPy Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------

__author__ = "Daniel McDonald"
__copyright__ = "Copyright 2013, The pyqi project"
__credits__ = ["Daniel McDonald", "Greg Caporaso", "Doug Wendel",
               "Jai Ram Rideout"]
__license__ = "BSD"
__version__ = "0.1-dev"
__maintainer__ = "Daniel McDonald"
__email__ = "mcdonadt@colorado.edu"

from tempfile import mkdtemp
from shutil import rmtree
from unittest import TestCase, main
from pyqi.core.interfaces.optparse.output_handler import (write_string,
        write_list_of_strings)
from pyqi.core.exception import IncompetentDeveloperError
import os

class CLIOutputHandlerTests(TestCase):
    def setUp(self):
        self.output_dir = mkdtemp()
        self.fp = os.path.join(self.output_dir, 'test_file.txt')

    def tearDown(self):
        rmtree(self.output_dir)

    def test_write_string(self):
        # can't write without a path
        self.assertRaises(IncompetentDeveloperError, write_string, 'a','b')

        write_string('foo', 'bar', self.fp)
        with open(self.fp, 'U') as obs_f:
            obs = obs_f.read()

        self.assertEqual(obs, 'bar\n')

    def test_write_list_of_strings(self):
        # can't write without a path
        self.assertRaises(IncompetentDeveloperError, write_list_of_strings,
                          'a', ['b', 'c'])

        write_list_of_strings('foo', ['bar', 'baz'], self.fp)
        with open(self.fp, 'U') as obs_f:
            obs = obs_f.read()

        self.assertEqual(obs, 'bar\nbaz\n')


if __name__ == '__main__':
    main()
