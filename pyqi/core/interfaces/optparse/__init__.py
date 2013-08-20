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
        pass

class OptparseOption(InterfaceOption):
    """An augmented option that expands a Parameter into an Option"""

    def __init__(self, Parameter=None, InputType=str, InputAction='store',
                 InputHandler=None, ShortName=None, Name=None, Required=False,
                 Help=None, Default=None, DefaultDescription=None,
                 convert_to_dashed_name=True):
        super(OptparseOption, self).__init__(Parameter=Parameter,
                InputType=InputType, InputAction=InputAction,
                InputHandler=InputHandler, ShortName=ShortName, Name=Name,
                Required=Required, Help=Help, Default=Default,
                DefaultDescription=DefaultDescription,
                convert_to_dashed_name=convert_to_dashed_name)

    def _validate_option(self):
        # optparse takes care of validating InputType, InputAction, and
        # ShortName, so we don't need any checks here.
        pass

    def __str__(self):
        if self.ShortName is None:
            return '--%s' % self.Name
        else:
            return '-%s/--%s' % (self.ShortName, self.Name)

    def getOptparseOption(self):
        if self.Required:
            # If the option doesn't already end with [REQUIRED], add it.
            help_text = self.Help

            if not help_text.strip().endswith('[REQUIRED]'):
                help_text += ' [REQUIRED]'

            if self.ShortName is None:
                option = make_option('--' + self.Name, type=self.InputType,
                                     action=self.InputAction, help=help_text)
            else:
                option = make_option('-' + self.ShortName,
                                     '--' + self.Name, type=self.InputType,
                                     action=self.InputAction, help=help_text)
        else:
            if self.DefaultDescription is None:
                help_text = '%s [default: %%default]' % self.Help
            else:
                help_text = '%s [default: %s]' % (self.Help,
                                                  self.DefaultDescription)

            if self.ShortName is None:
                option = make_option('--' + self.Name, type=self.InputType,
                                     action=self.InputAction, help=help_text,
                                     default=self.Default)
            else:
                option = make_option('-' + self.ShortName,
                                     '--' + self.Name, type=self.InputType,
                                     action=self.InputAction, help=help_text,
                                     default=self.Default)

        return option

class OptparseUsageExample(InterfaceUsageExample):
    """Provide structure to a usage example"""
    def _validate_usage_example(self):
        if self.ShortDesc is None:
            raise IncompetentDeveloperError("Must define ShortDesc")
        if self.LongDesc is None:
            raise IncompetentDeveloperError("Must define LongDesc")
        if self.Ex is None:
            raise IncompetentDeveloperError("Must define Ex")

class OptparseInterface(Interface):
    """A command line interface"""
    DisallowPositionalArguments = True
    HelpOnNoArguments = True 
    OptionalInputLine = '[] indicates optional input (order unimportant)'
    RequiredInputLine = '{} indicates required input (order unimportant)'
    
    def __init__(self, **kwargs):
        super(OptparseInterface, self).__init__(**kwargs)

    def _validate_usage_examples(self, usage_examples):
        super(OptparseInterface, self)._validate_usage_examples(usage_examples)

        if len(usage_examples) < 1:
            raise IncompetentDeveloperError("There are no usage examples "
                                            "associated with this command.")

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

        # If the command has required options and no input arguments were
        # provided, print the help string.
        if len(required_opts) > 0 and self.HelpOnNoArguments and len(in_) == 0:
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
            # dest may be different from the original option name because
            # optparse converts names from dashed to underscored.
            required_option_ids = [(o.dest, o.get_opt_string())
                                   for o in required.option_list]
            for required_dest, required_name in required_option_ids:
                if getattr(opts, required_dest) is None:
                    parser.error('Required option %s omitted.' % required_name)

        # Build up command input dictionary. This will be passed to
        # Command.__call__ as kwargs.
        self._optparse_input = opts.__dict__

        cmd_input_kwargs = {}
        for option in self._get_inputs():
            if option.Parameter is not None:
                param_name = option.getParameterName()
                optparse_clean_name = \
                        self._get_optparse_clean_name(option.Name)

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
                optparse_clean_name = \
                        self._get_optparse_clean_name(output.OptionName)
                opt_value = self._optparse_input[optparse_clean_name]
                handled_results[rk] = output.OutputHandler(rk, results[rk],
                                                           opt_value)

        return handled_results

    def _get_optparse_clean_name(self, name):
        # optparse converts dashes to underscores in long option names.
        return name.replace('-', '_')

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
