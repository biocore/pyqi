#!/usr/bin/env python

__author__ = "Greg Caporaso"
__copyright__ = "Copyright 2013, The QIIME Project"
__credits__ = ["Greg Caporaso", "Daniel McDonald", "Doug Wendel",
               "Jai Ram Rideout"]
__license__ = "GPL"
__version__ = "0.1.0-dev"
__maintainer__ = "Greg Caporaso"
__email__ = "gregcaporaso@gmail.com"

from __future__ import division

from sys import argv, stdout, stderr
from os.path import split, splitext
from pyqi.util import pyqi_system_call
from pyqi.core.log import StdErrLogger

def old_to_new_qiime_command(local_argv):
    logger = StdErrLogger()

    cmd_name = splitext(split(local_argv[0])[1])[0]
    base_cmd = "qiime %s" % cmd_name 
    command = '%s %s' % (base_cmd,' '.join(local_argv[1:]))

    logger.info("This is a new-style QIIME script. You should now call it with: %s" % base_cmd)
    logger.info("Calling: %s " % command)

    result_stdout, result_stderr, result_retval = pyqi_system_call(command)

    stdout.write(result_stdout)
    stderr.write(result_stderr)
