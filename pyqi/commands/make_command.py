#!/usr/bin/env python

#-----------------------------------------------------------------------------
# Copyright (c) 2013, The BiPy Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------

__credits__ = ["Daniel McDonald", "Greg Caporaso", "Doug Wendel",
               "Jai Ram Rideout"]

from pyqi.core.command import (Command, CommandIn, CommandOut, 
    ParameterCollection)
from pyqi.commands.code_header_generator import CodeHeaderGenerator

command_imports = """from pyqi.core.command import (Command, CommandIn, CommandOut, 
    ParameterCollection)"""

command_format = """class %s(Command):
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

CommandConstructor = %s"""

test_format = """from unittest import TestCase, main
from FILL IN MODULE PATH import %(name)s

class %(name)sTests(TestCase):
    def setUp(self):
        self.cmd_obj = %(name)s()

    def test_run(self):
        self.fail()


if __name__ == '__main__':
    main()"""

class MakeCommand(CodeHeaderGenerator):
    BriefDescription = "Construct a stubbed out Command object"
    LongDescription = """This command is intended to construct the basics of a Command object so that a developer can dive straight into the implementation of the command"""

    CommandIns = ParameterCollection(
          CodeHeaderGenerator.CommandIns.Parameters + [
          CommandIn(Name='name', DataType=str,
                    Description='the name of the Command', Required=True),
          CommandIn(Name='test_code', DataType=bool,
                    Description='create stubbed out unit test code',
                    Required=False, Default=False)
          ]
    )
    CommandOuts = ParameterCollection([
          CommandOut(Name='result',DataType=list, 
                    Description='The resulting template')
          ]
    )

    def run(self, **kwargs):
        code_header_lines = super(MakeCommand, self).run(
                author=kwargs['author'], email=kwargs['email'],
                license=kwargs['license'], copyright=kwargs['copyright'],
                version=kwargs['version'], credits=kwargs['credits'])['result']

        result_lines = code_header_lines

        if kwargs['test_code']:
            result_lines.extend(
                    (test_format % {'name': kwargs['name']}).split('\n'))
        else:
            result_lines.extend(command_imports.split('\n'))
            result_lines.append('')
            result_lines.extend((command_format % (
                    kwargs['name'], kwargs['name'])).split('\n'))

        return {'result':  result_lines}

CommandConstructor = MakeCommand
