#!/usr/bin/env python

__author__ = "Jai Ram Rideout"
__copyright__ = "Copyright 2013, The QIIME Project"
__credits__ = ["Greg Caporaso", "Daniel McDonald", "Doug Wendel",
               "Jai Ram Rideout"]
__license__ = "GPL"
__version__ = "0.1.0-dev"
__maintainer__ = "Jai Ram Rideout"
__email__ = "jai.rideout@gmail.com"

from pyqi.interface.cli import clmain, cli
import pyqi.qiime_backports.qiime.cli as qiime_cli
from pyqi.qiime_backports.bin.htbin.util import (get_cmd_cfg,
                                                 format_page_header,
                                                 format_page_footer)

print format_page_header()
print "<p>I know about these QIIME commands:</p>"
print "<table border='1'>"

for c in sorted(qiime_cli.__all__):
    cmd_cfg = get_cmd_cfg(c)
    desc = cmd_cfg.CommandConstructor.BriefDescription
    print "<tr>"
    print "<td><a href='run_command.py?command={0}'>{0}</td><td>{1}</td>".format(c, desc)
    print "</tr>"

print "</table>"
print format_page_footer()
