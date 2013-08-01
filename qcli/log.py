#!/usr/bin/env python
from __future__ import division

from sys import stderr
from datetime import datetime

__author__ = "Greg Caporaso"
__copyright__ = "Copyright 2013, The QIIME Project"
__credits__ = ["Greg Caporaso", "Daniel McDonald", "Doug Wendel",
               "Jai Ram Rideout"]
__license__ = "GPL"
__version__ = "0.1.0-dev"
__maintainer__ = "Greg Caporaso"
__email__ = "gregcaporaso@gmail.com"

class InvalidLoggerError(Exception):
    pass

class Logger(object):
    DEBUG = 'DEBUG'
    INFO = 'INFO'
    WARN = 'WARN'
    FATAL = 'FATAL'

    def debug(self, msg):
        self._debug(msg)
        self.flush()

    def info(self, msg):
        self._info(msg)
        self.flush()

    def warn(self, msg):
        self._warn(msg)
        self.flush()

    def fatal(self, msg):
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
        pass

    def _get_timestamp(self):
        return datetime.now().isoformat()

    def _format_line(self, level, msg):
        return '%s %s %s' % (self._get_timestamp(), level, msg)

class NullLogger(Logger):
    def _debug(self, msg):
        pass
    def _info(self, msg):
        pass
    def _warn(self, msg):
        pass
    def _fatal(self, msg):
        pass

class StdErrLogger(Logger):
    def _debug(self, msg):
        stderr.write(self._format_line(self.DEBUG, msg) + '\n')

    def _info(self, msg):
        stderr.write(self._format_line(self.INFO, msg) + '\n')

    def _warn(self, msg):
        stderr.write(self._format_line(self.WARN, msg) + '\n')

    def _fatal(self, msg):
        stderr.write(self._format_line(self.FATAL, msg) + '\n')
