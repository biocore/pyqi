#!/usr/bin/env python

#-----------------------------------------------------------------------------
# Copyright (c) 2013, The BiPy Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------

__credits__ = ["Evan Bolyen"]

import sys
from unittest import TestCase, main

if sys.version_info.major == 2:
    from StringIO import StringIO
else:
    from io import StringIO

from pyqi.core.exception import IncompetentDeveloperError
from pyqi.core.interfaces.html.input_handler import (load_file_lines,
        load_file_contents)

class HTMLInputHandlerTests(TestCase):
    def setUp(self):
        self.file_like_object = StringIO()
        #Note the whitespace, this tests strip()
        self.file_like_object.write("This is line 1\n")
        self.file_like_object.write(" This is line 2\n")
        self.file_like_object.write("This is line 3 \n")
        #Place it at the beginning of the file again
        self.file_like_object.seek(0)

    def tearDown(self):
        self.file_like_object.close()

    def test_load_file_lines(self):
        """Correctly returns file lines as a list of strings"""
        # can't load a string, etc...
        self.assertRaises(IncompetentDeveloperError, load_file_lines, 'This is not a file')
        result = load_file_lines(self.file_like_object)
        self.assertEqual(result,
                         ["This is line 1",
                          "This is line 2",
                          "This is line 3"])

    def test_load_file_contents(self):
        """Correctly returns file contents"""
        # can't load a string, etc...
        self.assertRaises(IncompetentDeveloperError, load_file_contents, 'This is not a file')

        result = load_file_contents(self.file_like_object)
        #Note the whitespace
        self.assertEqual(result, "This is line 1\n This is line 2\nThis is line 3 \n")

if __name__ == '__main__':
    main()
