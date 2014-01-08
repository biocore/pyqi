#!/usr/bin/env python

#-----------------------------------------------------------------------------
# Copyright (c) 2013, The BiPy Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------

__credits__ = ["Evan Bolyen"]

from unittest import TestCase, main
from pyqi.core.interfaces.html.output_handler import (newline_list_of_strings,
        html_list_of_strings)

class HTMLOutputHandlerTests(TestCase):

    def test_newline_list_of_strings(self):
        """Correctly returns a list of strings to delimited by '\n'."""
        result = newline_list_of_strings('foo', ['bar','bay','baz'])
        self.assertEqual(result, 'bar\nbay\nbaz')

    def test_html_list_of_strings(self):
        """Correctly returns a list of strings delimited by '<br/>'."""
        result = html_list_of_strings('foo', ['bar','bay','baz'])
        self.assertEqual(result, 'bar<br/>bay<br/>baz')

if __name__ == '__main__':
    main()
