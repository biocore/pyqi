#!/usr/bin/env python

__author__ = "Greg Caporaso"
__copyright__ = "Copyright 2013, The QIIME Project"
__credits__ = ["Greg Caporaso", "Daniel McDonald", "Doug Wendel",
               "Jai Ram Rideout"]
__license__ = "GPL"
__version__ = "0.1.0-dev"
__maintainer__ = "Greg Caporaso"
__email__ = "gregcaporaso@gmail.com"

from qcli.exception import IncompetentDeveloperError

# an option is interface dependent
# a parameter is interface independent

class Interface(object):
    CommandConstructor = None

    def __init__(self, **kwargs):
        """ """
        self.Options = []
        self.CmdInstance = None

        if self.CommandConstructor is None:
            raise IncompetentDeveloperError("I don't have a command constructor, idiot!!!")
    
        self.CmdInstance = self.CommandConstructor(**kwargs)
        for parameter in self.CmdInstance.Parameters:
            option = self._option_factory(parameter)
            self.Options.append(option)
    
    def __call__(self, in_, *args, **kwargs):
        self._the_in_validator(in_)
        parameter_instances = self._input_handler(in_, *args, **kwargs)
        return self._output_handler(self.CmdInstance(parameter_instances))

    def _the_in_validator(self, in_):
        """The job securator"""
        raise NotImplementedError("DO IT!")

    def _option_factory(self):
        raise NotImplementedError("DO IT!")

    def _input_handler(self, in_, *args, **kwargs):
        raise NotImplementedError("DO IT!")

    def _output_handler(self, results):
        raise NotImplementedError("DO IT!")
