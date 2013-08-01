#!/usr/bin/env python
from __future__ import division

__author__ = "Greg Caporaso"
__copyright__ = "Copyright 2013, The QIIME Project"
__credits__ = ["Greg Caporaso", "Daniel McDonald", "Doug Wendel",
               "Jai Ram Rideout"]
__license__ = "GPL"
__version__ = "0.1.0-dev"
__maintainer__ = "Greg Caporaso"
__email__ = "gregcaporaso@gmail.com"

from qcli.log import StdErrLogger
from qcli.exception import IncompetentDeveloperError

class Parameter(object):
    
    def __init__(self,
                 Type,
                 Help,
                 Name,
                 Required=False,
                 Default=None,
                 DefaultDescription=None):
        self.Type = Type
        self.Help = Help
        self.Default = Default
        self.Name = Name
        self.Required = Required
        self.DefaultDescription = DefaultDescription

        if self.Required and self.Default is not None:
            raise IncompetentDeveloperError("Required parameters cannot have defaults, idiot!!!")

class Command(object):
    """ Base class for abstracted command
    """
    _logger = None
    BriefDescription = ''
    LongDescription = ''

    def __init__(self, **kwargs):
        """ """
        self._logger = StdErrLogger()
        self.Parameters = []
        self.Parameters.extend(self._get_default_parameters())
        self.Parameters.extend(self._get_parameters())

    def __call__(self, **kwargs):
        """
        """
        self_str = str(self.__class__)
        self._logger.info('Starting command: %s' % self_str)
        try:
            result = self.run(**kwargs)
        except Exception, e:
            self._logger.fatal('Shit went down: %s' % self_str)
            raise e
        else:
            self._logger.info('Completed command: %s' % self_str)
        
        if not isinstance(result, dict):
            self._logger.fatal('Shit went wrong: %s' % self_str)
            raise InvalidReturnTypeError("Unexpected return type!")

        return result

    def run(self, **kwargs):
        raise NotImplementedError("All subclasses must implement run.")
    
    def _get_default_parameters(self):
        return [Parameter(Type=bool,
                          Help='Print information during execution -- useful for debugging',
                          Name='verbose',
                          Required=False,
                          Default=False)]

    def _get_parameters(self):
        raise NotImplementedError("All subclasses must implement _get_parameters")
