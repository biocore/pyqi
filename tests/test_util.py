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

import pyqi
from unittest import TestCase, main
from pyqi.util import get_version_string
from pyqi.core.exception import MissingVersionInfoError


class UtilTests(TestCase):
    def test_get_version_string(self):
        """Test extracting a version string given a module string."""
        exp = pyqi.__version__

        obs = get_version_string('pyqi')
        self.assertEqual(obs, exp)

        obs = get_version_string('pyqi.interfaces.optparse.config')
        self.assertEqual(obs, exp)

        with self.assertRaises(ImportError):
            _ = get_version_string('hopefully.bogus.python.module')

if __name__ == '__main__':
    main()
