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

import sys

from unittest import TestCase, main
from pyqi.core.interface import get_command_names, get_command_config
from pyqi.util import is_py2
import pyqi.interfaces.optparse.config.make_bash_completion

class TopLevelTests(TestCase):
    def test_get_command_names(self):
        """Test that command names are returned from a config directory."""
        exp = ['make-bash-completion', 'make-command', 'make-optparse',
               'make-release', 'serve-html-interface']
        obs = get_command_names('pyqi.interfaces.optparse.config')
        self.assertEqual(obs, exp)

        # Invalid config dir.
        with self.assertRaises(ImportError):
            _ = get_command_names('foo.bar.baz-aar')

    def test_get_command_config(self):
        """Test successful and unsuccessful module loading."""
        cmd_cfg, error_msg = get_command_config(
                'pyqi.interfaces.optparse.config', 'make_bash_completion')
        self.assertEqual(cmd_cfg,
                         pyqi.interfaces.optparse.config.make_bash_completion)
        self.assertEqual(error_msg, None)

        cmd_cfg, error_msg = get_command_config(
                'hopefully.nonexistent.python.module', 'umm',
                exit_on_failure=False)
        self.assertEqual(cmd_cfg, None)

        py2_err = 'No module named hopefully.nonexistent.python.module.umm'
        py3_err = "No module named 'hopefully'"
        if is_py2():
            self.assertEqual(error_msg, py2_err)
        else:
            self.assertEqual(error_msg, py3_err)


if __name__ == '__main__':
    main()
