#!/usr/bin/env python

#-----------------------------------------------------------------------------
# Copyright (c) 2013, The BiPy Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------

__author__ = "Daniel McDonald"
__copyright__ = "Copyright 2013, The QCLI Project"
__credits__ = ["Daniel McDonald", "Greg Caporaso", "Doug Wendel",
               "Jai Ram Rideout"]
__license__ = "BSD"
__version__ = "0.1.0-dev"
__maintainer__ = "Daniel McDonald"
__email__ = "mcdonadt@colorado.edu"

from pyqi.core.command import Command, Parameter, ParameterCollection

header = """#!/usr/bin/env python

__author__ = "%(author)s"
__copyright__ = "%(copyright)s"
__credits__ = ["%(author)s", %(credits)s]
__license__ = "%(license)s"
__version__ = "%(func_version)s"
__maintainer__ = "%(author)s"
__email__ = "%(email)s"

"""

command_imports = """from __future__ import division
from pyqi.core.command import Command, Parameter
"""

command_format = """class %s(Command):
    BriefDescription = "FILL IN A 1 SENTENCE DESCRIPTION"
    LongDescription = "GO INTO MORE DETAIL"
    Parameters = ParameterCollection([
        Parameter(Name='foo',Required=True,DataType=str,
                  Help='some required parameter'),
        Parameter(Name='bar',Required=False,DataType=int,
                  Help='some optional parameter',Default=1)
        ])
        
    def run(self, **kwargs):
        # EXAMPLE:
        # return {'result_1': kwargs['foo'] * kwargs['bar'],
        #         'result_2': "Some output bits"}
        raise NotImplementedError("You must define this method")

CommandConstructor = %s
"""

test_fmt = """from unittest import TestCase, main
from FILL IN MODULE PATH import %(name)s

class %(name)sTests(TestCase):
    def setUp(self):
        self.cmd_obj = %(name)s()

    def test_run(self):
        self.fail()

if __name__ == '__main__':
    main()
"""

class MakeCommand(Command):
    BriefDescription = "Construct a stringified stubbed out ``Command`` object"
    LongDescription = """This method will is intended to construct the basics of a ``Command`` object to so that a developer can dive straight into the fun bits"""
    Parameters = ParameterCollection([
        Parameter(Name='name',Required=True,DataType=str,
                  Help='the name of the ``Command``'), 
        Parameter(Name='email',Required=True,DataType=str,
                  Help='maintainer email address'),
        Parameter(Name='author',Required=True,DataType=str,
                  Help='the function author'),
        Parameter(Name='license',Required=True,DataType=str,
                  Help='the license for the function'),
        Parameter(Name='copyright',Required=True,DataType=str,
                  Help='the function copyright'),
        Parameter(Name='func_version',Required=True,DataType=str,
                  Help='the function version'),
        Parameter(Name='testcode',Required=False, DataType=bool,
                  Default=False, Help='create test code'),
### Default is not honored right now, and not reported right (shows "none")
        Parameter(Name='credits',Required=False,DataType=str,Default='',
                  Help='comma separated list of other authors')
        ])
    
    def run(self, **kwargs):
        # build a string formatting dictionary for the file header
        head = {}
        head['email']        = kwargs['email']
        head['author']       = kwargs['author']
        head['license']      = kwargs['license']
        head['copyright']    = kwargs['copyright']
        head['func_version'] = kwargs['func_version']
        
        if 'credits' in kwargs:
            f = lambda x: '"%s"' % x
            head['credits'] = ', '.join(map(f, kwargs['credits'].split(',')))
        else:
            head['credits'] = ''

        result_lines = [header % head]
        result_lines.append(command_imports)
        result_lines.append(command_format % (kwargs['name'], kwargs['name']))

        output = {}
        output['result'] = ''.join(result_lines)

        if 'testcode' in kwargs:
            result_lines = [header % head]
            result_lines.append(test_fmt % {'name':kwargs['name']})
            output['result_testcode'] = ''.join(result_lines)

        return output

CommandConstructor = MakeCommand
