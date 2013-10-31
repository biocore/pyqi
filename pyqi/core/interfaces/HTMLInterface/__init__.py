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
from cgi import parse_header, parse_multipart, parse_qs
from copy import copy
from glob import glob
from os.path import abspath, exists, isdir, isfile, split
from pyqi.core.interface import (Interface, InterfaceOption,
                                 InterfaceUsageExample, InterfaceResult, get_command_names, get_command_config)
from pyqi.core.factory import general_factory
from pyqi.core.exception import IncompetentDeveloperError
from pyqi.core.command import Parameter

from pyqi.core.interfaces.optparse import OptparseInterface, OptparseOption


class HTMLResult(InterfaceOption):
    def _validate_result(self):
        pass

class HTMLOption(OptparseOption):
    pass

class HTMLInterface(OptparseInterface):
    pass


def command_output_factory(module, command, POST):
    
    def command_out(write):
        write(POST)

    return command_out
def command_page_factory(module, command):
    
    cmd_config = get_command_config(module, command)[0]
    
    templateHead = '<!DOCTYPE html><html><head><title>%s</title></head><body><h1>%s</h1>'
    templateClose = '</body></html>'

    def descriptionator(usage):
        returnString = '<div class="usage">'
        returnString += '<h3>%s</h3>' % usage.ShortDesc
        returnString += '<div class="longDesc">%s</div>' % usage.LongDesc
        returnString += '<div class="ex">%s</div>' % usage.Ex
        return returnString + '</div>'

    def input_map(i):
        input_switch = {
        'str':'%s:<input type="text" name="pyqi_%s" />%s',
        'int':'%s:<input type="text" name="pyqi_%s" />%s',
        'long':'%s:<input type="text" name="pyqi_%s" />%s',
        'float':'%s:<input type="text" name="pyqi_%s" />%s',
        'complex':'%s:<input type="text" name="pyqi_%s" />%s',
        'choice':'%s:<input type="text" name="pyqi_%s" />%s',
        'multiple_choice':'%s:<input type="text" name="pyqi_%s" />%s',
        'upload_file':'%s:<input type="text" name="pyqi_%s" />%s'
        }

        iType = i.InputType

        if(type(iType) is not str):
            if(type("") is iType):
                iType = 'str'
            elif(type(1) is iType):
                iType = 'int'

        returnString = '<div class="input">'
        returnString += input_switch[iType] % (i.Name, i.Name, i.Help)
        


        return returnString + '</div>'

    def command_page(write):

        write(templateHead % (command, command))

        for usage in cmd_config.usage_examples:
            write(descriptionator(usage))

        write('<form method="POST">')
        for i in cmd_config.inputs:
            write(input_map(i))
        write('<input type="submit">')
        write('</form>')

        #print(cmd_config.outputs)
        #print(cmd_config.param_lookup)
        #print(cmd_config.CommandConstructor)
        write(templateClose)

    return command_page

def HTTPHandler_factory(module):

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

            #Why does python have no robust concept of anonymous functions? Is a function keyword so inelegant?

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
                self.wfile.close()

        def do_POST(self):

            ctype, pdict = parse_header(self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                postvars = parse_multipart(self.rfile, pdict)
            elif ctype == 'application/x-www-form-urlencoded':
                length = int(self.headers.getheader('content-length'))
                postvars = parse_qs(self.rfile.read(length), keep_blank_values=1)
            else:
                postvars = {}

            for command in get_command_names(module):
                self.route("/"+command, command_output_factory(module, command, postvars))


    return HTTPHandler




#This will generally be called from a generated command.
def start_server(port, module):
    """Start a server for the HTMLInterface on the specified port"""

    server = HTTPServer(("", port), HTTPHandler_factory(module))
    server.serve_forever()

