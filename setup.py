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
__version__ = '0.2.0-dev'
__maintainer__ = "Greg Caporaso"
__email__ = "gregcaporaso@gmail.com"

#from distutils.core import setup
from setuptools import Command, setup
from glob import glob
import sys

# from https://wiki.python.org/moin/PortingPythonToPy3k
try:
    # python 3.x
    from distutils.command.build_py import build_py_2to3 as build_py
except ImportError:
    # python 2.x
    from distutils.command.build_py import build_py

# classes/classifiers code adapted from Celery:
# https://github.com/celery/celery/blob/master/setup.py
#
# PyPI's list of classifiers can be found here:
# https://pypi.python.org/pypi?%3Aaction=list_classifiers
classes = """
    Development Status :: 4 - Beta
    License :: OSI Approved :: BSD License
    Topic :: Software Development :: Libraries :: Application Frameworks
    Topic :: Software Development :: User Interfaces 
    Programming Language :: Python
    Programming Language :: Python :: 2.7
    Programming Language :: Python :: Implementation :: CPython
    Operating System :: OS Independent
    Operating System :: POSIX
    Operating System :: MacOS :: MacOS X
"""
classifiers = [s.strip() for s in classes.split('\n') if s]

# Verify Python version
ver = '.'.join(map(str, [sys.version_info.major, sys.version_info.minor]))
if ver not in ['2.7']:
    sys.stderr.write("Only Python >=2.7 and <3.0 is supported.")
    sys.exit(1)

long_description = """pyqi (canonically pronounced pie chee) is a Python framework designed to support wrapping general commands in multiple types of interfaces, including at the command line, HTML, and API levels."""

setup(name='pyqi',
      cmdclass={'build_py':build_py},
      version=__version__,
      license=__license__,
      description='pyqi: expose your interface',
      long_description=long_description,
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
                'pyqi/core/interfaces/html',
                'pyqi/interfaces',
                'pyqi/interfaces/optparse',
                'pyqi/interfaces/html',
                'pyqi/interfaces/optparse/config',
                'pyqi/interfaces/html/config',
                ],
      scripts=glob('scripts/pyqi*'),
      install_requires=[],
      extras_require={'test':["nose >= 0.10.1",
                              "tox >= 1.6.1"],
                      'doc':"Sphinx >= 0.3"
                     },
      classifiers=classifiers
      )
