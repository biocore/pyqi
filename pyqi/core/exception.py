#!/usr/bin/env python

#-----------------------------------------------------------------------------
# Copyright (c) 2013, The BiPy Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------

__credits__ = ["Greg Caporaso", "Daniel McDonald", "Doug Wendel",
               "Jai Ram Rideout"]

class CommandError(Exception):
    pass

class IncompetentDeveloperError(CommandError):
    pass

class MissingParameterError(CommandError):
    pass

class InvalidReturnTypeError(IncompetentDeveloperError):
    pass

class UnknownParameterError(IncompetentDeveloperError):
    pass

class MissingVersionInfoError(IncompetentDeveloperError):
    pass
