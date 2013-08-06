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

    def __call__(self, in_, *args, **kwargs):
        self._the_in_validator(in_)
        cmd_input = self._input_handler(in_, *args, **kwargs)
        return self._output_handler(self.CmdInstance(**cmd_input))

    def _the_in_validator(self, in_):
        """The job securator"""
        raise NotImplementedError("All subclasses must implement "
                                  "_the_in_validator.")

    ### _option_factory not necessary, the InterfaceOptions link to 
    ### Parameters where necessary. OptparseInterface._input_handler needs
    ### to be smarter though

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
        """Return a list of ``InterfaceResult`` objects
        
        These are typically set in a command+interface specific configuration
        file and passed to ``pyqi.core.general_factory``
        """
        raise NotImplementedError("Must define _get_outputs")

class InterfaceOption(object):
    """Describes an option and what to do with it"""
    def __init__(self, InputType=None, Parameter=None, Required=False, 
                 Name=None, ShortName=None, InputHandler=None, Help=None,
                 Default=None, DefaultDescription=None):
        self.Parameter = Parameter
        if self.Parameter is not None:
            self.Name = Parameter.Name
            self.Help = Parameter.Help
            self.Default = Parameter.Default
            self.DefaultDescription = Parameter.DefaultDescription

            # If a parameter is required, the option is always required, but
            # if a parameter is not required, but the option does require it,
            # then we make the option required.
            if not Parameter.Required and Required:
                self.Required = True
            else:
                self.Required = Parameter.Required
        else:
            if Name is None:
                raise IncompetentDeveloperError("No Parameter, and no Name!")
            if Help is None:
                raise IncompetentDeveloperError("Please specify Help")

            self.Name = Name
            self.Help = Help
            self.Required = Required
            self.Default = Default
            self.DefaultDescription = DefaultDescription

        self.ShortName = ShortName
        self.InputType = InputType
        self.InputHandler = InputHandler
        
        self._validate_option()

    def _validate_option(self):
        """Interface specific validation requirements"""
        raise NotImplementedError("Must define in the subclass")

class InterfaceResult(object):
    """Describes a result and what to do with it"""

    def __init__(self, OutputType=None, Parameter=None, Name=None, 
                 OutputHandler=None, ResultKey=None):
        self.Parameter = Parameter
        if self.Parameter is not None:
            self.Name = Parameter.Name
        else:
            self.Name = Name # can be None

        if ResultKey is None:
            raise IncompetentDeveloperError('Must associate to a result key')
        else:
            self.ResultKey = ResultKey

        if OutputHandler is None:
            raise IncompetentDeveloperError('Must associate to a OutputHandler')
        else:
            self.OutputHandler = OutputHandler

        self._validate_result()

    def _validate_result(self):
        """Validate a result object"""
        raise NotImplementedError("Must implement in a subclass")

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

