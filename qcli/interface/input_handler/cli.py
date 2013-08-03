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

__author__ = "Daniel McDonald"
__copyright__ = "Copyright 2013, The QCLI Project"
__credits__ = ["Daniel McDonald", "Greg Caporaso", "Doug Wendel",
               "Jai Ram Rideout"]
__license__ = "BSD"
__version__ = "0.1-dev"
__maintainer__ = "Daniel McDonald"
__email__ = "mcdonadt@colorado.edu"
__status__ = "Development"

def command_handler(option_value):
    """Dynamically load a Python object from a module and return an instance"""
    module, klass = value.rsplit('.',1)
    mod = __import__(module, fromlist=[klass])
    return getattr(mod, klass)()
