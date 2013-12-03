#!/usr/bin/env python

#-----------------------------------------------------------------------------
# Copyright (c) 2013, The BiPy Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------

__credits__ = ["Evan Bolyen", "Jai Ram Rideout", "Daniel McDonald",
    "Greg Caporaso"]

import os
import types
import os.path
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
from pyqi.util import get_version_string

class HTMLResult(InterfaceOutputOption):
    """Base class for results for an HTML config file"""
    def __init__(self, MIMEType=None, **kwargs):
        super(HTMLResult, self).__init__(**kwargs)
        if MIMEType is None:
            raise IncompetentDeveloperError("A valid MIMEType must be provided")
        self.MIMEType = MIMEType;

class HTMLDownload(HTMLResult):
    """Result class for downloading a file from the server"""
    def __init__(self, FileExtension=None, FilenameLookup=None, DefaultFilename=None, 
            MIMEType='application/octet-stream', **kwargs):
        super(HTMLDownload, self).__init__(MIMEType=MIMEType, **kwargs)
        self.FileExtension = FileExtension
        self.FilenameLookup = FilenameLookup
        self.DefaultFilename = DefaultFilename

class HTMLPage(HTMLResult):
    """Result class for displaying a page for an HTML config file"""
    def __init__(self, MIMEType='text/html', **kwargs):
        super(HTMLPage, self).__init__(MIMEType=MIMEType, **kwargs)

class HTMLInputOption(InterfaceInputOption):
    """Define an input option for an HTML config file"""
    _type_handlers = {
        None: lambda: None,
        str: lambda x: str(x.value),
        bool: lambda x: x.value == "True",
        int: lambda x: int(x.value),
        float: lambda x: float(x.value),
        long: lambda x: long(x.value),
        complex: lambda x: complex(x.value),
        "upload_file": lambda x: x.file.read(),
        "multiple_choice": lambda x: x.value
    }

    def __init__(self, Choices=None, Type=str, **kwargs):
        self.Choices = Choices
        super(HTMLInputOption, self).__init__(Type=Type, **kwargs)
        if Type == bool:
            self.Choices = [True, False]

    def cast_value(self, postdata):
        """Casts str(postdata.value) as an object of the correct type"""
        return self._type_handlers[self.Type](postdata) if postdata is not None else None

    def get_html(self, prefix, value=""):
        """Return the HTML needed for user input given a default value"""
        if (not value) and (self.Default is not None):
            value = self.Default
            
        input_name = prefix + self.Name
        string_input = lambda: '<input type="text" name="%s" value="%s"/>' % (input_name, value)
        number_input = lambda: '<input type="number" name="%s" value="%s"/>' % (input_name, value)

        #html input files cannot have default values. 
        #If the html interface worked as a data service, this would be possible as submit would be ajax.
        upload_input = lambda: '<input type="file" name="%s" />' % input_name
        mchoice_input = lambda: ''.join(
            [ ('(%s<input type="radio" name="%s" value="%s" %s/>)' 
                    % (choice, input_name, choice, 'checked="true"' if value == choice else '')) 
                for choice in self.Choices ]
        )

        input_switch = {
            None: string_input,
            str: string_input,
            bool: mchoice_input,
            int: number_input,
            float: number_input,
            long: number_input,
            complex: string_input,
            "multiple_choice": mchoice_input,
            "upload_file": upload_input
        }

        return ''.join(['<tr><td class="right">',
                        ('<span class="required">*</span>' + self.Name) if self.Required else self.Name,
                       '</td><td>',
                       input_switch[self.Type](),
                       '</td></tr><tr><td></td><td>',
                        self.Help,
                       '</td></tr><tr><td>&nbsp;</td></tr>'
                       ])
   
    def _validate_option(self):
        if self.Type not in self._type_handlers:
            raise IncompetentDeveloperError("Unsupported Type in HTMLInputOption: %s" % self.Type)

        #From optparse's __init__.py, inside class PyqiOption
        if self.Type == "multiple_choice":
            if self.Choices is None:
                raise IncompetentDeveloperError(
                    "must supply a list of Choices for type '%s'" % self.type, self)
            elif type(self.Choices) not in (_type_handlers.TupleType, types.ListType):
                raise IncompetentDeveloperError(
                    "choices must be a list of strings ('%s' supplied)"
                    % str(type(self.Choices)).split("'")[1], self)
        elif self.Choices is not None:
            raise IncompetentDeveloperError("must not supply Choices for type %r" % self.type, self)

class HTMLInterface(Interface):
    """An HTML interface"""
    #Relative mapping wasn't working on a collegue's MacBook when pyqi was run outside of it's directory
    #Until I understand why that was the case and how to fix it, I am putting the style css here. 
    #This is not a permanent solution.
    css_style = '\n'.join([
        'html, body {',
        '   margin: 0px;',
        '   padding: 0px;',
        '   font-family: "Trebuchet MS",sans-serif;',
        '}',

        '#content {',
        '   padding-left: 20px;',
        '}',

        'h1 {',
        '   background-color: rgb(242, 242, 242);',
        '   font-weight: normal;',
        '   color: rgb(32, 67, 92);',
        '   border-bottom: 2px solid rgb(204, 204, 204);',

        '   margin: 0px;',
        '   padding: 3px 0px 3px 10px;',
        '}',

        '.right {',
        '    text-align: right;',
        '}',

        '.required {',
        '    color: red;',
        '}',

        '.error {',
        '    color: red;',
        '    border: 1px solid red;',
        '    padding: 5px;',
        '    background: pink;',
        '}',

        'ul {',
        '    list-style-type: none;',
        '    font-size: 20px;',
        '    float: left;',
        '}',
        'li {',
        '    padding: 5px;',
        '    margin-bottom:5px;',
        '    border: 1px solid rgb(204, 204, 204);',
        '    background: rgb(242, 242, 242);',
        '}',

        'a, a:visited, a:active{',
        '    color: rgb(32, 67, 92);',
        '}'
      ])

    def __init__(self, input_prefix="pyqi_", **kwargs):
        self._html_input_prefix = input_prefix
        self._html_interface_input = {}
        super(HTMLInterface, self).__init__(**kwargs)
    
    #Override
    def __call__(self, in_, *args, **kwargs):
        self._the_in_validator(in_)
        cmd_input, errors = self._input_handler(in_, *args, **kwargs)
        if errors:
            return {
                    'type': 'error',
                    'errors': errors
                }
        else:        
            cmd_result = self.CmdInstance(**cmd_input)
            self._the_out_validator(cmd_result)       
            return self._output_handler(cmd_result)

    def _validate_inputs_outputs(self, inputs, outputs):
        super(HTMLInterface, self)._validate_inputs_outputs(inputs, outputs)  
        
        if len(outputs) > 1:
            raise IncompetentDeveloperError("There can be only one... output")

        if not ( isinstance(outputs[0], HTMLPage) or isinstance(outputs[0], HTMLDownload) ):
            raise IncompetentDeveloperError("Output must subclass HTMLPage or HTMLDownload")

    def _validate_usage_examples(self, usage_examples):
        super(HTMLInterface, self)._validate_usage_examples(usage_examples)

        if usage_examples:
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

    def _input_handler(self, in_, *args, **kwargs):
        """reformat from http post data."""

        errors = []

        # Parse our input.
        formatted_input = {}

        for key in in_:
            mod_key = key[ len(self._html_input_prefix): ] 
            formatted_input[mod_key] = in_[key]
            if not formatted_input[mod_key].value:
                formatted_input[mod_key] = None

        cmd_input_kwargs = {}
        for option in self._get_inputs():
            if option.Name not in formatted_input:
                formatted_input[option.Name] = None

            if option.Required and formatted_input[option.Name] is None:
                errors.append("Error: %s is required." % option.Name)
                continue
            try:
                formatted_input[option.Name] = option.cast_value(formatted_input[option.Name])

            except (ValueError, TypeError):
                errors.append("Error: %s must be type %s" % (option.Name, option.Type) );

            if option.Parameter is not None:
                param_name = option.getParameterName()

                if option.Handler is None:
                    value = formatted_input[option.Name]
                else:
                    value = option.Handler(formatted_input[option.Name])

                cmd_input_kwargs[param_name] = value

        self._html_interface_input = formatted_input
        return cmd_input_kwargs, errors

    def _build_usage_lines(self, required_options):
        """ Build the usage string from components """
        return '<p class="usage_example">%s</p>' % self.CmdInstance.LongDescription

    def _output_download_handler(self, output, handled_results):
        """Handle the output for type: 'download' """
        #Set up the filename for download
        filename = "unnamed_pyqi_output"
        extension = ""
        if output.FileExtension is not None:
            extension = output.FileExtension

        if output.FilenameLookup is None:
            if output.DefaultFilename is not None:
                filename = output.DefaultFilename
        else:
            lookup_filename = self._html_interface_input[output.FilenameLookup]
            if lookup_filename is not None:
                filename = lookup_filename

        filehandle = filename + extension

        return {
            'type':'download',
            'filename':filehandle,
            'contents':handled_results
            }

    def _output_page_handler(self, output, handled_results):
        """Handle the output for type: 'page' """
        return {
            'type':'page',
            'mime_type':output.MIMEType,
            'contents':handled_results
        }

    def _output_handler(self, results):
        """Deal with things in output if we know how"""

        output = self._get_outputs()[0]

        rk = output.Name
        if output.Handler is not None:
            if output.InputName is None:
                handled_results = output.Handler(rk, results[rk])
            else:
                handled_results = output.Handler(rk, results[rk], 
                    self._html_interface_input[output.InputName])
        else:
            handled_results = results[rk]
    
        if isinstance(output, HTMLDownload):
            return self._output_download_handler(output, handled_results)

        elif isinstance(output, HTMLPage):
            return self._output_page_handler(output, handled_results)

    def command_page_writer(self, write, errors, postvars):
        """Write an HTML page which contains a form for user input"""
        write('<!DOCTYPE html><html><head><title>%s</title>' % self.CommandName)
        write('<style>')

        write(self.css_style)

        write('</style>')
        write('</head><body><h1>%s</h1><div id="content">' % self.CommandName)

        write(self._build_usage_lines([opt for opt in self._get_inputs() if opt.Required]))

        write('<p>An (<span class="required">*</span>) denotes a required field.</p>')

        for e in errors:
            write('<div class="error">%s</div>' % e)

        write('<form method="POST" enctype="multipart/form-data">')
        write('<table>')
        for i in self._get_inputs():
            full_name = self._html_input_prefix + i.Name
            if full_name in postvars and i.Type is not 'upload_file':
                default = i.cast_value(postvars[full_name])
                write(i.get_html(self._html_input_prefix, value=default))
            else:
                write(i.get_html(self._html_input_prefix))

        write('</table>')
        write('<input type="submit">')
        write('</form>')

        write('</div></body></html>')

def html_interface_factory(command_constructor, usage_examples, inputs, outputs,
                     version, command_name):
    interface_class = general_factory(command_constructor, usage_examples, inputs,
                           outputs, version, HTMLInterface)
    interface_class.CommandName = command_name
    return interface_class

def get_cmd_obj(cmd_cfg_mod, cmd):
    """Get a ``Command`` object"""
    cmd_cfg,_ = get_command_config(cmd_cfg_mod, cmd)
    version_str = get_version_string(cmd_cfg_mod)
    cmd_class = html_interface_factory(cmd_cfg.CommandConstructor, [],
                            cmd_cfg.inputs, cmd_cfg.outputs, version_str, cmd)
    cmd_obj = cmd_class()
    return cmd_obj

def get_http_handler(module):
    """Return a subclassed BaseHTTPRequestHandler with module in scope."""
    module_commands = get_command_names(module)

    class HTMLInterfaceHTTPHandler(BaseHTTPRequestHandler):
        """Handle incoming HTTP requests"""

        def __init__(self, *args, **kwargs):
            self._unrouted = True
            #Apparently this is an 'oldstyle' class, which doesn't allow the use of super()
            BaseHTTPRequestHandler.__init__(self, *args, **kwargs)

        def index(self, write):
            write("<html><head><title>")
            write("PyQi: " + module)
            write("</title>")
            write("<style>")
            write(HTMLInterface.css_style)
            write("</style>")
            write("</head><body>")
            write("<h1>Available Commands:</h1>")
            write("<ul>")
            for command in module_commands:
                write( '<li><a href="/%s">%s</a></li>'%(command, command) )
            write("</ul>")
            write("</body></html>")

        def route(self, path, output_writer):
            """Define a route for an output_writer"""
            if self._unrouted and self.path == path:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output_writer(self.wfile.write)
                
                self.wfile.close()
                self._unrouted = False;

        def command_route(self, command):
            """Define a route for a command and write the command page"""
            if self._unrouted and self.path == ("/" + command):
                cmd_obj = get_cmd_obj(module, command)

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                cmd_obj.command_page_writer(self.wfile.write, [], {})
                
                self.wfile.close()
                self._unrouted = False

        def post_route(self, command, postvars):
            """Define a route for user response and write the output or else provide errors"""
            if self._unrouted and self.path == ("/" + command):
                cmd_obj = get_cmd_obj(module, command)
                try:
                    result = cmd_obj(postvars)
                except Exception as e:
                    result = {
                        'type':'error',
                        'errors':[e]
                    }
                
                if result['type'] == 'error':
                    self.send_response(400)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    cmd_obj.command_page_writer(self.wfile.write, result['errors'], postvars)

                elif result['type'] == 'page':       
                    self.send_response(200)
                    self.send_header('Content-type', result['mime_type'])
                    self.end_headers()
                    self.wfile.write(result['contents'])

                elif result['type'] == 'download':
                    self.send_response(200)
                    self.send_header('Content-type', 'application/octet-stream')
                    self.send_header('Content-disposition', 'attachment; filename='+result['filename'])
                    self.end_headers()
                    self.wfile.write(result['contents'])
                    
                self.wfile.close()
                self._unrouted = False

        def end_routes(self):
            """If a route hasn't matched the path up to now, return a 404 and close stream"""
            if self._unrouted:
                self.send_response(404)
                self.end_headers()

                self.wfile.close()
                self._unrouted = False

        def do_GET(self):
            """Handle GET requests"""

            self.route("/", self.index)
            self.route("/index", self.index)
            self.route("/home", self.index)

            def r(write):#host.domain.tld/help
                write("This is still a very in development interface, there is no help.")
            self.route("/help", r)

            for command in module_commands:
                self.command_route(command)

            self.end_routes()

        def do_POST(self):
            """Handle POST requests"""
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
    interface_server = HTTPServer(("", port), get_http_handler(module))
    print "-- Starting server at http://localhost:%d --" % port
    print "To close the server, type 'ctrl-c' into this window."
    try:
        interface_server.serve_forever()

    except KeyboardInterrupt:
        return "-- Finished serving HTMLInterface --"
