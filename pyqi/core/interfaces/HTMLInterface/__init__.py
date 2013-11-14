#!/usr/bin/env python

#-----------------------------------------------------------------------------
# Copyright (c) 2013, The BiPy Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------

__author__ = "Evan Bolyen"
__copyright__ = "Copyright 2013, The pyqi project"
__credits__ = ["Greg Caporaso", "Daniel McDonald", "Gavin Huttley",
               "Rob Knight", "Doug Wendel", "Jai Ram Rideout",
               "Jose Antonio Navas Molina"]
__license__ = "BSD"
__version__ = "0.2.0-dev"
__maintainer__ = "Evan Bolyen"
__email__ = "ebolyen@gmail.com"

import os
import types
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from cgi import parse_header, parse_multipart, parse_qs
from copy import copy
from glob import glob
from os.path import abspath, exists, isdir, isfile, split
from pyqi.core.interface import (Interface, InterfaceOutputOption, 
                                 InterfaceUsageExample, get_command_names, get_command_config)
from pyqi.core.factory import general_factory
from pyqi.core.exception import IncompetentDeveloperError
from pyqi.core.command import Parameter

from pyqi.core.interfaces.optparse import OptparseInterface, OptparseResult, OptparseOption, OptparseUsageExample



class HTMLInterfaceResult(InterfaceOutputOption):
    def __init__(self, MIMEType=None, **kwargs):
        super(HTMLInterfaceResult, self).__init__(**kwargs)
        self.MIMEType = MIMEType;


class HTMLDownload(HTMLInterfaceResult):
    def __init__(self, FilenameLookup=None, DefaultFilename=None, MIMEType='application/octet-stream', FileExtension=None, **kwargs):
        super(HTMLDownload, self).__init__(**kwargs)
        self.FileExtension = FileExtension
        self.FilenameLookup = FilenameLookup
        self.DefaultFilename = DefaultFilename
        self.ResultType = 'download'


class HTMLPage(HTMLInterfaceResult):
    def __init__(self, MIMEType='text/html', **kwargs):
        super(HTMLPage, self).__init__(**kwargs)
        self.MIMEType = MIMEType;
        self.ResultType = 'page'
        print self.ResultType


class HTMLInterfaceOption(OptparseOption):
    pass

#Saving this in case we find a reason for usage examples
#class HTMLInterfaceUsageExample(InterfaceUsageExample):
#    def __init__(self, **kwargs):
#        super(HTMLInterfaceUsageExample, self).__init__(Ex=None, **kwargs)
#
#    def _validate_usage_example(self):
#        pass

class HTMLInterface(OptparseInterface):

    def _set_command(self, cmd):
        self._command = cmd

    def _validate_usage_examples(self, usage_examples):
        super(OptparseInterface, self)._validate_usage_examples(usage_examples)

        if len(usage_examples) > 1:
            raise IncompetentDeveloperError("There shouldn't be usage examples "
                                            "associated with this command.")

    def _the_in_validator(self, in_):
        """Validate input coming from the command line"""
        if not isinstance(in_, dict):
            raise IncompetentDeveloperError("Unsupported input '%r'. Input "
                                            "must be a dictionary." % in_)

    def _input_handler(self, in_, *args, **kwargs):
        """remormat from http post data."""
        required_opts = [opt for opt in self._get_inputs() if opt.Required]
        optional_opts = [opt for opt in self._get_inputs() if not opt.Required]

        # Build the usage and version strings
        usage = self._build_usage_lines(required_opts)
        version = 'Version: %prog ' + self._get_version()


        # If the command has required options and no input arguments were
        # provided, print the help string.
        if len(required_opts) > 0 and self.HelpOnNoArguments and len(in_) == 0:
            return usage

        # Parse our input.
        formatted_input = {}
        for key, value in in_.items():
            #HTMLInterface prepends input keys with pyqi_ as a namespacing precaution.
            #values are returned as lists, which is unhelpful.
            if(value[0] == ""):
                formatted_input[key[5:]] = None
            else:
                formatted_input[key[5:]] = value[0]


        # Build up command input dictionary. This will be passed to
        # Command.__call__ as kwargs.
        self._HTMLInterface_input = formatted_input

        cmd_input_kwargs = {}
        for option in self._get_inputs():
            if option.Parameter is not None:
                param_name = option.getParameterName()
                optparse_clean_name = option.Name

                if option.Handler is None:
                    value = self._HTMLInterface_input[optparse_clean_name]
                else:
                    value = option.Handler(
                            self._HTMLInterface_input[optparse_clean_name])

                cmd_input_kwargs[param_name] = value

        return cmd_input_kwargs

    def _build_usage_lines(self, required_options):
        """ Build the usage string from components """

        #This is almost sad, but I'm not sure theres anything else to do.
        return '<p>%s</p>' % self.CmdInstance.LongDescription

    def _output_handler(self, results):
        """Deal with things in output if we know how"""
        handled_results = {}
        download_results = []

        page_output = None
        page_seen = False

        for output in self._get_outputs():
            rk = output.Name

            if output.ResultType == 'download':
                #Set up the filename for download
                filename = "unnamed_pyqi_output"
                extension = ""
                if not output.FileExtension is None:
                    extension = output.FileExtension

                if output.FilenameLookup is None:
                    if output.DefaultFilename is None:
                        pass #the filename will remain the initialized string above
                        #alternatively, we could throw an error, but that feels drastic
                    else:
                        filename = output.DefaultFilename
                else:
                    filename = self._HTMLInterface_input[output.FilenameLookup]

                filehandle = filename + extension
                download_content = ""
                #Handle results
                if output.InputName is None:
                    download_content = output.Handler(rk, results[rk])
                else:
                    download_content = output.Handler(rk, results[rk], self._HTMLInterface_input[output.InputName])

                download_results.append({
                    'name':filehandle,
                    'contents':download_content
                    })

            elif output.ResultType == 'page':
                if not page_seen:
                    page_seen = True
                    if output.InputName is None:
                        page_output = {
                            'mime_type':output.MIMEType,
                            'contents':output.Handler(rk, results[rk])
                        } 
                    else:
                        page_output = {
                            'mime_type': output.MIMEType, 
                            'contents': output.Handler(rk, results[rk], self._HTMLInterface_input[output.InputName])
                        }
                else:
                    raise IncompetentDeveloperError("It is not possible to display multiple pages.")
            else:
                raise IncompetentDeveloperError("Unkown output object.")

        return page_output, download_results
        

def HTMLInterface_main():
    pass

def HTMLInterface_factory(command_constructor, usage_examples, inputs, outputs,
                     version):
    return general_factory(command_constructor, usage_examples, inputs,
                           outputs, version, HTMLInterface)

def get_cmd_obj(cmd_cfg_mod, cmd):
    """Get a ``Command`` object"""
    cmd_cfg,_ = get_command_config(cmd_cfg_mod, cmd)
    cmd_obj = HTMLInterface_factory(cmd_cfg.CommandConstructor, cmd_cfg.usage_examples, 
                            cmd_cfg.inputs, cmd_cfg.outputs,
                            cmd_cfg.__version__)()
    #The interface needs to know what command it is, because %prog doesn't mean anything without optparse
    cmd_obj._set_command(cmd)
    return cmd_obj



def command_page_factory(module, command):
    



#    def descriptionator(usage):
#        returnString = '<div class="usage">'
#        returnString += '<h3>%s</h3>' % usage.ShortDesc
#        returnString += '<div class="longDesc">%s</div>' % usage.LongDesc
#        returnString += '<div class="ex">%s</div>' % usage.Ex
#        return returnString + '</div>'

    def input_map(i):

        default_input = '<tr><td class="right">%s</td><td><input type="text" name="pyqi_%s" /></td></tr><tr><td></td><td>%s</td></tr><tr><td>&nbsp;</td></tr>'

        input_switch = {
        'none':default_input,
        'str':default_input,
        'int':default_input,
        'long':default_input,
        'float':default_input,
        'complex':default_input,
        'choice':default_input,
        'multiple_choice':default_input,
        'upload_file':default_input,
        'new_filepath':default_input
        }

        iType = i.Type

        if(type(iType) is not str):
            if(type("") is type(iType)):
                iType = 'str'
            elif(type(1) is type(iType)):
                iType = 'int'
            elif(type(None) is type(iType)):
                iType = 'none'

        return input_switch[iType] % ( ('<span class="required">*</span>' + i.Name if i.Required  else i.Name), i.Name, i.Help)
        



    def command_page(write):


        templateHead = '<!DOCTYPE html><html><head><title>%s</title>'
        styles = '<style>'

        # It would be better if I made a routing system for all files in assets
        with open(__file__[:-12]+"/assets/style.css", "U") as f:
            styles += f.read()
        #but until then, the above works.

        styles +='</style>'
        templateHead += styles + '</head><body><h1>%s</h1><div id="content">'
        templateClose = '</div></body></html>'


        cmd_obj = get_cmd_obj(module, command)
        write(templateHead % (command, command))

        write(cmd_obj._build_usage_lines([opt for opt in cmd_obj._get_inputs() if opt.Required]))

        write('<p>An (<span class="required">*</span>) denotes a required field.</p>')

        write('<form method="POST">')
        write('<table>')
        for i in cmd_obj._get_inputs():
            write(input_map(i))
        write('</table>')
        write('<input type="submit">')
        write('</form>')

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

        def download_route(self, path, module, command, postvars):
            if self._unrouted and self.path == path:
                cmd_obj = get_cmd_obj(module, command)
                result = cmd_obj(postvars)
                
                if result[0] is None:


                    filename = result[1][0]['name']
                    

                    self.send_response(200)


                    self.send_header('Content-disposition', 'attachment; filename=' + filename)
                    self.send_header('Content-type', 'application/octet-stream')
                    self.end_headers()
                    self.wfile.write(result[1][0]['contents'])
                else:
                    self.send_response(200)
                    self.send_header('Content-type', result[0]['mime_type'])
                    self.end_headers()
                    self.wfile.write(result[0]['contents'])


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
                self.download_route("/"+command, module, command, postvars)



    return HTTPHandler




#This will generally be called from a generated command.
def start_server(port, module):
    """Start a server for the HTMLInterface on the specified port"""

    server = HTTPServer(("", port), HTTPHandler_factory(module))
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass

