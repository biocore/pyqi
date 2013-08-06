#!/usr/bin/env python

#-----------------------------------------------------------------------------
# Copyright (c) 2013, The BiPy Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------

__author__ = "Greg Caporaso"
__copyright__ = "Copyright 2013, The QIIME Project"
__credits__ = ["Greg Caporaso", "Daniel McDonald", "Doug Wendel",
               "Jai Ram Rideout"]
__license__ = "BSD"
__version__ = "0.1.0-dev"
__maintainer__ = "Greg Caporaso"
__email__ = "gregcaporaso@gmail.com"

from pyqi.core.interface import Interface, InterfaceOption, \
        InterfaceUsageExample, InterfaceResult
from pyqi.core.factory import general_factory
from pyqi.core.exception import IncompetentDeveloperError
from pyqi.core.command import Parameter
from pyqi.option_parsing import (OptionParser, OptionGroup, Option, 
                                 OptionValueError, OptionError, make_option)
from optparse import Option as OPTPARSE_OPTION 
OPTPARSE_TYPES = OPTPARSE_OPTION.TYPES

import os

def new_filepath(data, path):
    if os.path.exists(path):
        raise IOError("Output path %s already exists." % path)
    f = open(path, 'w')
    f.write(data)
    f.close()

class OptparseResult(InterfaceResult):
    def _validate_result(self):
        ### anything to validate here?
        pass

class OptparseOption(InterfaceOption):
    """An augmented option that expands a Parameter into an Option"""
    def _validate_option(self):
        ### require Name, type, etc???
        pass 

    def __str__(self):
        if self.ShortName is None:
            return '--%s' % self.Name
        else:
            return '-%s/--%s' % (self.ShortName, self.Name)

    def getOptparseOption(self):
        # can't figure out callbacks right now. InputHandler applied anyway
        # at the end of _handle_input
        if self.InputType not in OPTPARSE_TYPES:
            input_type = 'str'
        else:
            input_type = self.InputType

        if self.Required:
            # If the option doesn't already end with [REQUIRED], add it.
            help_text = self.Help
            if not help_text.strip().endswith('[REQUIRED]'):
                help_text += ' [REQUIRED]'

            if self.ShortName is None:
                option = make_option('--' + self.Name, type=input_type,
                                     help=help_text)
            else:
                option = make_option('-' + self.ShortName,
                                     '--' + self.Name, type=input_type,
                                     help=help_text)
        else:
            if self.DefaultDescription is None:
                help_text = '%s [default: %%default]' % self.Help
            else:
                help_text = '%s [default: %s]' % (self.Help,
                                                  self.DefaultDescription)

            if self.ShortName is None:
                option = make_option('--' + self.Name, type=input_type,
                                     help=help_text, default=self.Default)
            else:
                option = make_option('-' + self.ShortName,
                                     '--' + self.Name, type=input_type,
                                     help=help_text, default=self.Default)
        return option

class OptparseUsageExample(InterfaceUsageExample):
    """Provide structure to a usage example"""
    def _validate_usage_example(self):
        if self.ShortDesc is None:
            raise UsageExampleError("Must define ShortDesc")
        if self.LongDesc is None:
            raise UsageExampleError("Must define LongDesc")
        if self.Ex is None:
            raise UsageExampleError("Must define Ex")

class OptparseInterface(Interface):
    """A command line interface"""
    DisallowPositionalArguments = True
    HelpOnNoArguments = True 
    OptionalInputLine = '[] indicates optional input (order unimportant)'
    RequiredInputLine = '{} indicates required input (order unimportant)'
    
    def __init__(self, **kwargs):
        self.BelovedFunctionality = {}
        self.UsageExamples = []
        self.UsageExamples.extend(self._get_usage_examples())

        if len(self.UsageExamples) < 1:
            raise IncompetentDeveloperError("There are no usage examples "
                                            "associated with this command.")

        super(OptparseInterface, self).__init__(**kwargs)

    def _the_in_validator(self, in_):
        """Validate input coming from the command line"""
        if not isinstance(in_, list):
            raise IncompetentDeveloperError("Unsupported input '%r'. Input "
                                            "must be a list." % in_)

    def _input_handler(self, in_, *args, **kwargs):
        """Parses command-line input."""
        required_opts = [opt for opt in self._get_inputs() if opt.Required]
        optional_opts = [opt for opt in self._get_inputs() if not opt.Required]

        # Build the usage and version strings
        usage = self._build_usage_lines(required_opts)
        version = 'Version: %prog ' + __version__

        # Instantiate the command line parser object
        parser = OptionParser(usage=usage, version=version)

        # If no arguments were provided, print the help string (unless the
        # caller specified not to).
        if self.HelpOnNoArguments and len(in_) == 0:
            parser.print_usage()
            return parser.exit(-1)

        if required_opts:
            # Define an option group so all required options are grouped
            # together and under a common header.
            required = OptionGroup(parser, "REQUIRED options",
                                   "The following options must be provided "
                                   "under all circumstances.")
            for ro in required_opts:
                required.add_option(ro.getOptparseOption())
            parser.add_option_group(required)

        # Add the optional options.
        for oo in optional_opts:
            parser.add_option(oo.getOptparseOption())

        #####
        # THIS IS THE NATURAL BREAKING POINT FOR THIS FUNCTIONALITY
        #####

        # Parse our input.
        opts, args = parser.parse_args(in_)

        # If positional arguments are not allowed, and any were provided, raise
        # an error.
        if self.DisallowPositionalArguments and len(args) != 0:
            parser.error("Positional argument detected: %s\n" % str(args[0]) +
             " Be sure all parameters are identified by their option name.\n" +
             " (e.g.: include the '-i' in '-i INPUT_DIR')")

        # Test that all required options were provided.
        if required_opts:
            required_option_ids = [o.dest for o in required.option_list]
            for required_option_id in required_option_ids:
                if getattr(opts,required_option_id) == None:
                    parser.error('Required option --%s omitted.' %
                                 required_option_id)

        beloved_functionality = opts.__dict__
        self.BelovedFunctionality = beloved_functionality
        for option in self._get_inputs():
            if option.InputHandler is not None:
                name = option.Name
                value = self.BelovedFunctionality[name]
                self.BelovedFunctionality[name] = option.InputHandler(value)
        return self.BelovedFunctionality

    def _build_usage_lines(self, required_options):
        """ Build the usage string from components """
        line1 = 'usage: %prog [options] ' + \
                '{%s}' % ' '.join(['%s %s' % (str(rp),rp.Name.upper())
                                   for rp in required_options])

        formatted_usage_examples = []
        for usage_example in self.UsageExamples:
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
        for output in self._get_outputs():
            rk = output.ResultKey
            if rk not in results:
                raise IncompetentDeveloperError("Did not find the expected "
                                                "output '%s' in results." % rk)


            if output.Name is None:
                results[rk] = output.OutputHandler(rk, results[rk])
            else:
                opt_value = self.BelovedFunctionality[output.Name]
                results[rk] = output.OutputHandler(rk, results[rk], opt_value)

def optparse_factory(command_constructor, usage_examples, inputs, outputs):
    """Optparse command line interface factory
    
    command_constructor - a subclass of ``Command``
    usage_examples - usage examples for using ``command_constructor`` on via a
        command line interface.
    inputs  - config ``inputs`` or a list of ``OptparseOptions``
    otuputs - config ``outputs`` or a list of ``OptparseResults`` 
    """
    return general_factory(command_constructor, usage_examples, inputs, outputs,
                           OptparseInterface)

def optparse_main(interface_object, local_argv):
    """Construct and execute an interface object"""
    optparse_cmd = interface_object()
    result = optparse_cmd(local_argv[1:])
    return 0
