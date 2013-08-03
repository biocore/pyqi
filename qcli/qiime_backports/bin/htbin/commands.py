#!/usr/bin/env python

from qcli.interface.cli import clmain, cli
import qcli.qiime_backports.qiime.cli as qiime_cli
from qcli.qiime_backports.bin.htbin.util import get_cmd_cfg, format_page_header, format_page_footer

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
