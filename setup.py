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
__credits__ = ["Rob Knight", "Greg Caporaso", "Jai Ram Rideout",
               "Daniel McDonald", "Doug Wendel"]
__license__ = "BSD"
__version__ = "0.2.0-dev"
__maintainer__ = "Greg Caporaso"
__email__ = "gregcaporaso@gmail.com"

from distutils.core import setup
from glob import glob

# from https://wiki.python.org/moin/PortingPythonToPy3k
try:
    # python 3.x
    from distutils.command.build_py import build_py_2to3 as build_py
except ImportError:
    # python 2.x
    from distutils.command.build_py import build_py

setup(name='pyqi',
      cmdclass={'build_py':build_py},
      version=__version__,
      description='pyqi: expose your interface',
      author=__maintainer__,
      author_email=__email__,
      maintainer=__maintainer__,
      maintainer_email=__email__,
      url='http://bipy.github.io/pyqi',
      packages=['pyqi',
                'pyqi/commands',
                'pyqi/core',
                'pyqi/core/interfaces',
                'pyqi/core/interfaces/optparse',
                'pyqi/interfaces',
                'pyqi/interfaces/optparse',
                'pyqi/interfaces/optparse/config',
                ],
      scripts=glob('scripts/pyqi*'))
