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
            raise IncompetentDeveloperError("Required parameters cannot have defaults.")

class Command(object):
    """Base class for ``Command``

    A ``Command`` is interface agnostic, knows how to run itself and knows 
    about the arguments that it can take (via ``Parameters``).
    """
    _logger = None
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
            self._logger.fatal('Shit went down: %s' % self_str)
            raise e
        else:
            self._logger.info('Completed command: %s' % self_str)
       
        # check if the result is sane
        if not isinstance(result, dict):
            self._logger.fatal('Shit went wrong: %s' % self_str)
            raise InvalidReturnTypeError("Unexpected return type!")

        return result

    def run(self, **kwargs):
        """Exexcute a ``Command``
        
        A ``Command`` must accept **kwargs to run, and must return a ``dict``
        as a result.
        """
        raise NotImplementedError("All subclasses must implement run.")
    
    def _get_default_parameters(self):
        return [Parameter(Type=bool,
                          Help='Print information during execution -- useful for debugging',
                          Name='verbose',
                          Required=False,
                          Default=False)]

    def _get_parameters(self):
        raise NotImplementedError("All subclasses must implement _get_parameters")
