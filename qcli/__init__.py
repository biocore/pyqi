#!/usr/bin/env python

__author__ = "The BiPy Development Team"
__copyright__ = "Copyright 2013, The BiPy Project"
__credits__ = ["Rob Knight", 
               "Greg Caporaso", 
               "Gavin Huttley", 
               "Daniel McDonald",
               "Jai Ram Rideout"] 
__license__ = "GPL"
__version__ = "0.1.1"
__maintainer__ = "Greg Caporaso"
__email__ = "gregcaporaso@gmail.com"

# import most commonly used objects and functions so they can
# be imported directly from qlci (e.g., from qcli import make_option)
from qcli.option_parsing import (
 make_option, 
 parse_command_line_parameters)
from qcli.test import (run_script_usage_tests)
from qcli.util import (qcli_system_call)

__all__ = ['option_parsing','test','util']
