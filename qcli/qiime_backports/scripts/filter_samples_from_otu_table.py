#!/usr/bin/env python

from sys import argv, stdout, stderr
from os.path import split, splitext
from qcli.util import qcli_system_call
from qcli.log import StdErrLogger

logger = StdErrLogger()

cmd_name = splitext(split(argv[0])[1])[0]
base_cmd = "qiime %s" % cmd_name 
command = '%s %s' % (base_cmd,' '.join(argv[1:]))

logger.info("This is a new-style QIIME script. You should now call it with: %s" % base_cmd)
logger.info("Calling: %s " % command)

result_stdout, result_stderr, result_retval = qcli_system_call(command)

stdout.write(result_stdout)
stderr.write(result_stderr)

