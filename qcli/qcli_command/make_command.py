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
__version__ = "0.1-dev"
__maintainer__ = "Daniel McDonald"
__email__ = "mcdonadt@colorado.edu"
__status__ = "Development"

from qcli.core.container import WithIO
from qcli.core.command import Command, Parameter

header = """#!/usr/bin/env python

from __future__ import division
from qcli.core.command import Command, Parameter

__author__ = "%(author)s"
__copyright__ = "%(copyright)s"
__credits__ = ["%(author)s", %(credits)s]
__license__ = "%(license)s"
__version__ = "%(func_version)s"
__maintainer__ = "%(author)s"
__email__ = "%(email)s"

"""

command_format = """class %s(Command):
    BriefDescription = "FILL IN A 1 SENTENCE DESCRIPTION"
    LongDescription = "GO INTO MORE DETAIL"

    def run(self, **kwargs):
        # EXAMPLE:
        # return {'result_1': kwargs['foo'] * kwargs['bar'],
        #         'result_2': "Some output bits"}
        raise NotImplementedError("You must define this method")

    def _get_parameters(self):
        # EXAMPLE:
        # return [Parameter(Name='foo',Required=True,Type=str,
        #                   Help='some required parameter'),
        #         Parameter(Name='bar',Required=False,Type=int,
        #                   Help='some optional parameter',Default=1)]
        raise NotImplementedError("You must define this method")

CommandConstructor = %s
"""

class CLIStub(Command):
    BriefDescription = "Construct a stringified stubbed out ``Command`` object"
    LongDescription = """This method will is intended to construct the basics of a ``Command`` object to so that a developer can dive straight into the fun bits"""

    def run(self, **kwargs):
        # build a string formatting dictionary for the file header
        head = dict([(k,v) for k,v in kwargs.items() if k not in ['name']])
        
        if 'credits' in head:
            f = lambda x: '"%s"' % x
            head['credits'] = ', '.join(map(f, head['credits'].split(',')))

        result_lines = [header % head]
        result_lines.append(command_format % (kwargs['name'], kwargs['name']))

        return {'result':''.join(result_lines)}

    def _get_parameters(self):
        return [Parameter(Name='name',Required=True,Type=str,
                          Help='the name of the ``Command``'), 
                Parameter(Name='email',Required=True,Type=str,
                          Help='maintainer email address'),
                Parameter(Name='author',Required=True,Type=str,
                          Help='the function author'),
                Parameter(Name='license',Required=True,Type=str,
                          Help='the license for the function'),
                Parameter(Name='copyright',Required=True,Type=str,
                          Help='the function copyright'),
                Parameter(Name='func_version',Required=True,Type=str,
                          Help='the function version'),
                Parameter(Name='credits',Required=False,Type=str,Default='',
                          Help='comma separated list of other authors')]
    
CommandConstructor = CLIStub
