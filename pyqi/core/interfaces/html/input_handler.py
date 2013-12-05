#!/usr/bin/env python


#-----------------------------------------------------------------------------
# Copyright (c) 2013, The BiPy Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------

__credits__ = ["Evan Bolyen"]

def load_file_lines(option_value):
    """Return a list of strings, one per line in the file.

    Each line will have leading and trailing whitespace stripped from it.
    """
    return [line.strip() for line in option_value]

def load_file_contents(option_value):
    """Return the contents of a file as a single string."""
    return option_value.read()
