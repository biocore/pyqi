#!/usr/bin/env python

#-----------------------------------------------------------------------------
# Copyright (c) 2013, The BiPy Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------
from __future__ import division

from sys import stderr
from datetime import datetime

__credits__ = ["Greg Caporaso", "Daniel McDonald", "Doug Wendel",
               "Jai Ram Rideout"]

class InvalidLoggerError(Exception):
    pass

class Logger(object):
    """Abstract logging interface"""
    DEBUG = 'DEBUG'
    INFO = 'INFO'
    WARN = 'WARN'
    FATAL = 'FATAL'

    def debug(self, msg):
        """Log at the DEBUG level"""
        self._debug(msg)
        self.flush()

    def info(self, msg):
        """Log at the INFO level"""
        self._info(msg)
        self.flush()

    def warn(self, msg):
        """Log at the WARN level"""
        self._warn(msg)
        self.flush()

    def fatal(self, msg):
        """Log at the FATAL level"""
        self._fatal(msg)
        self.flush()

    def _debug(self, msg):
        raise NotImplementedError("All subclasses must implement debug.")
    
    def _info(self, msg):
        raise NotImplementedError("All subclasses must implement info.")
    
    def _warn(self, msg):
        raise NotImplementedError("All subclasses must implement warn.")
    
    def _fatal(self, msg):
        raise NotImplementedError("All subclasses must implement fatal.")

    def flush(self):
        """Flush buffers as needed"""
        pass

    def _get_timestamp(self):
        """Get an ISO standard timestamp"""
        return datetime.now().isoformat()

    def _format_line(self, level, msg):
        """Construct a logging line"""
        return '%s %s %s' % (self._get_timestamp(), level, msg)

class NullLogger(Logger):
    """Ignore log messages"""
    def _debug(self, msg):
        pass
    def _info(self, msg):
        pass
    def _warn(self, msg):
        pass
    def _fatal(self, msg):
        pass

class StdErrLogger(Logger):
    """Log messages directly to ``stderr``"""
    def _debug(self, msg):
        stderr.write(self._format_line(self.DEBUG, msg) + '\n')

    def _info(self, msg):
        stderr.write(self._format_line(self.INFO, msg) + '\n')

    def _warn(self, msg):
        stderr.write(self._format_line(self.WARN, msg) + '\n')

    def _fatal(self, msg):
        stderr.write(self._format_line(self.FATAL, msg) + '\n')
