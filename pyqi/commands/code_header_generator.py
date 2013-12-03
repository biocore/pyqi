#!/usr/bin/env python
from __future__ import division

#-----------------------------------------------------------------------------
# Copyright (c) 2013, The BiPy Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------

__credits__ = ["Jai Ram Rideout", "Daniel McDonald"]

from pyqi.core.command import (Command, CommandIn, CommandOut, 
    ParameterCollection)

class CodeHeaderGenerator(Command):
    BriefDescription = "Generate header code for use in a Python file"
    LongDescription = ("Generate valid Python code containing header "
                       "information, such as author, email address, "
                       "maintainer, version, etc.. This code can be placed at "
                       "the top of a Python file.")

    CommandIns = ParameterCollection([
        CommandIn(Name='author', DataType=str,
                  Description='author/maintainer name', Required=False,
                  Default=None),
        CommandIn(Name='email', DataType=str,
                  Description='maintainer email address', Required=False,
                  Default=None),
        CommandIn(Name='license', DataType=str,
                  Description='license (e.g., BSD)', Required=False,
                  Default=None),
        CommandIn(Name='copyright', DataType=str,
                  Description='copyright (e.g., Copyright 2013, The pyqi '
                  'project)', Required=False, Default=None),
        CommandIn(Name='version', DataType=str,
                  Description='version (e.g., 0.1)', Required=False,
                  Default=None),
        CommandIn(Name='credits', DataType=list,
                  Description='list of other authors',
                  Required=False, Default=None)
    ])

    CommandOuts = ParameterCollection([
        CommandOut(Name='result', DataType=list,
                   Description='the resulting header')])

    def run(self, **kwargs):
        # Build a string formatting dictionary for the file header.
        head = {}
        head['author'] = kwargs['author']
        head['email'] = kwargs['email']
        head['license'] = kwargs['license']
        head['copyright'] = kwargs['copyright']
        head['version'] = kwargs['version']

        # Credits always includes author. Note that even if neither author nor
        # credits is passed, credits will be an empty list and will be written
        # out
        credits = [head['author']]
        if kwargs['credits'] is not None:
            credits.extend(kwargs['credits'])
        credits = filter(lambda x: x is not None, credits)
        f = lambda x: '"%s"' % x
        head['credits'] = ', '.join(map(f, credits))

        header_lines = []
        header_lines.append("#!/usr/bin/env python")
        header_lines.append("from __future__ import division")
        header_lines.append("")

        if head['author'] is not None:
            header_lines.append('__author__ = "%s"' % head['author'])
        if head['copyright'] is not None:
            header_lines.append('__copyright__ = "%s"' % head['copyright'])
        if head['credits'] is not None:
            header_lines.append('__credits__ = [%s]' % head['credits'])
        if head['license'] is not None:
            header_lines.append('__license__ = "%s"' % head['license'])
        if head['version'] is not None:
            header_lines.append('__version__ = "%s"' % head['version'])
        if head['author'] is not None:
            header_lines.append('__maintainer__ = "%s"' % head['author'])
        if head['email'] is not None:
            header_lines.append('__email__ = "%s"' % head['email'])

        header_lines.append("")
        header_format = ''.join(header_lines)

        return {'result': header_lines}

CommandConstructor = CodeHeaderGenerator
