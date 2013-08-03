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

__author__ = "Daniel McDonald"
__copyright__ = "Copyright 2013, The QCLI Project"
__credits__ = ["Daniel McDonald", "Greg Caporaso", "Doug Wendel",
               "Jai Ram Rideout"]
__license__ = "BSD"
__version__ = "0.1-dev"
__maintainer__ = "Daniel McDonald"
__email__ = "mcdonadt@colorado.edu"
__status__ = "Development"

from qcli.core.exception import IncompetentDeveloperError
import os

def write_string(result_key, data, option_value=None):
    """Write a string to a file"""
    if option_value is None:
        raise IncompetentDeveloperError("Cannot write without a path!")

    if os.path.exists(option_value):
        raise IOError("Output path %s already exists!" % option_value)
    f = open(option_value, 'w')
    f.write(data)
    f.close()
