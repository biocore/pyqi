#!/usr/bin/env python

#-----------------------------------------------------------------------------
# Copyright (c) 2013, The BiPy Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------

def general_factory(command_constructor, usage_examples, param_conversions, 
            added_options, output_map, interface=None):
    """Generalized interface factory"""
    class IObject(interface):
        """Dynamic interface object"""
        CommandConstructor = command_constructor
        def _get_param_conv_info(self):
            return param_conversions
        def _get_additional_options(self):
            return added_options
        def _get_usage_examples(self):
            return usage_examples
        def _get_output_map(self):
            return output_map

    return IObject
