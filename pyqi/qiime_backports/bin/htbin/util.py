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
from sys import stderr
import cgi
import importlib
from pyqi.interface.cli import cli

CLI_CFG_BASE = 'pyqi.qiime_backports.qiime.cli'

def get_cmd_cfg(cmd):
    try:
        cmd_cfg = importlib.import_module('.'.join([CLI_CFG_BASE, cmd]))
    except ImportError, e:
        stderr.write("Unable to import the command configuration.\n")
        stderr.write(traceback.format_exc())
        exit(1)
    return cmd_cfg

def get_cmd_obj(cmd):
    cmd_cfg = get_cmd_cfg(cmd)
    return cli(cmd_cfg.CommandConstructor, cmd_cfg.usage_examples, 
                  cmd_cfg.param_conversions, cmd_cfg.additional_options, cmd_cfg.output_map)

def format_page_header():
    return """Content-type: text/html

    <html>
        <head>
            <title>Fooooooooo</title>
            <link rel='stylesheet' href='../style/qiime.css' type='text/css' />
        </head>
        <body>
    """

def format_page_footer():
    return "</body></html>"

