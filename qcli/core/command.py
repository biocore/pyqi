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

from qcli.core.log import NullLogger
from qcli.core.exception import (IncompetentDeveloperError,
                                 InvalidReturnTypeError)

class Parameter(object):
    """A ``Command`` variable

    A ``Command`` variable is interface agnostic and are analogous to a 
    function argument.
    """
    def __init__(self, Type, Help, Name, Required=False, Default=None,
                 DefaultDescription=None):
        self.Type = Type
        self.Help = Help
        self.Default = Default
        self.Name = Name
        self.Required = Required
        self.DefaultDescription = DefaultDescription

        if self.Required and self.Default is not None:
            raise IncompetentDeveloperError("Found required parameter '%s' "
                    "with default value '%s'. Required parameters cannot have "
                    "default values." % (self.Name, self.Default))

class Command(object):
    """Base class for ``Command``

    A ``Command`` is interface agnostic, knows how to run itself and knows 
    about the arguments that it can take (via ``Parameters``).
    """
    BriefDescription = "" # 1 sentence description
    LongDescription = """""" # longer, more detailed description

    def __init__(self, **kwargs):
        """ """
        self._logger = NullLogger()
        self.Parameters = []
        self.Parameters.extend(self._get_default_parameters())
        self.Parameters.extend(self._get_parameters())

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

    def _get_default_parameters(self):
        return [Parameter(Type=bool,
                          Help='Print information during execution -- useful '
                               'for debugging',
                          Name='verbose',
                          Required=False,
                          Default=False)]

    def _get_parameters(self):
        """Return a list of Parameters for the Command"""
        raise NotImplementedError("All subclasses must implement "
                                  "_get_parameters.")
