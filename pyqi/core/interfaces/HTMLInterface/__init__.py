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

from pyqi.core.interfaces.optparse import OptparseInterface, OptparseResult, OptparseOption, OptparseUsageExample


class HTMLInterfaceResult(OptparseResult):
    pass

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


        # Test that all required options were provided.
       # if required_opts:
            # dest may be different from the original option name because
            # optparse converts names from dashed to underscored.
         #   required_option_ids = [(o.dest, o.get_opt_string())
            #                       for o in required.option_list]
       #     for required_dest, required_name in required_option_ids:
       #         if getattr(formatted_input, required_dest) is None:
         #           print('Required option %s omitted.' % required_name)

        # Build up command input dictionary. This will be passed to
        # Command.__call__ as kwargs.
        self._optparse_input = formatted_input

        cmd_input_kwargs = {}
        for option in self._get_inputs():
            if option.Parameter is not None:
                param_name = option.getParameterName()
                optparse_clean_name = option.Name

                if option.InputHandler is None:
                    value = self._optparse_input[optparse_clean_name]
                else:
                    value = option.InputHandler(
                            self._optparse_input[optparse_clean_name])

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

        for output in self._get_outputs():
            rk = output.ResultKey
            if rk not in results:
                raise IncompetentDeveloperError("Did not find the expected "
                                                "output '%s' in results." % rk)

            if output.OptionName is None:
                handled_results[rk] = output.OutputHandler(rk, results[rk])
            else:
                optparse_clean_name = output.OptionName
                opt_value = self._optparse_input[optparse_clean_name]
                handled_results[rk] = output.OutputHandler(rk, results[rk],
                                                           opt_value)


        return handled_results

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

def command_output_factory(module, command, POST):
    
    def command_out(write):
        #validate data, if wrong, return command_page_factory's command_page

        write(POST)

    return command_out
def command_page_factory(module, command):
    
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
        'upload_file':'%s:<input type="text" name="pyqi_%s" />%s',
        'new_filepath':'%s:<input type="text" name="pyqi_%s" />%s'
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

        cmd_obj = get_cmd_obj(module, command)()
        write(templateHead % (command, command))

        write(cmd_obj._build_usage_lines([opt for opt in cmd_obj._get_inputs() if opt.Required]))

        write('<form method="POST">')
        for i in cmd_obj._get_inputs():
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

        def download_route(self, path, output_writer, module, command, postvars):
            if self._unrouted and self.path == path:
                cmd_obj = get_cmd_obj(module, command)()
                result = cmd_obj(postvars)
                filename = "unnamed.txt"
                for output in cmd_obj._get_outputs():
                    if output.ResultKey == "result":
                        filename = cmd_obj._optparse_input[output.OptionName]

                self.send_response(200)
                self.send_header('Content-disposition', 'attachment; filename=' + filename)
                self.send_header('Content-type', 'application/octet-stream')
                self.end_headers()
                self.wfile.write(result['result'])


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
                self.download_route("/"+command, command_output_factory(module,command, postvars), module, command, postvars)



    return HTTPHandler




#This will generally be called from a generated command.
def start_server(port, module):
    """Start a server for the HTMLInterface on the specified port"""

    server = HTTPServer(("", port), HTTPHandler_factory(module))
    server.serve_forever()

