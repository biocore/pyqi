#!/usr/bin/env python

#-----------------------------------------------------------------------------
# Copyright (c) 2013, The BiPy Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------

from __future__ import division

__credits__ = ["Evan Bolyen"]

from pyqi.core.command import (Command, CommandIn, CommandOut, ParameterCollection)
from pyqi.core.interfaces.html import start_server

class ServeHTMLInterface(Command):
    BriefDescription = "Start the HTMLInterface server"
    LongDescription = "Start the HTMLInterface server and load the provided interface_module and port"
    CommandIns = ParameterCollection([
        CommandIn(Name='port', DataType=int,
                  Description='The port to run the server on', Required=False,
                  Default=8080),

        CommandIn(Name='interface_module', DataType=str,
                  Description='The module to serve the interface for', Required=True)
    ])

    CommandOuts = ParameterCollection([
          CommandOut(Name='result',DataType=str, 
                    Description='Signals the termination of the HTMLInterface server')
          ])

    def run(self, **kwargs):
        """Start the HTMLInterface server with the port and interface_module"""
        fin = start_server(kwargs['port'], kwargs['interface_module'])

        return {'result': fin}

CommandConstructor = ServeHTMLInterface
