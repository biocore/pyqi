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


class HTMLInterfaceOption(OptparseOption):
    pass

class HTMLInterfaceUsageExample(OptparseUsageExample):
    pass

class HTMLInterface(OptparseInterface):


    def _validate_usage_examples(self, usage_examples):
        super(OptparseInterface, self)._validate_usage_examples(usage_examples)

        if len(usage_examples) < 1:
            raise IncompetentDeveloperError("There are no usage examples "
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
        line1 = 'usage: %prog [options] ' + \
                '{%s}' % ' '.join(['%s %s' % (str(rp),rp.Name.upper())
                                   for rp in required_options])

        formatted_usage_examples = []
        for usage_example in self._get_usage_examples():
            short_description = usage_example.ShortDesc.strip(':').strip()
            long_description = usage_example.LongDesc.strip(':').strip()
            example = usage_example.Ex.strip()

            if short_description:
                formatted_usage_examples.append('%s: %s\n %s' % 
                                                (short_description,
                                                 long_description, example))
            else:
                formatted_usage_examples.append('%s\n %s' %
                                                (long_description,example))

        formatted_usage_examples = '\n\n'.join(formatted_usage_examples)

        lines = (line1,
                 '', # Blank line
                 self.OptionalInputLine,
                 self.RequiredInputLine,
                 '', # Blank line
                 self.CmdInstance.LongDescription,
                 '', # Blank line
                 'Example usage: ',
                 'Print help message and exit',
                 ' %prog -h\n',
                 formatted_usage_examples)

        return '\n'.join(lines)

    def _output_handler(self, results):
        """Deal with things in output if we know how"""
        handled_results = {}
        download_results = []

        page_output = ""
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
                    'contents':download_results
                    })

            elif self.ResultType == 'page':
                if not page_seen:
                    page_seen = True
                    if output.InputName is None:
                        page_output = output.Handler(rk, results[rk])
                    else:
                        page_output = output.Handler(rk, results[rk], self._HTMLInterface_input[output.InputName])
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
    cmd_cfg, _ = get_command_config(cmd_cfg_mod, cmd)
    return HTMLInterface_factory(cmd_cfg.CommandConstructor, cmd_cfg.usage_examples, 
                            cmd_cfg.inputs, cmd_cfg.outputs,
                            cmd_cfg.__version__)



def command_page_factory(module, command):
    
    templateHead = '<!DOCTYPE html><html><head><title>%s</title></head><body><h1>%s</h1>'
    templateClose = '</body></html>'



#    def descriptionator(usage):
#        returnString = '<div class="usage">'
#        returnString += '<h3>%s</h3>' % usage.ShortDesc
#        returnString += '<div class="longDesc">%s</div>' % usage.LongDesc
#        returnString += '<div class="ex">%s</div>' % usage.Ex
#        return returnString + '</div>'

    def input_map(i):
        input_switch = {
        'none':'%s:<input type="text" name="pyqi_%s" />%s', #THIS IS BAD AND I SHOULD FEEL BAD
        'str':'%s:<input type="text" name="pyqi_%s" />%s',
        'int':'%s:<input type="text" name="pyqi_%s" />%s',
        'long':'%s:<input type="text" name="pyqi_%s" />%s',
        'float':'%s:<input type="text" name="pyqi_%s" />%s',
        'complex':'%s:<input type="text" name="pyqi_%s" />%s',
        'choice':'%s:<input type="text" name="pyqi_%s" />%s',
        'multiple_choice':'%s:<input type="text" name="pyqi_%s" />%s',
        'upload_file':'%s:<input type="text" name="pyqi_%s" />%s',
        'new_filepath':'%s:<input type="text" name="pyqi_%s" />%s'
        }

        iType = i.Type

        if(type(iType) is not str):
            if(type("") is type(iType)):
                iType = 'str'
            elif(type(1) is type(iType)):
                iType = 'int'
            elif(type(None) is type(iType)):
                iType = 'none'

        returnString = '<div class="input">'
        returnString += input_switch[iType] % (i.Name, i.Name, i.Help)
        


        return returnString + '</div>'

    def command_page(write):

        cmd_obj = get_cmd_obj(module, command)()
        write(templateHead % (command, command))

        write(cmd_obj._build_usage_lines([opt for opt in cmd_obj._get_inputs() if opt.Required]))

        write('<form method="POST">')
        for i in cmd_obj._get_inputs():
            write(input_map(i))
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
                cmd_obj = get_cmd_obj(module, command)()
                result = cmd_obj(postvars)
              
                filename = result[1][0]['name']
                print filename

                self.send_response(200)
                self.send_header('Content-disposition', 'attachment; filename=' + filename)
                self.send_header('Content-type', 'application/octet-stream')
                self.end_headers()
                self.wfile.write(result[1][0]['contents'])


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
    server.serve_forever()

