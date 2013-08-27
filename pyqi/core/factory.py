#!/usr/bin/env python

#-----------------------------------------------------------------------------
# Copyright (c) 2013, The BiPy Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------

__author__ = "Daniel McDonald"
__copyright__ = "Copyright 2013, The pyqi project"
__credits__ = ["Greg Caporaso", "Daniel McDonald", "Doug Wendel",
               "Jai Ram Rideout"]
__license__ = "BSD"
__version__ = "0.2.0"
__maintainer__ = "Daniel McDonald"
__email__ = "mcdonadt@colorado.edu"

def general_factory(command_constructor, usage_examples, inputs, outputs,
                    version, interface=None):
    """Generalized interface factory"""
    class IObject(interface):
        """Dynamic interface object"""
        CommandConstructor = command_constructor
        def _get_usage_examples(self):
            return usage_examples
        def _get_inputs(self):
            return inputs
        def _get_outputs(self):
            return outputs
        def _get_version(self):
            return version

    return IObject
