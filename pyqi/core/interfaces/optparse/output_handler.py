#!/usr/bin/env python

"""Command line interface output handlers

All output handlers must conform to the following function definition

function(result_key, data, option_value=None)

result_key   - the corresponding key in the results dictionary
data         - the actual results
option_value - if the handler is tied to an output option, the value of that
               option is represented here
"""

#-----------------------------------------------------------------------------
# Copyright (c) 2013, The BiPy Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------

__credits__ = ["Daniel McDonald", "Greg Caporaso", "Doug Wendel",
               "Jai Ram Rideout", "Evan Bolyen"]

from pyqi.core.exception import IncompetentDeveloperError
import os

def write_string(result_key, data, option_value=None):
    """Write a string to a file.
    
    A newline will be added to the end of the file.
    """
    if option_value is None:
        raise IncompetentDeveloperError("Cannot write output without a "
                                        "filepath.")

    if os.path.exists(option_value):
        raise IOError("Output path '%s' already exists." % option_value)

    with open(option_value, 'w') as f:
        f.write(data)
        f.write('\n')

def write_list_of_strings(result_key, data, option_value=None):
    """Write a list of strings to a file, one per line.
    
    A newline will be added to the end of the file.
    """
    if option_value is None:
        raise IncompetentDeveloperError("Cannot write output without a "
                                        "filepath.")

    if os.path.exists(option_value):
        raise IOError("Output path '%s' already exists." % option_value)

    with open(option_value, 'w') as f:
        for line in data:
            f.write(line)
            f.write('\n')

def print_list_of_strings(result_key, data, option_value=None):
    """Print a list of strings to stdout, one per line.

    ``result_key`` and ``option_value`` are ignored.
    """
    for line in data:
        print line

def print_string(result_key, data, option_value=None):
    """Print the string

    A newline will be printed before the data"""
    print ""
    print data
