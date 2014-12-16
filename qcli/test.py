#!/usr/bin/env python
""" Utilities for parsing command line options and arguments

This code was derived from QIIME (www.qiime.org), where it was initally
developed. It has been ported to qcli to support accessing this functionality 
without those dependencies.

"""

import signal
from os.path import isdir, split, join, abspath, exists
from os import chdir, getcwd
from shutil import copytree, rmtree
from glob import glob
from site import addsitedir
from qcli.util import (qcli_system_call, 
                       remove_files)


__author__ = "Greg Caporaso"
__copyright__ = "Copyright 2013, The BiPy Project"
__credits__ = ["Greg Caporaso"]
__license__ = "GPL"
__version__ = "0.1.1"
__maintainer__ = "Greg Caporaso"
__email__ = "gregcaporaso@gmail.com"

### Code for timing out tests that exceed a time limit
## The test case timing code included in this file is adapted from
## recipes provided at:
##  http://code.activestate.com/recipes/534115-function-timeout/
##  http://stackoverflow.com/questions/492519/timeout-on-a-python-function-call

# to use this, call initiate_timeout(allowed_seconds_per_test) in 
# TestCase.setUp() and then disable_timeout() in TestCase.tearDown()

class TimeExceededError(Exception):
    pass

def initiate_timeout(seconds=60):
    
    def timeout(signum, frame):
        raise TimeExceededError,\
         "Test failed to run in allowed time (%d seconds)." % seconds
    
    signal.signal(signal.SIGALRM, timeout)
    # set the 'alarm' to go off in seconds seconds
    signal.alarm(seconds)

def disable_timeout():
    # turn off the alarm
    signal.alarm(0)

### End code for timing out tests that exceed a time limit

def run_script_usage_tests(test_data_dir,
                           scripts_dir,
                           working_dir,
                           verbose=False,
                           tests=None,
                           failure_log_fp=None,
                           force_overwrite=False,
                           timeout=60):
    """ Test script_usage examples when test data is present in test_data_dir

        Returns a result summary string and the number of script usage
        examples (i.e. commands) that failed.
    """
    # process input filepaths and directories
    test_data_dir = abspath(test_data_dir)
    working_dir = join(working_dir,'script_usage_tests')
    if force_overwrite and exists(working_dir):
        rmtree(working_dir)
    if failure_log_fp != None:
        failure_log_fp = abspath(failure_log_fp)

    if tests == None:
        tests = [split(d)[1] for d in sorted(glob('%s/*' % test_data_dir)) if isdir(d)]
    
    if verbose:
        print 'Tests to run:\n %s' % ' '.join(tests)
    
    addsitedir(scripts_dir)
    
    failed_tests = []
    warnings = []
    total_tests = 0
    for test in tests:
        
        # import the usage examples - this is possible because we added 
        # scripts_dir to the PYTHONPATH above
        script_fn = '%s/%s.py' % (scripts_dir,test)
        script = __import__(test)
        usage_examples = script.script_info['script_usage']
        
        if verbose:
            print 'Testing %d usage examples from: %s' % (len(usage_examples),script_fn)
        
        # init the test environment
        test_input_dir = '%s/%s' % (test_data_dir,test)
        test_working_dir = '%s/%s' % (working_dir,test)
        copytree(test_input_dir,test_working_dir)
        chdir(test_working_dir)
        
        # remove pre-exisitng output files if any
        try:
            script_usage_output_to_remove = script.script_info['script_usage_output_to_remove']
        except KeyError:
            script_usage_output_to_remove = []
        for e in script_usage_output_to_remove:
            rmtree(e.replace('$PWD',getcwd()),ignore_errors=True)
            remove_files([e.replace('$PWD',getcwd())],error_on_missing=False)
        
        if verbose:
            print ' Running tests in: %s' % getcwd()
            print ' Tests:'
        
        for usage_example in usage_examples:
            if '%prog' not in usage_example[2]:
                warnings.append('%s usage examples do not all use %%prog to represent the command name. You may not be running the version of the command that you think you are!' % test)
            cmd = usage_example[2].replace('%prog',script_fn)
            if verbose:
                print '  %s' % cmd,
            
            timed_out = False
            initiate_timeout(timeout)
            try:
                stdout, stderr, return_value = qcli_system_call(cmd)
            except TimeExceededError:
                timed_out = True
            else:
                disable_timeout()
            
            total_tests += 1
            if timed_out:
                # Add a string instead of return_value - if fail_tests ever ends
                # up being returned from this function we'll want to code this as 
                # an int for consistency in the return value type.
                failed_tests.append((cmd, "", "", "None, time exceeded"))
                if verbose: print ": Timed out"
            elif return_value != 0:
                failed_tests.append((cmd, stdout, stderr, return_value))
                if verbose: print ": Failed"
            else:
                pass
                if verbose: print ": Pass"
        
        if verbose:
            print ''
            
    if failure_log_fp:
        failure_log_f = open(failure_log_fp,'w')
        if len(failed_tests) == 0:
            failure_log_f.write('All script interface tests passed.\n')
        else:
            i = 1
            for cmd, stdout, stderr, return_value in failed_tests:
                failure_log_f.write('**Failed test %d:\n%s\n\nReturn value: %s\n\nStdout:\n%s\n\nStderr:\n%s\n\n' % (i,cmd,str(return_value), stdout, stderr))
                i += 1
        failure_log_f.close()
    
    
    if warnings:
        print 'Warnings:'
        for warning in warnings:
            print ' ' + warning
        print ''
    
    result_summary = 'Ran %d commands to test %d scripts. %d of these commands failed.' % (total_tests,len(tests),len(failed_tests))
    if len(failed_tests) > 0:
        failed_scripts = set([split(e[0].split()[0])[1] for e in failed_tests])
        result_summary += '\nFailed scripts were: %s' % " ".join(failed_scripts)
    if failure_log_fp:
        result_summary += "\nFailures are summarized in %s" % failure_log_fp
    
    rmtree(working_dir)
    
    return result_summary, len(failed_tests)
