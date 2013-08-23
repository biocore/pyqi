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
__version__ = "0.1.0-dev"
__maintainer__ = "Daniel McDonald"
__email__ = "mcdonadt@colorado.edu"

from pyqi.core.command import Command, Parameter, ParameterCollection

header = """#!/usr/bin/env python
from __future__ import division

__author__ = "%(author)s"
__copyright__ = "%(copyright)s"
__credits__ = [%(credits)s]
__license__ = "%(license)s"
__version__ = "%(command_version)s"
__maintainer__ = "%(author)s"
__email__ = "%(email)s"

"""

command_imports = """from pyqi.core.command import Command, Parameter, ParameterCollection
"""

command_format = """class %s(Command):
    BriefDescription = "FILL IN A 1 SENTENCE DESCRIPTION"
    LongDescription = "GO INTO MORE DETAIL"
    Parameters = ParameterCollection([
        Parameter(Name='foo', DataType=str,
                  Description='some required parameter', Required=True),
        Parameter(Name='bar', DataType=int,
                  Description='some optional parameter', Required=False,
                  Default=1)
    ])

    def run(self, **kwargs):
        # EXAMPLE:
        # return {'result_1': kwargs['foo'] * kwargs['bar'],
        #         'result_2': "Some output bits"}
        raise NotImplementedError("You must define this method")

CommandConstructor = %s"""

test_fmt = """from unittest import TestCase, main
from FILL IN MODULE PATH import %(name)s

class %(name)sTests(TestCase):
    def setUp(self):
        self.cmd_obj = %(name)s()

    def test_run(self):
        self.fail()

if __name__ == '__main__':
    main()"""

class MakeCommand(Command):
    BriefDescription = "Construct a stubbed out Command object"
    LongDescription = """This command is intended to construct the basics of a Command object so that a developer can dive straight into the implementation of the command"""
    Parameters = ParameterCollection([
        Parameter(Name='name', DataType=str,
                  Description='the name of the Command', Required=True),
        Parameter(Name='email', DataType=str,
                  Description='maintainer email address', Required=True),
        Parameter(Name='author', DataType=str,
                  Description='the Command author', Required=True),
        Parameter(Name='license', DataType=str,
                  Description='the license for the Command', Required=True),
        Parameter(Name='copyright', DataType=str,
                  Description='the Command copyright', Required=True),
        Parameter(Name='command_version', DataType=str,
                  Description='the Command version', Required=True),
        Parameter(Name='credits', DataType=str,
                  Description='comma-separated list of other authors',
                  Required=False, Default=''),
        Parameter(Name='test_code', DataType=bool,
                  Description='create stubbed out test code',
                  Required=False, Default=False)
    ])

    def run(self, **kwargs):
        # build a string formatting dictionary for the file header
        head = {}
        head['email']        = kwargs['email']
        head['author']       = kwargs['author']
        head['license']      = kwargs['license']
        head['copyright']    = kwargs['copyright']
        head['command_version'] = kwargs['command_version']

        # Credits always includes author.
        credits = [head['author']]
        if len(kwargs['credits']) > 0:
            credits.extend(kwargs['credits'].split(','))

        f = lambda x: '"%s"' % x
        head['credits'] = ', '.join(map(f, credits))

        result_lines = [header % head]
        
        if kwargs['test_code']:
            result_lines.append(test_fmt % {'name':kwargs['name']})
        else:
            result_lines.append(command_imports)
            result_lines.append('\n')
            result_lines.append(command_format % (kwargs['name'], kwargs['name']))

        output = {}
        output['result'] = ''.join(result_lines)

        return output

CommandConstructor = MakeCommand
