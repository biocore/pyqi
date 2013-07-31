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

from datetime import datetime
from sys import stderr

def clmain(cmd_constructor, argv, logger_constructor=StdErrLogger):
    kwargs = argv_to_kwargs(cmd_constructor, argv)

    logger = logger_constructor()
    cmd = cmd_constructor(logger)
    try:
        result = cmd(kwargs)
    except Exception, e:
        # Possibly do *something*
        raise e
    else:
        output_mapping = cmd.getOutputFilepaths(result, kwargs)

        for k, v in result.items():
            v.write(output_mapping[k])

    return 0

def argv_to_kwargs(cmd, argv):
    pass

class CommandError(Exception):
    pass

class InvalidLoggerError(CommandError):
    pass

class IncompetentDeveloperError(CommandError):
    pass

class InvalidReturnTypeError(IncompetentDeveloperError):
    pass

class Logger(object):
    DEBUG = 'DEBUG'
    INFO = 'INFO'
    WARN = 'WARN'
    FATAL = 'FATAL'

    def debug(self, msg):
        self._debug(msg)
        self.flush()

    def info(self, msg):
        self._info(msg)
        self.flush()

    def warn(self, msg):
        self._warn(msg)
        self.flush()

    def fatal(self, msg):
        self._fatal(msg)
        self.flush()

    def _debug(self, msg):
        raise NotImplementedError("All subclasses must implement debug.")
    def _info(self, msg):
        raise NotImplementedError("All subclasses must implement info.")
    def _warn(self, msg):
        raise NotImplementedError("All subclasses must implement warn.")
    def _fatal(self, msg):
        raise NotImplementedError("All subclasses must implement fatal.")

    def flush(self):
        pass

    def _get_timestamp(self):
        return datetime.now().isoformat()

    def _format_line(self, level, msg):
        return '%s %s %s' % (self._get_timestamp(), level, msg)

class NullLogger(Logger):
    def _debug(self, msg):
        pass
    def _info(self, msg):
        pass
    def _warn(self, msg):
        pass
    def _fatal(self, msg):
        pass

class StdErrLogger(Logger):
    def _debug(self, msg):
        stderr.write(self._format_line(self.DEBUG, msg) + '\n')

    def _info(self, msg):
        stderr.write(self._format_line(self.INFO, msg) + '\n')

    def _warn(self, msg):
        stderr.write(self._format_line(self.WARN, msg) + '\n')

    def _fatal(self, msg):
        stderr.write(self._format_line(self.FATAL, msg) + '\n')

class Command(object):
    """ Base class for abstracted command
    """

    BriefDescription = ''
    LongDescription = ''
    StandardParameters = {}
    RequiredParameters = []
    OptionalParameters = []

    def __init__(self, logger, **kwargs):
        """
        """
        if logger is None:
            raise InvalidLoggerError("A logger was not provided.")

        self._logger = logger

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

class FilterSamplesFromOTUTable(Command):
    BriefDescription = "Filters samples from an OTU table on the basis of the number of observations in that sample, or on the basis of sample metadata. Mapping file can also be filtered to the resulting set of sample ids."
    LongDescription = ''
    RequiredParameters = ['biom_table']
    OptionalParameters = ['sample_metadata', 'output_mapping_fp', 'sample_id_map', 'valid_states', 'min_count', 'max_count']

    def run(self, **kwargs):
        pass

class CLCommand(object):
    UsageExamples = []
    StandardParameters = {}
    # Need to figure out logging...
    StandardParameters['log_fp'] = None
    StandardParameters['verbose'] = False

    SuppressVerbose = False
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

    def parse_command_line_parameters(**kwargs):
        """ Constructs the OptionParser object and parses command line arguments
        
            parse_command_line_parameters takes a dict of objects via kwargs which
             it uses to build command line interfaces according to standards 
             developed in the Knight Lab, and enforced in QIIME. The currently 
             supported options are listed below with their default values. If no 
             default is provided, the option is required.
            
            script_description
            script_usage = [("","","")]
            version
            required_options=None
            optional_options=None
            suppress_verbose=False
            disallow_positional_arguments=True
            help_on_no_arguments=True
            optional_input_line = '[] indicates optional input (order unimportant)'
            required_input_line = '{} indicates required input (order unimportant)'
            
           These values can either be passed directly, as:
            parse_command_line_parameters(script_description="My script",\
                                         script_usage=[('Print help','%prog -h','')],\
                                         version=1.0)
                                         
           or they can be passed via a pre-constructed dict, as:
            d = {'script_description':"My script",\
                 'script_usage':[('Print help','%prog -h','')],\
                 'version':1.0}
            parse_command_line_parameters(**d)
        
        """
        # command_line_text will usually be nothing, but can be passed for
        # testing purposes

        # Do we need this? Was used for testing
        #command_line_args = set_parameter('command_line_args',kwargs,None)
        
        # Build the usage and version strings
        usage = self._build_usage_lines()
        version = 'Version: %prog ' + __version__

        # Instantiate the command line parser object
        parser = OptionParser(usage=usage, version=version)

        # What does this do?
        #parser.exit = set_parameter('exit_func',kwargs,parser.exit)
        
        # If no arguments were provided, print the help string (unless the
        # caller specified not to)
        if self.HelpOnNoArguments and (not command_line_args) and len(sys.argv) == 1:
            parser.print_usage()
            return parser.exit(-1)

        
        # Process the required options
        if required_options:
            # Define an option group so all required options are
            # grouped together, and under a common header
            required = OptionGroup(parser, "REQUIRED options",
             "The following options must be provided under all circumstances.")
            for ro in required_options:
                # if the option doesn't already end with [REQUIRED], 
                # add it.
                if not ro.help.strip().endswith('[REQUIRED]'):
                    ro.help += ' [REQUIRED]'
                required.add_option(ro)
            parser.add_option_group(required)

        # Add a verbose parameter (if the caller didn't specify not to)
        if not suppress_verbose:
            parser.add_option('-v','--verbose',action='store_true',\
               dest='verbose',help='Print information during execution '+\
               '-- useful for debugging [default: %default]',default=False)

        # Add the optional options
        map(parser.add_option,optional_options)
        
        # Parse the command line
        # command_line_text will None except in test cases, in which 
        # case sys.argv[1:] will be parsed
        opts,args = parser.parse_args(command_line_args)
        
        # If positional arguments are not allowed, and any were provided,
        # raise an error.
        if disallow_positional_arguments and len(args) != 0:
            parser.error("Positional argument detected: %s\n" % str(args[0]) +\
             " Be sure all parameters are identified by their option name.\n" +\
             " (e.g.: include the '-i' in '-i INPUT_DIR')")

        # Test that all required options were provided.
        if required_options:
            required_option_ids = [o.dest for o in required.option_list]
            for required_option_id in required_option_ids:
                if getattr(opts,required_option_id) == None:
                    return parser.error('Required option --%s omitted.' \
                                 % required_option_id)
                
        # Return the parser, the options, and the arguments. The parser is returned
        # so users have access to any additional functionality they may want at 
        # this stage -- most commonly, it will be used for doing custom tests of 
        # parameter values.
        return parser, opts, args

    def _build_usage_lines(self):
        """ Build the usage string from components 
        """
        line1 = 'usage: %prog [options] ' + '{%s}' %\
         ' '.join(['%s %s' % (str(ro),ro.dest.upper())\
                   for ro in self.RequiredOptions])
        usage_examples = []
        for title, description, command in self.UsageExamples:
            title = title.strip(':').strip()
            description = description.strip(':').strip()
            command = command.strip()
            if title:
                usage_examples.append('%s: %s\n %s' %\
                 (title,description,command))
            else:
                usage_examples.append('%s\n %s' % (description,command))
        usage_examples = '\n\n'.join(usage_examples)
        lines = (line1,
                 '', # Blank line
                 self.OptionalInputLine,
                 self.RequiredInputLine,
                 '', # Blank line
                 self.LongDescription,
                 '', # Blank line
                 'Example usage: ',\
                 'Print help message and exit',
                 ' %prog -h\n',
                 usage_examples)
        return '\n'.join(lines)


class CLFilterSamplesFromOTUTable(FilterSamplesFromOTUTable, CLCommand):
    UsageExamples = []
    UsageExamples.append(("Abundance filtering (low coverage)","Filter samples with fewer than 150 observations from the otu table.","%prog -i otu_table.biom -o otu_table_no_low_coverage_samples.biom -n 150"))
    UsageExamples.append(("Abundance filtering (high coverage)","Filter samples with greater than 149 observations from the otu table.","%prog -i otu_table.biom -o otu_table_no_high_coverage_samples.biom -x 149"))
    UsageExamples.append(("Metadata-based filtering (positive)","Filter samples from the table, keeping samples where the value for 'Treatment' in the mapping file is 'Control'","%prog -i otu_table.biom -o otu_table_control_only.biom -m map.txt -s 'Treatment:Control'"))
    UsageExamples.append(("Metadata-based filtering (negative)","Filter samples from the table, keeping samples where the value for 'Treatment' in the mapping file is not 'Control'","%prog -i otu_table.biom -o otu_table_not_control.biom -m map.txt -s 'Treatment:*,!Control'"))
    UsageExamples.append(("List-based filtering","Filter samples where the id is listed in samples_to_keep.txt","%prog -i otu_table.biom -o otu_table_samples_to_keep.biom --sample_id_fp samples_to_keep.txt"))

    RequiredParameters.append('output_fp')

    ParameterMapping = {}
    ParameterMapping['biom_table'] = make_option('-i','--input_fp',type="existing_filepath", help='the input otu table filepath in biom format')
    ParameterMapping['output_fp'] = make_option('-o','--output_fp',type="new_filepath", help='the output filepath in biom format')
    ParameterMapping['mapping_fp'] = make_option('-m', '--mapping_fp', type='existing_filepath', help='path to the map file [default: %default]')
    ParameterMapping['output_mapping_fp'] = make_option('--output_mapping_fp', type='new_filepath', help='path to write filtered mapping file [default: filtered mapping file is not written]')
    ParameterMapping['sample_id_fp'] = make_option('--sample_id_fp', type='existing_filepath', help='path to file listing sample ids to keep [default: %default]')
    ParameterMapping['valid_states'] = make_option('-s', '--valid_states', type='string', help="string describing valid states (e.g. 'Treatment:Fasting') [default: %default]")
    ParameterMapping['min_count'] = make_option('-n', '--min_count', type='int', default=0, help="the minimum total observation count in a sample for that sample to be retained [default: %default]")
    ParameterMapping['max_count'] = make_option('-x', '--max_count', type='int', default=inf, help="the maximum total observation count in a sample for that sample to be retained [default: infinity]")


    def getOutputFilepaths(results, **kwargs):
        mapping = {}

        for k,v in results.items():
            if isinstance(v, FilePath):
                output_fp = str(v)
            else:
                # figure out filepath
                pass

            mapping[k] = output_fp

        return mapping
