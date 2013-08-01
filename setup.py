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
__credits__ = ["Rob Knight", "Greg Caporaso", ] 
__license__ = "BSD"
__version__ = "0.1.0-dev"
__maintainer__ = "Greg Caporaso"
__email__ = "gregcaporaso@gmail.com"

from distutils.core import setup
from glob import glob

setup(name='qcli',
      version='0.1.0-dev',
      packages=['qcli'],
      scripts=glob('scripts/qcli*')
      )