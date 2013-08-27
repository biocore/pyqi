#!/usr/bin/env python
from __future__ import division

#-----------------------------------------------------------------------------
# Copyright (c) 2013, The BiPy Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------

__author__ = "Jai Ram Rideout"
__copyright__ = "Copyright 2013, The pyqi project"
__credits__ = ["Jai Ram Rideout"]
__license__ = "BSD"
__version__ = "0.2.0"
__maintainer__ = "Jai Ram Rideout"
__email__ = "jai.rideout@gmail.com"

from unittest import TestCase, main
from pyqi.commands.code_header_generator import CodeHeaderGenerator

class CodeHeaderGeneratorTests(TestCase):
    def setUp(self):
        """Set up a CodeHeaderGenerator instance to use in the tests."""
        self.cmd = CodeHeaderGenerator()

    def test_run(self):
        """Correctly generates header with and without credits."""
        obs = self.cmd(author='bob', email='bob@bob.bob',
                       license='very permissive license',
                       copyright='what\'s that?', version='1.0')
        self.assertEqual(obs.keys(), ['result'])

        obs = obs['result']
        self.assertEqual('\n'.join(obs), exp_header1)

        # With credits.
        obs = self.cmd(author='bob', email='bob@bob.bob',
                       license='very permissive license',
                       copyright='what\'s that?', version='1.0',
                       credits=['another person', 'another another person'])
        self.assertEqual(obs.keys(), ['result'])

        obs = obs['result']
        self.assertEqual('\n'.join(obs), exp_header2)


exp_header1 = """#!/usr/bin/env python
from __future__ import division

__author__ = "bob"
__copyright__ = "what's that?"
__credits__ = ["bob"]
__license__ = "very permissive license"
__version__ = "1.0"
__maintainer__ = "bob"
__email__ = "bob@bob.bob"
"""

exp_header2 = """#!/usr/bin/env python
from __future__ import division

__author__ = "bob"
__copyright__ = "what's that?"
__credits__ = ["bob", "another person", "another another person"]
__license__ = "very permissive license"
__version__ = "1.0"
__maintainer__ = "bob"
__email__ = "bob@bob.bob"
"""


if __name__ == '__main__':
    main()
