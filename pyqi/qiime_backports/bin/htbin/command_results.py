#!/usr/bin/env python

__author__ = "Jai Ram Rideout"
__copyright__ = "Copyright 2013, The QIIME Project"
__credits__ = ["Greg Caporaso", "Daniel McDonald", "Doug Wendel",
               "Jai Ram Rideout"]
__license__ = "GPL"
__version__ = "0.1.0-dev"
__maintainer__ = "Jai Ram Rideout"
__email__ = "jai.rideout@gmail.com"

import cgi

from qcli.interface.cli import cli
from qcli.qiime_backports.bin.htbin.util import (get_cmd_obj,
                                                 format_page_header,
                                                 format_page_footer)

form = cgi.FieldStorage()
cmd_name = form.getvalue('command')
cmd_interface_class = get_cmd_obj(cmd_name)
cmd = cmd_interface_class.CommandConstructor()

cmd_input = {}
prefix = 'qiime_parameter_'
prefix_len = len(prefix)
for param_name in form:
    param_value = form[param_name]
    if not param_name.startswith(prefix):
        continue

    param_name = param_name[prefix_len:]
    cmd_input[param_name] = param_value

results = cmd(**cmd_input)
 
print format_page_header()
print "<h2>%s</h2>" % cmd_name
print "<pre>{0}</pre>".format(results)
print format_page_footer()
