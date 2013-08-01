#!/usr/bin/env python

def general_factory(command_constructor, usage_examples, param_conversions, 
            added_options, interface=None):
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
    return IObject
