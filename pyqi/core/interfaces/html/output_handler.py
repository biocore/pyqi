#!/usr/bin/env python


#-----------------------------------------------------------------------------
# Copyright (c) 2013, The BiPy Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------

__credits__ = ["Evan Bolyen"]

def newline_list_of_strings(result_key, data, option_value=None):
    """Return a string from a list of strings while appending newline"""
    return "\n".join(data)
