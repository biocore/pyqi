#!/usr/bin/env python

#-----------------------------------------------------------------------------
# Copyright (c) 2013, The BiPy Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------

"""Utility functionality for the pyqi project."""

__author__ = "Greg Caporaso"
__copyright__ = "Copyright 2013, The pyqi project"
__credits__ = ["Greg Caporaso", "Jai Ram Rideout"]
__license__ = "BSD"
__version__ = "0.2.0-dev"
__maintainer__ = "Greg Caporaso"
__email__ = "gregcaporaso@gmail.com"

from os import remove
from os.path import split, splitext
from sys import stdout, stderr
from subprocess import Popen, PIPE, STDOUT
from pyqi.core.log import StdErrLogger

def pyqi_system_call(cmd, shell=True):
    """Call cmd and return (stdout, stderr, return_value).

    cmd can be either a string containing the command to be run, or a sequence
    of strings that are the tokens of the command.

    Please see Python's subprocess.Popen for a description of the shell
    parameter and how cmd is interpreted differently based on its value.
    
    This function is ported from QIIME (http://www.qiime.org), previously
    named qiime_system_call. QIIME is a GPL project, but we obtained permission
    from the authors of this function to port it to pyqi (and keep it under
    pyqi's BSD license).
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

    This function is ported from PyCogent (http://www.pycogent.org). PyCogent
    is a GPL project, but we obtained permission from the authors of this
    function to port it to pyqi (and keep it under pyqi's BSD license).
    """
    missing = []
    for fp in list_of_filepaths:
        try:
            remove(fp)
        except OSError:
            missing.append(fp)

    if error_on_missing and missing:
        raise OSError, "Some filepaths were not accessible: %s" % '\t'.join(missing)

def old_to_new_command(driver_name, project_title, local_argv):
    """Deprecate an old-style script.

    Will only work if the old-style script name matches a command name, and if
    all option names are the same between old and new.

    Use like this (put in the script you want to deprecate):

        #!/usr/bin/env python
        import sys
        from pyqi.util import old_to_new_command

        sys.exit(old_to_new_command('biom', 'BIOM', sys.argv))
    """
    logger = StdErrLogger()

    cmd_name = splitext(split(local_argv[0])[1])[0]
    base_cmd = "%s %s" % (driver_name, cmd_name)
    command = '%s %s' % (base_cmd, ' '.join(local_argv[1:]))

    logger.info("This is a new-style %s script. You should now call it with: "
                "%s" % (project_title, base_cmd))
    logger.info("Calling: %s " % command)

    result_stdout, result_stderr, result_retval = pyqi_system_call(command)

    stdout.write(result_stdout)
    stderr.write(result_stderr)

    return result_retval
