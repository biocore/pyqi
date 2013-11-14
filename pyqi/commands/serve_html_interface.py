#!/usr/bin/env python
from __future__ import division

__author__ = "Evan Bolyen"
__copyright__ = "Copyright 2013, The pyqi project"
__credits__ = ["Evan Bolyen", "Daniel McDonald", "Jai Ram Rideout", "Doug Wendel", "Greg Caporaso"]
__license__ = "BSD"
__version__ = "0.0.1-dev"
__maintainer__ = "Evan Bolyen"
__email__ = "ebolyen@gmail.com"

from pyqi.core.command import (Command, CommandIn, CommandOut, ParameterCollection)
from pyqi.core.interfaces.HTMLInterface import start_server

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

    CommandOuts = None

    def run(self, **kwargs):
        start_server(kwargs['port'], kwargs['interface_module'])

CommandConstructor = ServeHTMLInterface
