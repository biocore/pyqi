#!/usr/bin/env python

#-----------------------------------------------------------------------------
# Copyright (c) 2013, The BiPy Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------

__author__ = "Greg Caporaso"
__copyright__ = "Copyright 2013, The pyqi project"
__credits__ = ["Greg Caporaso", "Daniel McDonald", "Gavin Huttley",
               "Rob Knight", "Doug Wendel", "Jai Ram Rideout",
               "Jose Antonio Navas Molina"]
__license__ = "BSD"
__version__ = "0.2.0-dev"
__maintainer__ = "Greg Caporaso"
__email__ = "gregcaporaso@gmail.com"

import os
import types
import BaseHTTPServer
from copy import copy
from glob import glob
from os.path import abspath, exists, isdir, isfile, split
from pyqi.core.interface import (Interface, InterfaceOption,
                                 InterfaceUsageExample, InterfaceResult, get_command_names)
from pyqi.core.factory import general_factory
from pyqi.core.exception import IncompetentDeveloperError
from pyqi.core.command import Parameter


#This should be a singleton, but python makes that difficult, so lets just pretend.
class HTMLInterface_server(BaseHTTPServer.BaseHTTPRequestHandler):
	def __init__(cmd_cfg_mod, port):
		pass
		




#This will generally be called from a generated command.
def start_server(port):
	"""Start a server for the HTMLInterface on the specified port"""
	return get_command_names('pyqi.interfaces.optparse.config')

def stop_server():
	"""Stop a running server for the HTMLInterface"""
	pass