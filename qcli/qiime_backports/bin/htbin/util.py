#!/usr/bin/env python
import cgi
import importlib

from qcli.interface.cli import cli

CLI_CFG_BASE = 'qcli.qiime_backports.qiime.cli'

def get_cmd_cfg(cmd):
    try:
        cmd_cfg = importlib.import_module('.'.join([CLI_CFG_BASE, cmd]))
    except ImportError, e:
        stderr.write("Unable to import the command configuration!\n")
        exit(1)
    return cmd_cfg

def get_cmd_obj(cmd):
    cmd_cfg = get_cmd_cfg(cmd)
    return cli(cmd_cfg.CommandConstructor, cmd_cfg.usage_examples, 
                  cmd_cfg.param_conversions, cmd_cfg.additional_options)

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
