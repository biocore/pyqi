#!/usr/bin/env python

"""Command line interface input handlers

All input handlers must conform to the following function definittion

function(option_value)
"""
#-----------------------------------------------------------------------------
# Copyright (c) 2013, The BiPy Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------

__credits__ = ["Daniel McDonald", "Greg Caporaso", "Doug Wendel",
               "Jai Ram Rideout"]

def command_handler(option_value):
    """Dynamically load a Python object from a module and return an instance"""
    module, klass = option_value.rsplit('.',1)
    mod = __import__(module, fromlist=[klass])
    return getattr(mod, klass)()

def string_list_handler(option_value=None):
    """Split a comma-separated string into a list of strings."""
    result = None
    if option_value is not None:
        result = option_value.split(',')
    return result

def file_reading_handler(option_value=None):
    """Open a filepath for reading."""
    result = None
    if option_value is not None:
        result = open(option_value, 'U')
    return result

def load_file_lines(option_value):
    """Return a list of strings, one per line in the file.

    Each line will have leading and trailing whitespace stripped from it.
    """
    with open(option_value, 'U') as f:
        return [line.strip() for line in f]

def load_file_contents(option_value):
    """Return the contents of a file as a single string."""
    with open(option_value, 'U') as f:
        return f.read()
