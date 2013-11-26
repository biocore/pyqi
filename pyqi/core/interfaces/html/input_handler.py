#!/usr/bin/env python


#-----------------------------------------------------------------------------
# Copyright (c) 2013, The BiPy Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------

__author__ = "Evan Bolyen"
__copyright__ = "Copyright 2013, The pyqi project"
__credits__ = ["Evan Bolyen", "Daniel McDonald"]
__license__ = "BSD"
__version__ = "0.2.0-dev"
__maintainer__ = "Evan Bolyen"
__email__ = "ebolyen@gmail.com"

#Taken from optparse input_handler.py
def string_list_handler(option_value=None):
    """Split a comma-separated string into a list of strings."""
    result = None
    if option_value is not None:
        result = option_value.split(',')
    return result

#Taken from optparse input_handler.py
def command_handler(option_value):
    """Dynamically load a Python object from a module and return an instance"""
    module, klass = option_value.rsplit('.',1)
    mod = __import__(module, fromlist=[klass])
    return getattr(mod, klass)()



def string_to_true_false(option_value):
	"""Return a boolean from a string"""
	return bool(option_value)