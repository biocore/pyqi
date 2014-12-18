#!/usr/bin/env python
""" Utilities for parsing command line options and arguments

This code was derived from QIIME (www.qiime.org), where it was initally
developed. It has been ported to qcli to support accessing this functionality 
without those dependencies.

"""

__author__ = "Greg Caporaso"
__copyright__ = "Copyright 2013, The BiPy Project"
__credits__ = ["Greg Caporaso"]
__license__ = "GPL"
__version__ = "0.1.1"
__maintainer__ = "Greg Caporaso"
__email__ = "gregcaporaso@gmail.com"

from os import remove
from subprocess import Popen, PIPE, STDOUT

def qcli_system_call(cmd, shell=True):
    """Call cmd and return (stdout, stderr, return_value).

    cmd can be either a string containing the command to be run, or a sequence
    of strings that are the tokens of the command.

    Please see Python's subprocess. Popen for a description of the shell
    parameter and how cmd is interpreted differently based on its value.
    
    This function is ported from QIIME (previously qiime_system_call).
    """
    proc = Popen(cmd,
                 shell=shell,
                 universal_newlines=True,
                 stdout=PIPE,
                 stderr=PIPE)
    # communicate pulls all stdout/stderr from the PIPEs to 
    # avoid blocking -- don't remove this line!
    stdout, stderr = proc.communicate()
    return_value = proc.returncode
    return stdout, stderr, return_value

def remove_files(list_of_filepaths, error_on_missing=True):
    """Remove list of filepaths, optionally raising an error if any are missing
    
       This function is ported from PyCogent.
    """
    missing = []
    for fp in list_of_filepaths:
        try:
            remove(fp)
        except OSError:
            missing.append(fp)

    if error_on_missing and missing:
        raise OSError, "Some filepaths were not accessible: %s" % '\t'.join(missing)
        