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
__credits__ = ["Evan Bolyen", "Greg Caporaso", "Daniel McDonald", "Jai Ram Rideout",]
__license__ = "BSD"
__version__ = "0.2.0-dev"
__maintainer__ = "Evan Bolyen"
__email__ = "ebolyen@gmail.com"

import os
import types
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from cgi import parse_header, parse_multipart, parse_qs, FieldStorage
from copy import copy
from glob import glob
from os.path import abspath, exists, isdir, isfile, split
from pyqi.core.interface import (Interface, InterfaceOutputOption, InterfaceInputOption,
                                 InterfaceUsageExample, get_command_names, get_command_config)
from pyqi.core.factory import general_factory
from pyqi.core.exception import IncompetentDeveloperError
from pyqi.core.command import Parameter



class HTMLInterfaceResult(InterfaceOutputOption):
    def __init__(self, MIMEType=None, **kwargs):
        super(HTMLInterfaceResult, self).__init__(**kwargs)
        self.MIMEType = MIMEType;


class HTMLDownload(HTMLInterfaceResult):
    def __init__(self, FileExtension=None, FilenameLookup=None, DefaultFilename=None, MIMEType='application/octet-stream', **kwargs):
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


class HTMLInterfaceOption(InterfaceInputOption):
    
    def __init__(self, Choices=None, **kwargs):
        self.Choices = Choices
        super(HTMLInterfaceOption, self).__init__(**kwargs)
        

    accepted_types = [
            "str",
            "none",
            "int",
            "float",
            "long",
            "complex",
            "multiple_choice",
            "upload_file"
        ]

    def _validate_option(self):

        # convert python type objets to strings so they can be processed later
        if self.Type is str:
            self.Type = "str"
        elif self.Type is None:
            self.Type = "none"
        elif self.Type is int:
            self.Type = "int"
        elif self.Type is float:
            self.Type = "float"
        elif self.Type is long:
            self.Type = "long"
        elif self.Type is complex:
            self.Type = "complex"

        unkown_type = True
        for t in self.accepted_types:
            if self.Type == t:
                unkown_type = False
                break

        if unkown_type:
            raise IncompetentDeveloperError("Unsupported Type in HTMLInterfaceOption: %s" % str(self.Type))

        #From optparse's __init__.py, inside class PyqiOption
        if self.Type == "multiple_choice":
            if self.Choices is None:
                raise OptionError(
                    "must supply a list of mchoices for type '%s'" % self.type, self)
            elif type(self.Choices) not in (types.TupleType, types.ListType):
                raise OptionError(
                    "choices must be a list of strings ('%s' supplied)"
                    % str(type(self.Choices)).split("'")[1], self)
        elif self.Choices is not None:
            raise OptionError(
                "must not supply Choices for type %r" % self.type, self)


#Saving this in case we find a reason for usage examples

#class HTMLInterfaceUsageExample(InterfaceUsageExample):
#    def __init__(self, **kwargs):
#        super(HTMLInterfaceUsageExample, self).__init__(Ex=None, **kwargs)


class HTMLInterface(Interface):

    #Override
    def __call__(self, in_, *args, **kwargs):
        self._the_in_validator(in_)
        cmd_input, errors = self._input_handler(in_, *args, **kwargs)
        if len(errors) == 0:        
            cmd_result = self.CmdInstance(**cmd_input)
            self._the_out_validator(cmd_result)       
            return self._output_handler(cmd_result)
        else:
            return {
                'type': 'error',
                'errors': errors
            }

    def _set_command(self, cmd):
        self._command = cmd

    def _validate_usage_examples(self, usage_examples):
        super(HTMLInterface, self)._validate_usage_examples(usage_examples)

        if len(usage_examples) > 1:
            raise IncompetentDeveloperError("There shouldn't be usage examples "
                                            "associated with this command.")

    def _the_in_validator(self, in_):
        """Validate input coming from the postvars"""
        if not isinstance(in_, FieldStorage):
            raise IncompetentDeveloperError("Unsupported input '%r'. Input "
                                            "must be FieldStorage." % in_)


    def _the_out_validator(self, out_):
        """Validate output coming from the command call"""
        if not isinstance(out_, dict):
            raise IncompetentDeveloperError("Unsupported result '%r'. Result "
                                            "must be a dict." % out_)

    def _cast_as(self, postdata, t):
        """Casts str(postdata.value) as an object of the correct type 't'"""
        if postdata is None:
            return None

        if t == "str" or t is str:  
            return str(postdata.value)
        if t == "int" or t is int:
            return int(postdata.value)
        if t == "float" or t is float:
            return float(postdata.value)
        if t == "long" or t is long:
            return long(postdata.value)
        if t == "complex" or t is complex:
            return complex(postdata.value)
        if t == "upload_file":
            return postdata.file.read()

        return postdata.value



    def _input_handler(self, in_, *args, **kwargs):
        """reformat from http post data."""

        errors = []

        # Parse our input.
        formatted_input = {}

        for key in in_.keys():
            mod_key = key[5:]
            formatted_input[mod_key] = in_[key]
            if formatted_input[mod_key].value == "":
                formatted_input[mod_key] = None


        cmd_input_kwargs = {}
        for option in self._get_inputs():
            if option.Name not in formatted_input:
                formatted_input[option.Name] = None


            if option.Required and formatted_input[option.Name] is None:
                errors.append("Error: %s is required." % option.Name)
                continue
            try:
                formatted_input[option.Name] = self._cast_as(formatted_input[option.Name], 
                                                            option.Type)
            except (ValueError, TypeError):
                errors.append("Error: %s must be type %s" % (option.Name, option.Type) );


            if option.Parameter is not None:
                param_name = option.getParameterName()
                optparse_clean_name = option.Name

                if option.Handler is None:
                    value = formatted_input[optparse_clean_name]
                else:
                    value = option.Handler(formatted_input[optparse_clean_name])

                cmd_input_kwargs[param_name] = value

        self._HTMLInterface_input = formatted_input
        return cmd_input_kwargs, errors

    def _build_usage_lines(self, required_options):
        """ Build the usage string from components """

        #This is almost sad, but I'm not sure theres anything else to do.
        return '<p>%s</p>' % self.CmdInstance.LongDescription

    def _output_handler(self, results):
        """Deal with things in output if we know how"""


        output = self._get_outputs()
        if type(output) is list:
            if len(output) > 1:
                raise IncompetentDeveloperError("There can be only one... output")
            else:
                output = output[0]


        rk = output.Name

        if output.ResultType == 'download':
            #Set up the filename for download
            filename = "unnamed_pyqi_output"
            extension = ""
            if not output.FileExtension is None:
                extension = output.FileExtension

            if output.FilenameLookup is None:
                if output.DefaultFilename is not None:
                    filename = output.DefaultFilename
            else:
                lookup_filename = self._HTMLInterface_input[output.FilenameLookup]
                if lookup_filename is not None:
                    filename = lookup_filename

            filehandle = filename + extension
            download_content = ""
            #Handle results
            if output.InputName is None:
                download_content = output.Handler(rk, results[rk])
            else:
                download_content = output.Handler(rk, results[rk], self._HTMLInterface_input[output.InputName])

            return {
                'type':'download',
                'filename':filehandle,
                'contents':download_content
                }

        elif output.ResultType == 'page':

            if output.InputName is None:
                handled_results = output.Handler(rk, results[rk])
            else:
                handled_results = output.Handler(rk, results[rk], self._HTMLInterface_input[output.InputName])
        
            return {
                'type':'page',
                'mime_type':output.MIMEType,
                'contents':handled_results
            }

        else:
            raise IncompetentDeveloperError("Output must subclass HTMLPage or HTMLDownload")


    def _input_map(self, i):

        def string_input():
            html_input = '<tr><td class="right">%s</td>' % ('<span class="required">*</span>' + i.Name if i.Required  else i.Name)
            html_input += '<td><input type="text" name="pyqi_%s" /></td></tr>' % i.Name
            html_input += '<tr><td></td><td>%s</td></tr><tr><td>&nbsp;</td></tr>' % i.Help
            return html_input

        def number_input():
            html_input =  '<tr><td class="right">%s</td>' 
            html_input += '<td><input type="number" name="pyqi_%s" /></td></tr>' 
            html_input += '<tr><td></td><td>%s</td></tr><tr><td>&nbsp;</td></tr>'
            return html_input
            
        def mchoice_input():
            html_input = '<tr><td class="right">%s</td><td>' % ('<span class="required">*</span>' + i.Name if i.Required  else i.Name)
            for choice in i.Choices:
                html_input += '%s<input type="radio" name="pyqi_%s" value="%s" />' % (choice, i.Name, choice)

            html_input += '</td></tr><tr><td></td><td>%s</td></tr><tr><td>&nbsp;</td></tr>' % i.Help
            return html_input
            
        def upload_input():
            html_input =  '<tr><td class="right">%s</td>' % ('<span class="required">*</span>' + i.Name if i.Required  else i.Name)
            html_input += '<td><input type="file" name="pyqi_%s" /></td></tr>' % i.Name
            html_input += '<tr><td></td><td>%s</td></tr><tr><td>&nbsp;</td></tr>' % i.Name
            return html_input
            

        input_switch = {
            "str": string_input,
            "none": string_input,
            "int": number_input,
            "float": number_input,
            "long": number_input,
            "complex": string_input,
            "multiple_choice": mchoice_input,
            "upload_file": upload_input
        }


        return input_switch[i.Type]()

    def command_page_writer(self, write, errors):


        templateHead = '<!DOCTYPE html><html><head><title>%s</title>'
        styles = '<style>'

        # It would be better if I made a routing system for all files in assets
        # This would also probably be done in tandem with the proper seperation of server and execution.
        with open(__file__[:-12]+"/assets/style.css", "U") as f:
            styles += f.read()
        # but until then, the above works.

        styles +='</style>'
        templateHead += styles + '</head><body><h1>%s</h1><div id="content">'
        templateClose = '</div></body></html>'


        write(templateHead % (self._command, self._command))
        write(self._build_usage_lines([opt for opt in self._get_inputs() if opt.Required]))

        write('<p>An (<span class="required">*</span>) denotes a required field.</p>')

        for e in errors:
            write('<div class="error">%s</div>' % e)

        write('<form method="POST" enctype="multipart/form-data">')
        write('<table>')
        for i in self._get_inputs():
            write(self._input_map(i))
        write('</table>')
        write('<input type="submit">')
        write('</form>')

        write('</div></body></html>')
        


def HTMLInterface_factory(command_constructor, usage_examples, inputs, outputs,
                     version):
    return general_factory(command_constructor, usage_examples, inputs,
                           outputs, version, HTMLInterface)

def get_cmd_obj(cmd_cfg_mod, cmd):
    """Get a ``Command`` object"""
    cmd_cfg,_ = get_command_config(cmd_cfg_mod, cmd)
    cmd_class = HTMLInterface_factory(cmd_cfg.CommandConstructor, cmd_cfg.usage_examples, 
                            cmd_cfg.inputs, cmd_cfg.outputs,
                            cmd_cfg.__version__)
    cmd_obj = cmd_class()
    #The interface needs to know what command it is
    cmd_obj._set_command(cmd)
    return cmd_obj







def HTMLInterfaceHTTPHandler_factory(module):
    """Return a subclassed BaseHTTPRequestHandler with module in scope."""

    module_commands = get_command_names(module)

    class HTMLInterfaceHTTPHandler(BaseHTTPRequestHandler):

        _unrouted = True;

        def route(self, path, output_writer):
            if self._unrouted and self.path == path:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output_writer(self.wfile.write)
                
                self.wfile.close()
                self._unrouted = False;

        def command_route(self, command):
            if self._unrouted and self.path == "/" + command:
                cmd_obj = get_cmd_obj(module, command)

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                cmd_obj.command_page_writer(self.wfile.write, [])
                
                self.wfile.close()
                self._unrouted = False

        def post_route(self, command, postvars):
            if self._unrouted and self.path == "/" + command:
                cmd_obj = get_cmd_obj(module, command)
                result = cmd_obj(postvars)
                
                if result['type'] == 'error':
                    self.send_response(400)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    cmd_obj.command_page_writer(self.wfile.write, result['errors'])

                elif result['type'] == 'page':       
                    self.send_response(200)
                    self.send_header('Content-type', result['mime_type'])
                    self.end_headers()
                    self.wfile.write(result['contents'])

                elif result['type'] == 'download':
                    self.send_response(200)
                    self.send_header('Content-type', 'application/octet-stream')
                    self.send_header('Content-disposition', 'attachment; filename=' + result['filename'])
                    self.end_headers()
                    self.wfile.write(result['contents'])
                    
                self.wfile.close()
                self._unrouted = False

        def end_routes(self):
            if self._unrouted:
                self.send_response(404)
                self.end_headers()

                self.wfile.close()
                self._unrouted = False

        def do_GET(self):

            #Why does python have no robust concept of anonymous functions? Is a function keyword so inelegant?

            def r(write):#host.domain.tld/
                write("<ul>")
                for command in module_commands:
                    write( '<li><a href="/%s">%s</a></li>'%(command, command) )
                write("</ul>")
            self.route("/", r)
            self.route("/index", r)
            self.route("/home", r)

            def r(write):#host.domain.tld/help
                write("This is still a very in development interface, there is no help.")
            self.route("/help", r)

            for command in module_commands:
                self.command_route(command)

            self.end_routes()

        def do_POST(self):

            postvars = FieldStorage(fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD':'POST',
                        'CONTENT_TYPE':self.headers['Content-Type']})

            for command in module_commands:
                self.post_route(command, postvars)

            self.end_routes()


    return HTMLInterfaceHTTPHandler


#This will generally be called from a generated command.
def start_server(port, module):
    """Start a server for the HTMLInterface on the specified port"""

    interface_server = HTTPServer(("", port), HTMLInterfaceHTTPHandler_factory(module))

    try:
        interface_server.serve_forever()

    except KeyboardInterrupt:
        return "--Finished serving HTMLInterface--"

