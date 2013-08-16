#!/usr/bin/env python

#-----------------------------------------------------------------------------
# Copyright (c) 2013, The BiPy Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------
from __future__ import division

__author__ = "Greg Caporaso"
__copyright__ = "Copyright 2013, The QIIME Project"
__credits__ = ["Greg Caporaso", "Daniel McDonald", "Doug Wendel",
               "Jai Ram Rideout"]
__license__ = "BSD"
__version__ = "0.1.0-dev"
__maintainer__ = "Greg Caporaso"
__email__ = "gregcaporaso@gmail.com"

import re
from pyqi.core.log import NullLogger
from pyqi.core.exception import (IncompetentDeveloperError,
                                 InvalidReturnTypeError)

class Parameter(object):
    """A ``Command`` variable

    A ``Command`` variable is interface agnostic and is analogous to a function
    argument.
    """

    def __init__(self, Name, DataType, Description, Required=False,
                 Default=None, DefaultDescription=None):
        """
        
        ``Name`` should be a valid Python name so that users can supply either
        a dictionary as input or named arguments.

        ``DataType`` specifies the type that the input must be. The input
        should be an instance of type ``DataType``.
        """
        if not self._is_valid_name(Name):
            raise IncompetentDeveloperError("Parameter '%s' is not a valid "
                                            "Python variable name. Parameter "
                                            "names must be alphanumeric and "
                                            "start with a letter or "
                                            "underscore." % Name)

        if Required and Default is not None:
            raise IncompetentDeveloperError("Found required parameter '%s' "
                    "with default value '%s'. Required parameters cannot have "
                    "default values." % (Name, Default))

        self.Name = Name
        self.DataType = DataType
        self.Description = Description
        self.Required = Required
        self.Default = Default
        self.DefaultDescription = DefaultDescription

    def _is_valid_name(self, name):
        return name == self._pythonize(name)

    def _pythonize(self, name):
        """Taken from http://stackoverflow.com/a/3303361"""
        # Remove invalid characters.
        name = re.sub('[^0-9a-zA-Z_]', '', name)

        # Remove leading characters until we find a letter or underscore.
        name = re.sub('^[^a-zA-Z_]+', '', name)

        return name

class ParameterCollection(dict):
    """A collection of parameters with dict like lookup"""
    def __init__(self, Parameters):
        self.Parameters = Parameters

        for p in self.Parameters:
            if p.Name in self:
                raise IncompetentDeveloperError("Found duplicate Parameter "
                                                "name '%s'. Parameter names "
                                                "must be unique." % p.Name)
            else:
                self[p.Name] = p

    ### override setattr and contains to throw a more explicit error than
    ### keyerror if a parameter doesn't exist?

class Command(object):
    """Base class for ``Command``

    A ``Command`` is interface agnostic, knows how to run itself and knows 
    about the arguments that it can take (via ``Parameters``).

    """
    BriefDescription = "" # 1 sentence description
    LongDescription = """""" # longer, more detailed description
    Parameters = ParameterCollection([])

    def __init__(self, **kwargs):
        """ """
        self._logger = NullLogger()

    def __call__(self, **kwargs):
        """Safely execute a ``Command``"""
        self_str = str(self.__class__)
        self._logger.info('Starting command: %s' % self_str)
        
        try:
            result = self.run(**kwargs)
        except Exception, e:
            self._logger.fatal('Error executing command: %s' % self_str)
            raise e
        else:
            self._logger.info('Completed command: %s' % self_str)

        # verify the result type
        if not isinstance(result, dict):
            self._logger.fatal('Unsupported result return type for command: '
                               '%s' % self_str)
            raise InvalidReturnTypeError("Unsupported result return type. "
                                         "Results must be stored in a "
                                         "dictionary.")
        return result

    def run(self, **kwargs):
        """Exexcute a ``Command``
        
        A ``Command`` must accept **kwargs to run, and must return a ``dict``
        as a result.
        """
        raise NotImplementedError("All subclasses must implement run.")

def make_parameter_collection_lookup_f(obj):
    """Return a function for convenient parameter lookup.

    ``obj`` should be a Command (sub)class or instance.
    """
    def lookup_f(name):
        return obj.Parameters[name]
    return lookup_f
