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

from numpy import inf
from datetime import datetime
from sys import stderr
import sys
from optparse import (OptionParser, OptionGroup, Option, 
                      OptionValueError, OptionError)
from qcli.option_parsing import make_option
from qcli.log import StdErrLogger
from qcli.exception import CommandError, IncompetentDeveloperError

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

class CLOption(Parameter):
    
    def __init__(self, Type, Help, Name, LongName, CLType, CLAction='store',
                 Required=False, Default=None, DefaultDescription=None,
                 ShortName=None):
        self.LongName = LongName
        self.CLType = CLType
        self.CLAction = CLAction
        self.ShortName = ShortName
        
        super(CLOption,self).__init__(Type=Type,Help=Help,Name=Name,Required=Required,Default=Default,DefaultDescription=DefaultDescription)
        
        if LongName != self.Name:
            self.DepWarn = "parameter %s will be renamed %s in QIIME 2.0.0" % (self.LongName, self.Name)
        else:
            self.DepWarn = ""

    def __str__(self):
        return '-%s/--%s' % (self.ShortName, self.LongName)
        
    @classmethod
    def fromParameter(cls, parameter, LongName, CLType, CLAction='store',
                      ShortName=None):
        result = cls(Type=parameter.Type,
                     Help=parameter.Help,
                     Name=parameter.Name,
                     Required=parameter.Required,
                     LongName=LongName,
                     CLType=CLType,
                     CLAction=CLAction,
                     Default=parameter.Default,
                     DefaultDescription=parameter.DefaultDescription,
                     ShortName=ShortName)
        return result

class Command(object):
    """ Base class for abstracted command
    """
    _logger = None
    BriefDescription = ''
    LongDescription = ''

    def __init__(self, **kwargs):
        """ """
        self._logger = StdErrLogger
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

class FilterSamplesFromOTUTable(Command):
    BriefDescription = "Filters samples from an OTU table on the basis of the number of observations in that sample, or on the basis of sample metadata. Mapping file can also be filtered to the resulting set of sample ids."
    LongDescription = ''

    def __init__(self, **kwargs):
        super(FilterSamplesFromOTUTable, self).__init__(**kwargs)

    def _get_parameters(self):
        return [
                Parameter(Type='biom-table',Help='the input otu table',Name='biom-table', Required=True),
                Parameter(Type=float,Help='the minimum total observation count in a sample for that sample to be retained',Name='min-count', Default=0),
                Parameter(Type=float,Help='the maximum total observation count in a sample for that sample to be retained',Name='max-count', Default=inf,DefaultDescription='infinity')]
    
    def run(self, **kwargs):
        print self.Parameters

class CLCommandParser(object):
    DisallowPositionalArguments = True
    HelpOnNoArguments = True
    OptionalInputLine = '[] indicates optional input (order unimportant)'
    RequiredInputLine = '{} indicates required input (order unimportant)'

    def __init__(self):
        if len(self.UsageExamples) < 1:
            raise IncompetentDeveloperError("How the fuck do I use this "
                                            "command?")

    def getOutputFilepaths(results, **kwargs):
        raise NotImplementedError("All subclasses must implement "
                                  "getOutputFilepaths.")

def build_usage_lines(required_params, usage_examples, optional_input_line, 
                      required_input_line, long_description):
    """ Build the usage string from components """
    line1 = 'usage: %prog [options] ' + '{%s}' %\
     ' '.join(['%s %s' % (str(rp),rp.Name.upper())\
               for rp in required_params])
    
    formatted_usage_examples = []
    for title, description, command in usage_examples:
        title = title.strip(':').strip()
        description = description.strip(':').strip()
        command = command.strip()
        if title:
            formatted_usage_examples.append('%s: %s\n %s' %\
             (title,description,command))
        else:
            formatted_usage_examples.append('%s\n %s' % (description,command))
    
    formatted_usage_examples = '\n\n'.join(formatted_usage_examples)
    
    lines = (line1,
             '', # Blank line
             optional_input_line,
             required_input_line,
             '', # Blank line
             long_description,
             '', # Blank line
             'Example usage: ',\
             'Print help message and exit',
             ' %prog -h\n',
             formatted_usage_examples)
    
    return '\n'.join(lines)

