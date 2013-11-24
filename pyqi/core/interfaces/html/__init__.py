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
__credits__ = ["Evan Bolyen", "Jai Ram Rideout", "Daniel McDonald", "Greg Caporaso"]
__license__ = "BSD"
__version__ = "0.2.0-dev"
__maintainer__ = "Evan Bolyen"
__email__ = "ebolyen@gmail.com"

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



class HTMLResult(InterfaceOutputOption):
    def __init__(self, MIMEType=None, **kwargs):
        super(HTMLResult, self).__init__(**kwargs)
        self.MIMEType = MIMEType;


class HTMLDownload(HTMLResult):
    def __init__(self, FileExtension=None, FilenameLookup=None, DefaultFilename=None, MIMEType='application/octet-stream', **kwargs):
        super(HTMLDownload, self).__init__(MIMEType=MIMEType, **kwargs)
        self.FileExtension = FileExtension
        self.FilenameLookup = FilenameLookup
        self.DefaultFilename = DefaultFilename


class HTMLPage(HTMLResult):
    def __init__(self, MIMEType='text/html', **kwargs):
        super(HTMLPage, self).__init__(MIMEType=MIMEType, **kwargs)


class HTMLInputOption(InterfaceInputOption):

    primitive_mapping = {
        "None": None,
        "str": str,
        "int": int,
        "float": float,
        "long": long,
        "complex": complex
    }

    type_handlers = {
        None: lambda: None,
        str: lambda x: str(x.value),
        int: lambda x: int(x.value),
        float: lambda x: float(x.value),
        long: lambda x: long(x.value),
        complex: lambda x: complex(x.value),
        "upload_file": lambda x: x.file.read(),
        "multiple_choice": lambda x: x.value
    }

    def __init__(self, Choices=None, Type=str, **kwargs):
        self.Choices = Choices
        super(HTMLInputOption, self).__init__(Type=self._convert_primitive_strings(Type), **kwargs)

    def _convert_primitive_strings(self, t):
        """Convert the type `t` to a python type object if it is a primitive string.
           Otherwise, leave unchanged"""
        return self.primitive_mapping.get(t, t)

    def _validate_option(self):

        if self.Type not in self.type_handlers:
            raise IncompetentDeveloperError("Unsupported Type in HTMLInputOption: %s" % self.Type)


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

class HTMLInterface(Interface):

    style_css = os.path.join(os.path.dirname(__file__), 'assets/style.css')

    def __init__(self, InputPrefix='pyqi_', **kwargs):
        self._html_input_prefix = InputPrefix
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

    def _cast_as(self, postdata, t):
        """Casts str(postdata.value) as an object of the correct type 't'"""

        return HTMLInputOption.type_handlers[t](postdata) if postdata is not None else None

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
                formatted_input[option.Name] = self._cast_as(formatted_input[option.Name], 
                                                            option.Type)
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

        #This is almost sad, but I'm not sure theres anything else to do.
        return '<p>%s</p>' % self.CmdInstance.LongDescription

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
        if output.InputName is None:
            handled_results = output.Handler(rk, results[rk])
        else:
            handled_results = output.Handler(rk, results[rk], self._html_interface_input[output.InputName])
    
        if isinstance(output, HTMLDownload):
            return self._output_download_handler(output, handled_results)

        elif isinstance(output, HTMLPage):
            return self._output_page_handler(output, handled_results)



    def _input_map(self, i):
        """Return the HTML needed for user input given an HTMLInterfaceOption"""
        input_name = ''.join([self._html_input_prefix, i.Name])
        string_input = lambda: '<input type="text" name="%s" />' % input_name
        number_input = lambda: '<input type="number" name="%s" />' % input_name
        upload_input = lambda: '<input type="file" name="%s" />' % input_name
        mchoice_input = lambda: ''.join(
            [ ('(%s<input type="radio" name="%s" value="%s" />)' % (choice, input_name, choice)) 
                for choice in i.Choices ]
        )

        input_switch = {
            None: string_input,
            str: string_input,
            int: number_input,
            float: number_input,
            long: number_input,
            complex: string_input,
            "multiple_choice": mchoice_input,
            "upload_file": upload_input
        }

        return ''.join(['<tr><td class="right">',
                        (''.join(['<span class="required">*</span>', i.Name]) if i.Required  else i.Name),
                       '</td><td>',
                       input_switch[i.Type](),
                       '</td></tr><tr><td></td><td>',
                        i.Help,
                       '</td></tr><tr><td>&nbsp;</td></tr>'
                       ])
       

    def command_page_writer(self, write, errors):
        """Write an HTML page which contains a form for user input"""

        write('<!DOCTYPE html><html><head><title>%s</title>' % self.CommandName)
        write('<style>')

        # It would be better if I made a routing system for all files in assets
        # This would also probably be done in tandem with the proper seperation of server and execution.
        with open(HTMLInterface.style_css, "U") as f:
            write(f.read())
        # but until then, the above works.

        write('</style>')
        write('</head><body><h1>%s</h1><div id="content">' % self.CommandName)

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
        


def html_interface_factory(command_constructor, usage_examples, inputs, outputs,
                     version, command_name):
    interface_class = general_factory(command_constructor, usage_examples, inputs,
                           outputs, version, HTMLInterface)
    interface_class.CommandName = command_name
    return interface_class

def get_cmd_obj(cmd_cfg_mod, cmd):
    """Get a ``Command`` object"""
    cmd_cfg,_ = get_command_config(cmd_cfg_mod, cmd)
    cmd_class = html_interface_factory(cmd_cfg.CommandConstructor, [], 
                            cmd_cfg.inputs, [cmd_cfg.output],
                            cmd_cfg.__version__, cmd)
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
            if self._unrouted and self.path == "/" + command:
                cmd_obj = get_cmd_obj(module, command)

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                cmd_obj.command_page_writer(self.wfile.write, [])
                
                self.wfile.close()
                self._unrouted = False

        def post_route(self, command, postvars):
            """Define a route for user response and write the output or else provide errors"""
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
            """If a route hasn't matched the path up to now, return a 404 and close stream"""
            if self._unrouted:
                self.send_response(404)
                self.end_headers()

                self.wfile.close()
                self._unrouted = False

        def do_GET(self):
            """Handle GET requests"""
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
    try:
        interface_server.serve_forever()

    except KeyboardInterrupt:
        return "--Finished serving HTMLInterface--"

