#!/usr/bin/env python

#-----------------------------------------------------------------------------
# Copyright (c) 2013, The BiPy Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------

__author__ = "Greg Caporaso"
__copyright__ = "Copyright 2013, The pyqi project"
__credits__ = ["Greg Caporaso", "Daniel McDonald", "Gavin Huttley",
               "Rob Knight", "Doug Wendel", "Jai Ram Rideout",
               "Jose Antonio Navas Molina"]
__license__ = "BSD"
__version__ = "0.2.0-dev"
__maintainer__ = "Greg Caporaso"
__email__ = "gregcaporaso@gmail.com"

import os
import types
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from copy import copy
from glob import glob
from os.path import abspath, exists, isdir, isfile, split
from pyqi.core.interface import (Interface, InterfaceOption,
                                 InterfaceUsageExample, InterfaceResult, get_command_names, get_command_config)
from pyqi.core.factory import general_factory
from pyqi.core.exception import IncompetentDeveloperError
from pyqi.core.command import Parameter


def command_page_factory(module, command):
    def command_page(write):

        cmd_config = get_command_config(module, command)[0]
        print(cmd_config.inputs)
        print(cmd_config.outputs)
        print(cmd_config.param_lookup)
        print(cmd_config.usage_examples)
        print(cmd_config.CommandConstructor)

        write(command)
    return command_page

#This will generally be called from a generated command.
def start_server(port, module):
    """Start a server for the HTMLInterface on the specified port"""

    #WHAT IS THIS DOING HERE? Well I need module to be in scope for the HTTPHandler.
    #I am sure there is a better way to do this, but I just need it to work right now.
    class HTTPHandler(BaseHTTPRequestHandler):

        _unrouted = True;

        def route(self, path, output_writer):
            if self._unrouted and self.path == path:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self._unrouted = False;
                output_writer(self.wfile.write)


        def do_GET(self):

            #Why does python have no robust concept of callbacks?

            def r(write):#host.domain.tld/
                write("<ul>")
                for command in get_command_names(module):
                    write( '<li><a href="/%s">%s</a></li>'%(command, command) )
                write("</ul>")
            self.route("/", r)

            for command in get_command_names(module):
                self.route("/"+command, command_page_factory(module, command))

            
            def r(write):#host.domain.tld/help
                write("help")
            self.route("/help", r)


            if self._unrouted:
                self.send_response(404)
                self.end_headers()



        def do_POST(self):
            pass
    #End of weird scoping hack

    server = HTTPServer(("", port), HTTPHandler)
    server.serve_forever()



def stop_server():
    """Stop a running server for the HTMLInterface"""
    pass