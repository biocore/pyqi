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
__credits__ = ["Jai Ram Rideout", "Daniel McDonald"]
__license__ = "BSD"
__version__ = "0.2.0"
__maintainer__ = "Jai Ram Rideout"
__email__ = "jai.rideout@gmail.com"

from pyqi.core.command import Command, Parameter, ParameterCollection

header_format = """#!/usr/bin/env python
from __future__ import division

__author__ = "%(author)s"
__copyright__ = "%(copyright)s"
__credits__ = [%(credits)s]
__license__ = "%(license)s"
__version__ = "%(version)s"
__maintainer__ = "%(author)s"
__email__ = "%(email)s"
"""

class CodeHeaderGenerator(Command):
    BriefDescription = "Generate header code for use in a Python file"
    LongDescription = ("Generate valid Python code containing header "
                       "information, such as author, email address, "
                       "maintainer, version, etc.. This code can be placed at "
                       "the top of a Python file.")
    Parameters = ParameterCollection([
        Parameter(Name='author', DataType=str,
                  Description='author/maintainer name', Required=True),
        Parameter(Name='email', DataType=str,
                  Description='maintainer email address', Required=True),
        Parameter(Name='license', DataType=str,
                  Description='license (e.g., BSD)', Required=True),
        Parameter(Name='copyright', DataType=str,
                  Description='copyright (e.g., Copyright 2013, The pyqi '
                              'project)', Required=True),
        Parameter(Name='version', DataType=str,
                  Description='version (e.g., 0.1)', Required=True),
        Parameter(Name='credits', DataType=list,
                  Description='list of other authors',
                  Required=False, Default=None)
    ])

    def run(self, **kwargs):
        # Build a string formatting dictionary for the file header.
        head = {}
        head['author']    = kwargs['author']
        head['email']     = kwargs['email']
        head['license']   = kwargs['license']
        head['copyright'] = kwargs['copyright']
        head['version']   = kwargs['version']

        # Credits always includes author.
        credits = [head['author']]
        if kwargs['credits']:
            credits.extend(kwargs['credits'])

        f = lambda x: '"%s"' % x
        head['credits'] = ', '.join(map(f, credits))

        return {'result': (header_format % head).split('\n')}

CommandConstructor = CodeHeaderGenerator
