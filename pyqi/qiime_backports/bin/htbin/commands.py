#!/usr/bin/env python

__author__ = "Jai Ram Rideout"
__copyright__ = "Copyright 2013, The QIIME Project"
__credits__ = ["Greg Caporaso", "Daniel McDonald", "Doug Wendel",
               "Jai Ram Rideout"]
__license__ = "GPL"
__version__ = "0.1.0-dev"
__maintainer__ = "Jai Ram Rideout"
__email__ = "jai.rideout@gmail.com"

import traceback
from pyqi.interface.cli import clmain, cli
import pyqi.qiime_backports.qiime.cli as qiime_cli
from pyqi.qiime_backports.bin.htbin.util import (get_cmd_cfg,
                                                 format_page_header,
                                                 format_page_footer)

print format_page_header()
print "<h2>List of QIIME commands:</h2>"
print "<table>"

for c in qiime_cli.__all__:
	try:
	    cmd_cfg = get_cmd_cfg(c)
	    desc = cmd_cfg.CommandConstructor.BriefDescription
	    print "<tr>"
	    print "<td><a href='run_command.py?command={0}'>{0}</td><td>{1}</td>".format(c, desc)
	    print "</tr>"
	except Exception, e:
		print '<pre>{0}</pre>'.format(traceback.format_exc())

print "</table>"
print format_page_footer()
