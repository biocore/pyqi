#!/usr/bin/env python

#-----------------------------------------------------------------------------
# Copyright (c) 2013, The BiPy Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------

__credits__ = ["Greg Caporaso", "Daniel McDonald", "Doug Wendel",
               "Jai Ram Rideout", "Evan Bolyen"]

import importlib
from sys import exit, stderr
from ConfigParser import SafeConfigParser
from glob import glob
from os.path import basename, dirname, expanduser, join
from pyqi.core.exception import IncompetentDeveloperError

class Interface(object):
    CommandConstructor = None

    def __init__(self, **kwargs):
        """ """
        self.CmdInstance = None

        if self.CommandConstructor is None:
            raise IncompetentDeveloperError("Cannot construct an Interface "
                                            "without a CommandConstructor.")

        self.CmdInstance = self.CommandConstructor(**kwargs)

        self._validate_usage_examples(self._get_usage_examples())
        self._validate_inputs_outputs(self._get_inputs(), self._get_outputs())
    
    def __call__(self, in_, *args, **kwargs):
        self._the_in_validator(in_)
        cmd_input = self._input_handler(in_, *args, **kwargs)
        cmd_result = self.CmdInstance(**cmd_input)
        self._the_out_validator(cmd_result)
        return self._output_handler(cmd_result)

    def _validate_usage_examples(self, usage_examples):
        """Perform validation on a list of ``InterfaceUsageExample`` objects.

        ``usage_examples`` will be the output of
        ``self._get_usage_examples()``. Subclasses can override to perform
        validation that requires a list of all usage examples. Validation that
        should be performed on a per-usage example basis should instead go into
        ``InterfaceUsageExample._validate_usage_example``.
        """
        pass

    def _validate_inputs_outputs(self, inputs, outputs):
        """Perform validation on interface IO objects.

        ``inputs`` will be the output of ``self._get_inputs()``. Subclasses can
        override to perform validation that requires a list of all input
        options. Validation that should be performed on a per-option basis
        should instead go into ``InterfaceOption._validate_option``.

        ``outputs`` will be the output of ``self._get_outputs()``. Subclasses
        can override to perform validation that requires a list of all
        interface results. Validation that should be performed on a
        per-interface result basis should instead go into
        ``InterfaceOutputOption._validate_result``.
        """
        param_names = [input_.getParameterName()
                       for input_ in inputs
                       if input_.getParameterName() is not None]

        if len(param_names) != len(set(param_names)):
            raise IncompetentDeveloperError("Found more than one "
                                            "InterfaceOption mapping to the "
                                            "same Parameter.")

        input_names = set([i.Name for i in inputs])
        for ifout in outputs:
            if ifout.InputName is None:
                continue
            
            if ifout.InputName not in input_names:
                raise IncompetentDeveloperError(\
                        "Could not link %s to an input!" % ifout.InputName)

    def _the_in_validator(self, in_):
        """The job securator"""
        raise NotImplementedError("All subclasses must implement "
                                  "_the_in_validator.")

    def _the_out_validator(self, out_):
        """The result securator"""
        raise NotImplementedError("All subclasses must implement "
                                  "_the_out_validator.")

    def _input_handler(self, in_, *args, **kwargs):
        raise NotImplementedError("All subclasses must implement "
                                  "_input_handler.")

    def _output_handler(self, results):
        raise NotImplementedError("All subclasses must implement "
                                  "_output_handler.")

    def _get_usage_examples(self):
        """Return a list of ``InterfaceUsageExample`` objects
        
        These are typically set in a command+interface specific configuration
        file and passed to ``pyqi.core.general_factory``
        """
        raise NotImplementedError("Must define _get_usage_examples")

    def _get_inputs(self):
        """Return a list of ``InterfaceOption`` objects
        
        These are typically set in a command+interface specific configuration
        file and passed to ``pyqi.core.general_factory``
        """
        raise NotImplementedError("Must define _get_inputs")

    def _get_outputs(self):
        """Return a list of ``InterfaceOutputOption`` objects
        
        These are typically set in a command+interface specific configuration
        file and passed to ``pyqi.core.general_factory``
        """
        raise NotImplementedError("Must define _get_outputs")

    def _get_version(self):
        """Return a version string, e.g., ``'0.1'``
        
        This is typically set in a command+interface specific configuration
        file and passed to ``pyqi.core.general_factory``
        """
        raise NotImplementedError("Must define _get_version")

class InterfaceOption(object):
    """Describes an option and what to do with it
    
    ``Parameter`` is a pyqi.core.command.Parameter instance, typically an 
        instance of a ``CommandIn`` or a ``CommandOut``.
    ``Type`` refers to the interface type, not the actually datatype of the
        ``Parameter``. For instance, a file path may be specified on a command
        line interface for a BIOM table. The ``Parameter.Datatype`` is a BIOM 
        type, while the ``InterfaceOption.Type`` is a string or possibly a 
        ``FilePath`` object.
    ``Handler`` is a function that either transforms the value associated with 
        the option into the ``Parameter.DataType`` (e.g., if ``Parameter`` is a
        ``CommandIn``), or the result of a ``Command`` into something consumable
        by the interface (e.g., if ``Parameter`` is a ``CommandOut``).
    ``Name`` is the name of the ``InterfaceOption``, e.g,, 'input-fp'
    ``Help`` is a description of the ``InterfaceOption``
    """
    def __init__(self, Parameter=None, Type=None, Handler=None, Name=None,
                 Help=None):
        self.Parameter = Parameter
        
        if self.Parameter is None:
            if Name is None:
                raise IncompetentDeveloperError("Must specify a Name for the "
                                                "InterfaceOption since it "
                                                "doesn't have a Parameter.")
            if Help is None:
                raise IncompetentDeveloperError("Must specify Help for the "
                                                "InterfaceOption since it "
                                                "doesn't have a Parameter.")
            self.Name = Name
            self.Help = Help

        else:
            # Transfer information from Parameter unless overridden here.
            self.Name = Parameter.Name if Name is None else Name
            self.Help = Parameter.Description if Help is None else Help
            
        # This information is never contained in a Parameter. 
        self.Type = Type
        self.Handler = Handler

    def _validate_option(self):
        """Interface specific validation requirements"""
        raise NotImplementedError("Must define in the subclass")

    def getParameterName(self):
        if self.Parameter is None:
            return None
        else:
            return self.Parameter.Name

class InterfaceInputOption(InterfaceOption):
    _primitive_mapping = {
        "None": None,
        "bool": bool,
        "str": str,
        "int": int,
        "float": float,
        "long": long,
        "complex": complex,
        "tuple": tuple,
        "dict": dict,
        "list": list,
        "set": set,
        "unicode": unicode,
        "frozenset": frozenset
    }

    def __init__(self, Action=None, Required=False, Default=None, 
                 ShortName=None, DefaultDescription=None, 
                 convert_to_dashed_name=True, **kwargs):
        super(InterfaceInputOption, self).__init__(**kwargs)

        self.Required = Required
        self.Default = Default
        self.DefaultDescription = DefaultDescription
        self.ShortName = ShortName
        self.Action = Action
        
        if convert_to_dashed_name:
            self.Name = self.Name.replace('_', '-')

        if self.Required and self.Default is not None:
            raise IncompetentDeveloperError("Found required option '%s' "
                    "with default value '%s'. Required options cannot have "
                    "default values." % (self.Name, self.Default))
    
        if self.Default is None and self.Parameter is not None:
            self.Default = self.Parameter.Default
            self.DefaultDescription = self.Parameter.DefaultDescription 

        # If a parameter is required, the option is always required, but
        # if a parameter is not required, but the option does require it,
        # then we make the option required.
        if self.Parameter is not None: 
            self.Required = self.Parameter.Required

            if not self.Parameter.Required and Required:
                self.Required = True
        
        self._convert_primitive_strings()
        self._validate_option()

    def _convert_primitive_strings(self):
        """Convert our Type to a python type object if it is a primitive string.
           Otherwise, leave unchanged"""
        self.Type = self._primitive_mapping.get(self.Type, self.Type)

class InterfaceOutputOption(InterfaceOption):
    def __init__(self, InputName=None, **kwargs):
        super(InterfaceOutputOption, self).__init__(**kwargs)

        self.InputName = InputName

class InterfaceUsageExample(object): 
    """Provide structure to a usage example"""
    def __init__(self, ShortDesc, LongDesc, Ex):
        self.ShortDesc = ShortDesc
        self.LongDesc = LongDesc
        self.Ex = Ex

        self._validate_usage_example()

    def _validate_usage_example(self):
        """Interface specific usage example validation"""
        raise NotImplementedError("Must define in the subclass")

def get_command_names(config_base_name):
    """Return a list of available command names.

    Command names are strings and are returned in alphabetical order.
    ``config_base_name`` must be the python module path to a directory
    containing config files.
    """
    # Load the interface configuration base.
    try:
        config_base_module = importlib.import_module(config_base_name)
    except ImportError:
        raise ImportError("Unable to load base config module: %s" %
                          config_base_name)

    config_base_dir = dirname(config_base_module.__file__)

    # from http://stackoverflow.com/questions/1057431/loading-all-modules-in-a-folder-in-python
    command_names = CommandList()
    for f in glob(join(config_base_dir, '*.py')):
        command_name = basename(f)

        if not command_name.startswith('__init__'):
            command_names.append(command_name[:-3])
    command_names.sort()

    return command_names

def get_command_config(command_config_module, cmd, exit_on_failure=True):
    """Get the configuration for a ``Command``"""
    cmd_cfg = None
    error_msg = None
    python_cmd_name = cmd.replace('-', '_')

    try:
        cmd_cfg = importlib.import_module('.'.join([command_config_module,
                                                    python_cmd_name]))
    except ImportError, e:
        error_msg = str(e)

        if exit_on_failure:
            stderr.write("Unable to import the command configuration for "
                         "%s:\n" % cmd)
            stderr.write(error_msg)
            stderr.write('\n')
            exit(1)

    return cmd_cfg, error_msg

class CommandList(list):
    def __init__(self):
        super(CommandList, self).__init__()

    def append(self, item):
        super(CommandList, self).append(self._convert_to_dashed_name(item))

    def __contains__(self, item):
        return super(CommandList,
                     self).__contains__(self._convert_to_dashed_name(item))

    def _convert_to_dashed_name(self, name):
        return name.replace('_', '-')
