#!/usr/bin/env python

#-----------------------------------------------------------------------------
# Copyright (c) 2013, The BiPy Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------
from __future__ import division

__author__ = "Jai Ram Rideout"
__copyright__ = "Copyright 2013, The pyqi project"
__credits__ = ["Greg Caporaso", "Daniel McDonald", "Doug Wendel",
               "Jai Ram Rideout"]
__license__ = "BSD"
__version__ = "0.1.0-dev"
__maintainer__ = "Jai Ram Rideout"
__email__ = "jai.rideout@gmail.com"

from unittest import TestCase, main
from pyqi.core.interface import get_command_names

class TopLevelTests(TestCase):
    def test_get_command_names(self):
        """Test that command names are returned from a config directory."""
        exp = ['make_bash_completion', 'make_command', 'make_optparse']
        obs = get_command_names('pyqi.interfaces.optparse.config')
        self.assertEqual(obs, exp)

        # Invalid config dir.
        with self.assertRaises(ImportError):
            _ = get_command_names('foo.bar.baz-aar')


if __name__ == '__main__':
    main()
