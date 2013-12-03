#!/usr/bin/env python

#-----------------------------------------------------------------------------
# Copyright (c) 2013, The BiPy Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------

__credits__ = ["Greg Caporaso", "Daniel McDonald", "Gavin Huttley",
               "Rob Knight", "Doug Wendel", "Jai Ram Rideout",
               "Jose Antonio Navas Molina"]

import os
import types
from copy import copy
from glob import glob
from os.path import abspath, exists, isdir, isfile, split
from optparse import (Option, OptionParser, OptionGroup, OptionValueError,
                      OptionError)
from pyqi.core.interface import (Interface, InterfaceInputOption, 
                                 InterfaceOutputOption, InterfaceUsageExample)
from pyqi.core.factory import general_factory
from pyqi.core.exception import IncompetentDeveloperError
from pyqi.core.command import Parameter

class OptparseResult(InterfaceOutputOption):
    def __init__(self, **kwargs):
        super(OptparseResult, self).__init__(**kwargs)

    def _validate_option(self):
        pass

class OptparseOption(InterfaceInputOption):
    """An augmented option that expands a ``CommandIn`` into an Option"""

    def __init__(self, **kwargs):
        super(OptparseOption, self).__init__(**kwargs)

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
                option = PyqiOption('--' + self.Name, type=self.Type,
                                    action=self.Action, help=help_text)
            else:
                option = PyqiOption('-' + self.ShortName,
                                    '--' + self.Name, type=self.Type,
                                    action=self.Action, help=help_text)
        else:
            if self.DefaultDescription is None:
                help_text = '%s [default: %%default]' % self.Help
            else:
                help_text = '%s [default: %s]' % (self.Help,
                                                  self.DefaultDescription)

            if self.ShortName is None:
                option = PyqiOption('--' + self.Name, type=self.Type,
                                    action=self.Action, help=help_text,
                                    default=self.Default)
            else:
                option = PyqiOption('-' + self.ShortName,
                                    '--' + self.Name, type=self.Type,
                                    action=self.Action, help=help_text,
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

    def _the_out_validator(self, out_):
        """Validate output coming from the command call"""
        if not isinstance(out_, dict):
            raise IncompetentDeveloperError("Unsupported result '%r'. Result "
                                            "must be a dict." % out_)

    def _input_handler(self, in_, *args, **kwargs):
        """Parses command-line input."""
        required_opts = [opt for opt in self._get_inputs() if opt.Required]
        optional_opts = [opt for opt in self._get_inputs() if not opt.Required]

        # Build the usage and version strings
        usage = self._build_usage_lines(required_opts)
        version = 'Version: %prog ' + self._get_version()

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

                if option.Handler is None:
                    value = self._optparse_input[optparse_clean_name]
                else:
                    value = option.Handler(
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
            rk = output.Name
        
            if output.InputName is None:
                handled_results[rk] = output.Handler(rk, results[rk])
            else:
                optparse_clean_name = \
                        self._get_optparse_clean_name(output.InputName)
                opt_value = self._optparse_input[optparse_clean_name]
                handled_results[rk] = output.Handler(rk, results[rk],
                                                           opt_value)

        return handled_results

    def _get_optparse_clean_name(self, name):
        # optparse converts dashes to underscores in long option names.
        return name.replace('-', '_')

def optparse_factory(command_constructor, usage_examples, inputs, outputs,
                     version):
    """Optparse command line interface factory
    
    command_constructor - a subclass of ``Command``
    usage_examples - usage examples for using ``command_constructor`` via a
        command line interface.
    inputs  - config ``inputs`` or a list of ``OptparseOptions``
    outputs - config ``outputs`` or a list of ``OptparseResults`` 
    version - config ``__version__`` (a version string)
    """
    return general_factory(command_constructor, usage_examples, inputs,
                           outputs, version, OptparseInterface)

def optparse_main(interface_object, local_argv):
    """Construct and execute an interface object"""
    optparse_cmd = interface_object()
    result = optparse_cmd(local_argv[1:])
    return 0

# Definition of PyqiOption option type, a subclass of Option that contains
# specific types for filepaths and directory paths.
#
# This code was derived from PyCogent (http://www.pycogent.org) and QIIME
# (http://www.qiime.org), where it was initally developed.
#
# QIIME and PyCogent are GPL projects, but we obtained permission from the
# authors of this code to port it to pyqi (and keep it under pyqi's BSD
# license).
#
# TODO: this code needs to be refactored to better fit the pyqi framework.
# Should probably get added to the OptparseInterface class.

def check_existing_filepath(option, opt, value):
    if not exists(value):
        raise OptionValueError(
            "option %s: file does not exist: %r" % (opt, value))
    elif not isfile(value):
        raise OptionValueError(
            "option %s: not a regular file (can't be a directory!): %r" % (opt, value))
    else:
        return value

def check_existing_filepaths(option, opt, value):
    paths = []
    for v in value.split(','):
        fps = glob(v)
        if len(fps) == 0:
            raise OptionValueError(
             "No filepaths match pattern/name '%s'. "
             "All patterns must be matched at least once." % v)
        else:
            paths.extend(fps)
    values = []
    for v in paths:
        check_existing_filepath(option,opt,v)
        values.append(v)
    return values

def check_existing_dirpath(option, opt, value):
    if not exists(value):
        raise OptionValueError(
            "option %s: directory does not exist: %r" % (opt, value))
    elif not isdir(value):
        raise OptionValueError(
            "option %s: not a directory (can't be a file!): %r" % (opt, value))
    else:
        return value

def check_existing_dirpaths(option, opt, value):
    paths = []
    for v in value.split(','):
        dps = glob(v)
        if len(dps) == 0:
            raise OptionValueError(
                "No dirpaths match pattern/name '%s'."
                "All patterns must be matched at least once." % v)
        else:
            paths.extend(dps)
    values = []
    for v in paths:
        check_existing_dirpath(option, opt, v)
        values.append(v)
    return values

def check_new_filepath(option, opt, value):
    if exists(value):
        if isdir(value):
            raise OptionValueError(
                "option %s: output file exists and it is a directory: %r" %(opt,
                    value))
    return value
        
def check_new_dirpath(option, opt, value):
    if exists(value):
        if isfile(value):
            raise OptionValueError(
                "option %s: output directory exists and it is a file: %r" %(opt,
                    value))
    return value
    
def check_existing_path(option, opt, value):
    if not exists(value):
        raise OptionValueError(
            "option %s: path does not exist: %r" % (opt, value))
    return value
    
def check_new_path(option, opt, value):
    return value

def check_multiple_choice(option, opt, value):
    values = value.split(option.split_char)
    for v in values:
        if v not in option.mchoices:
            choices = ",".join(map(repr, option.mchoices))
            raise OptionValueError(
                "option %s: invalid choice: %r (choose from %s)"
                % (opt, v, choices))
    return values

def check_blast_db(option, opt, value):
    db_dir, db_name = split(abspath(value))
    if not exists(db_dir):
        raise OptionValueError(
            "option %s: path does not exists: %r" % (opt, db_dir))
    elif not isdir(db_dir):
        raise OptionValueError(
            "option %s: not a directory: %r" % (opt, db_dir))
    return value

class PyqiOption(Option):
    ATTRS = Option.ATTRS + ['mchoices','split_char']

    TYPES = Option.TYPES + ("existing_path",
                            "new_path",
                            "existing_filepath",
                            "existing_filepaths",
                            "new_filepath",
                            "existing_dirpath",
                            "existing_dirpaths",
                            "new_dirpath",
                            "multiple_choice",
                            "blast_db")
    TYPE_CHECKER = copy(Option.TYPE_CHECKER)
    # for cases where the user specifies an existing file or directory
    # as input, but it can be either a dir or a file
    TYPE_CHECKER["existing_path"] = check_existing_path
    # for cases where the user specifies a new file or directory
    # as output, but it can be either a dir or a file
    TYPE_CHECKER["new_path"] = check_new_path
    # for cases where the user passes a single existing file
    TYPE_CHECKER["existing_filepath"] = check_existing_filepath
    # for cases where the user passes one or more existing files
    # as a comma-separated list - paths are returned as a list
    TYPE_CHECKER["existing_filepaths"] = check_existing_filepaths
    # for cases where the user is passing a new path to be 
    # create (e.g., an output file)
    TYPE_CHECKER["new_filepath"] = check_new_filepath
    # for cases where the user is passing an existing directory
    # (e.g., containing a set of input files)
    TYPE_CHECKER["existing_dirpath"] = check_existing_dirpath
    # for cases where the user passes one or more existing directories
    # as a comma-separated list - paths are returned as a list
    TYPE_CHECKER["existing_dirpaths"] = check_existing_dirpaths
    # for cases where the user is passing a new directory to be 
    # create (e.g., an output dir which will contain many result files)
    TYPE_CHECKER["new_dirpath"] = check_new_dirpath
    # for cases where the user is passing one or more values
    # as comma- or semicolon-separated list
    # choices are returned as a list
    TYPE_CHECKER["multiple_choice"] = check_multiple_choice
    # for cases where the user is passing a blast database option
    # blast_db is returned as a string
    TYPE_CHECKER["blast_db"] = check_blast_db

    def _check_multiple_choice(self):
        if self.type == "multiple_choice":
            if self.mchoices is None:
                raise OptionError(
                    "must supply a list of mchoices for type '%s'" % self.type, self)
            elif type(self.mchoices) not in (types.TupleType, types.ListType):
                raise OptionError(
                    "choices must be a list of strings ('%s' supplied)"
                    % str(type(self.mchoices)).split("'")[1], self)
            if self.split_char is None:
                self.split_char = ','
        elif self.mchoices is not None:
            raise OptionError(
                "must not supply mchoices for type %r" % self.type, self)

    CHECK_METHODS = Option.CHECK_METHODS + [_check_multiple_choice]
