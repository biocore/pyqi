#!/usr/bin/env python
from __future__ import division

#-----------------------------------------------------------------------------
# Copyright (c) 2013, The BiPy Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------

__credits__ = ["Jai Ram Rideout"]

from unittest import TestCase, main
from pyqi.commands.make_command import MakeCommand

class MakeCommandTests(TestCase):
    def setUp(self):
        """Set up a MakeCommand instance to use in the tests."""
        self.cmd = MakeCommand()

    def test_run_command_code_generation(self):
        """Correctly generates stubbed out Command code."""
        obs = self.cmd(name='Test', author='bob', email='bob@bob.bob',
                       license='very permissive license',
                       copyright='what\'s that?', version='1.0')
        self.assertEqual(list(obs.keys()), ['result'])

        obs = obs['result']
        self.assertEqual(obs, exp_command_code1.splitlines())

    def test_run_test_code_generation(self):
        """Correctly generates stubbed out unit test code."""
        obs = self.cmd(name='Test', author='bob', email='bob@bob.bob',
                       license='very permissive license',
                       copyright='what\'s that?', version='1.0',
                       credits=['another person'], test_code=True)
        self.assertEqual(list(obs.keys()), ['result'])

        obs = obs['result']
        self.assertEqual('\n'.join(obs), exp_test_code1)


exp_command_code1 = """#!/usr/bin/env python
from __future__ import division

__author__ = "bob"
__copyright__ = "what's that?"
__credits__ = ["bob"]
__license__ = "very permissive license"
__version__ = "1.0"
__maintainer__ = "bob"
__email__ = "bob@bob.bob"

from pyqi.core.command import (Command, CommandIn, CommandOut, 
    ParameterCollection)

class Test(Command):
    BriefDescription = "FILL IN A 1 SENTENCE DESCRIPTION"
    LongDescription = "GO INTO MORE DETAIL"
    CommandIns = ParameterCollection([
        CommandIn(Name='foo', DataType=str,
                  Description='some required parameter', Required=True),
        CommandIn(Name='bar', DataType=int,
                  Description='some optional parameter', Required=False,
                  Default=1)
    ])

    CommandOuts = ParameterCollection([
        CommandOut(Name="result_1", DataType=str, Description="xyz"),
        CommandOut(Name="result_2", DataType=str, Description="123"),
    ])

    def run(self, **kwargs):
        # EXAMPLE:
        # return {'result_1': kwargs['foo'] * kwargs['bar'],
        #         'result_2': "Some output bits"}
        raise NotImplementedError("You must define this method")

CommandConstructor = Test"""

exp_test_code1 = """#!/usr/bin/env python
from __future__ import division

__author__ = "bob"
__copyright__ = "what's that?"
__credits__ = ["bob", "another person"]
__license__ = "very permissive license"
__version__ = "1.0"
__maintainer__ = "bob"
__email__ = "bob@bob.bob"

from unittest import TestCase, main
from FILL IN MODULE PATH import Test

class TestTests(TestCase):
    def setUp(self):
        self.cmd_obj = Test()

    def test_run(self):
        self.fail()


if __name__ == '__main__':
    main()"""


if __name__ == '__main__':
    main()
