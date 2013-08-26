#!/usr/bin/env python

#-----------------------------------------------------------------------------
# Copyright (c) 2013, The BiPy Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------


__author__ = "The BiPy Development Team"
__copyright__ = "Copyright 2013, The BiPy Project"
__credits__ = ["Rob Knight", 
               "Greg Caporaso", 
               "Gavin Huttley", 
               "Daniel McDonald",
               "Jai Ram Rideout"] 
__license__ = "BSD"
__version__ = "0.1.0-dev"
__maintainer__ = "Greg Caporaso"
__email__ = "gregcaporaso@gmail.com"

# import most commonly used objects and functions so they can
# be imported directly from pyqi (e.g., from pyqi import make_option)
from pyqi.option_parsing import (
 make_option, 
 parse_command_line_parameters)
from pyqi.test import (run_script_usage_tests)
from pyqi.util import (pyqi_system_call)

__all__ = ['option_parsing','test','util']
