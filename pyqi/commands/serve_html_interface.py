#!/usr/bin/env python
from __future__ import division

__author__ = "Evan Bolyen"
__copyright__ = "Copyright 2013, The pyqi project"
__credits__ = ["Evan Bolyen", "Daniel McDonald", "Jai Ram Rideout", "Doug Wendel", "Greg Caporaso"]
__license__ = "BSD"
__version__ = "0.0.1-dev"
__maintainer__ = "Evan Bolyen"
__email__ = "ebolyen@gmail.com"

from pyqi.core.command import  (Command, CommandIn, CommandOut, 
    ParameterCollection)
from pyqi.core.interfaces.HTMLInterface import start_server

class ServeHTMLInterface(Command):
    BriefDescription = "Bootstrap the HTMLInterface server"
    LongDescription = "Start the HTMLInterface server and load the provided interface_module and port"
    CommandIns = ParameterCollection([
        CommandIn(Name='port', DataType=int,
                  Description='The port to run the server on', Required=False,
                  Default=8080),

        CommandIn(Name='interface_module', DataType=str,
                  Description='The module to serve the interface for', Required=True)
    ])

    CommandOuts = ParameterCollection([
        CommandOut(Name='result', DataType=str,
                   Description='Does nothing.')
    ])

    def run(self, **kwargs):
        # EXAMPLE:
        # return {'result_1': kwargs['foo'] * kwargs['bar'],
        #         'result_2': "Some output bits"}
        result = start_server(kwargs['port'], kwargs['interface_module'])
        return {'result': result}

CommandConstructor = ServeHTMLInterface
