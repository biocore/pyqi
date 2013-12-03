#!/usr/bin/env python
from __future__ import division

#-----------------------------------------------------------------------------
# Copyright (c) 2013, The BiPy Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------

"""
    make-release
    ~~~~~~~~~~~~

    This code is adapted from the Flask project
    (https://raw.github.com/mitsuhiko/flask/)

    :copyright: (c) 2011 by Armin Ronacher.
    :license: BSD, see Flask's LICENSE file for more details.

"""

__credits__ = ["Daniel McDonald", " Armin Ronacher"]

import importlib
import sys
import os
import re
from datetime import datetime, date
from pyqi.util import pyqi_system_call
from pyqi.core.command import (Command, CommandIn, CommandOut, 
    ParameterCollection)

class MakeRelease(Command):
    BriefDescription = "Make the release"
    LongDescription = "Do all the things for a release"
    CommandIns = ParameterCollection([
        CommandIn(Name='package_name', DataType=str,
                  Description='The name of the package to release', 
                  Required=True),
        CommandIn(Name='real_run', DataType=bool, 
                  Description='Perform a real run', Required=False,
                  Default=False)
    ])
    
    CommandOuts = ParameterCollection([])
    RealRun = False
    _date_clean_re = re.compile(r'(\d+)(st|nd|rd|th)')

    def _parse_changelog(self):
        with open('ChangeLog.md') as f:
            lineiter = iter(f)
            for line in lineiter:
                match = re.search('^pyqi\s+(.*)', line.strip())
                if match is None:
                    continue
                length = len(match.group(1))
                version = match.group(1).strip()
                if lineiter.next().count('-') != len(match.group(0)):
                    continue
                while 1:
                    change_info = lineiter.next().strip()
                    if change_info:
                        break

                match = re.search(r'released on (\w+\s+\d+\w+\s+\d+)', change_info)
                if match is None:
                    continue

                datestr = match.group(1)
                return version, self._parse_date(datestr)

    def _bump_version(self, version):
        try:
            parts = map(int, version.split('.'))
        except ValueError:
            self._fail('Current version is not numeric')
        parts[-1] += 1
        return '.'.join(map(str, parts))

    def _parse_date(self, string):
        string = self._date_clean_re.sub(r'\1', string)
        return datetime.strptime(string, '%B %d %Y')

    def _set_filename_version(self,filename,version_number,pattern):
        changed = []
        def inject_version(match):
            before, old, after = match.groups()
            changed.append(True)
            return before + version_number + after
        with open(filename) as f:
            contents = re.sub(r"""^(\s*%s\s*=\s*(?:'|"))(.+?)((?:'|"))(?sm)""" % 
                    pattern, inject_version, f.read())

        if not changed:
            self._fail('Could not find %s in %s', pattern, filename)

        if self.RealRun:
            with open(filename, 'w') as f:
                f.write(contents)

    def _set_init_version(self, pkg_name, version):
        self._info('Setting __init__.py version to %s', version)
        self._set_filename_version('%s/__init__.py' % pkg_name, version, 
                                   '__version__')

    def _set_setup_version(self, version):
        self._info('Setting setup.py version to %s', version)
        self._set_filename_version('setup.py', version, '__version__')

    def _set_doc_version(self, version):
        self._info('Setting doc/conf.py version to %s', version)
        self._set_filename_version('doc/conf.py', version, 'release')

    def _build_and_upload(self):
        cmd = [sys.executable, 'setup.py', 'sdist', 'upload']
        stdout, stderr, retval = pyqi_system_call(cmd, shell=False,
                                                  dry_run=not self.RealRun)
        if retval is not 0:
            self._fail("build and upload failed,\nSTDOUT:\n%s\n\nSTDERR:\n%s", 
                       stdout, stderr)

    def _fail(self, message, *args):
        sys.stderr.write('Error: ') 
        sys.stderr.write(message % args)
        sys.stderr.write('\n')
        sys.exit(1)

    def _info(self, message, *args):
        sys.stderr.write(message % args)
        sys.stderr.write('\n')

    def _get_git_tags(self):
        cmd = ['git', 'tag']
        stdout, stderr, retval = pyqi_system_call(cmd, shell=False,
                                                  dry_run=not self.RealRun)
        if retval is not 0:
            self._fail("Could not git tag, \nSTDOUT:\n%s\n\nSTDERR:\n%s", 
                       stdout, stderr)

        return stdout.splitlines()

    def _git_is_clean(self):
        cmd = ['git','diff','--quiet']
        stdout, stderr, retval = pyqi_system_call(cmd, shell=False, 
                                                  dry_run=not self.RealRun)
        return retval == 0

    def _make_git_commit(self, message, *args):
        message = message % args
        cmd = ['git', 'commit', '-am', message]
        stdout, stderr, retval = pyqi_system_call(cmd, shell=False,
                                                  dry_run=not self.RealRun)
        if retval is not 0:
            self._fail("Could not git commit, \nSTDOUT:\n%s\n\nSTDERR:\n%s", 
                       stdout, stderr)

    def _make_git_tag(self, tag):
        self._info('Tagging "%s"', tag)
        cmd = ['git', 'tag', tag]
        stdout, stderr, retval = pyqi_system_call(cmd, shell=False,
                                                  dry_run=not self.RealRun)
        if retval is not 0:
            self._fail("Could not git tag, \nSTDOUT:\n%s\n\nSTDERR:\n%s", stdout,
                 stderr)

    def _get_git_branch(self):
        cmd = ['git','rev-parse','--abbrev-ref','HEAD']
        # ignoring self.RealRun, always execute
        stdout, stderr, retval = pyqi_system_call(cmd, shell=False)
        if retval is not 0:
            self._fail("Could not get git branch, \nSTDOUT:\n%s\n\nSTDERR:\n%s",
                       stdout, stderr)
        return stdout.strip()

    def _git_push_branch(self):
        branch = self._get_git_branch()
        self._info('Pushing branch %s to origin', branch)
        cmd = ['git','push','upstream', branch]
        stdout, stderr, retval = pyqi_system_call(cmd, shell=False,
                                                  dry_run=not self.RealRun)
        if retval is not 0:
            self._fail("Could not push branch %s, \nSTDOUT:\n%s\n\nSTDERR:\n%s",
                       stdout, stderr, branch)

    def _git_push_tag(self, tag):
        self._info('Pushing tag "%s"', tag)
        cmd = ['git','push','upstream',tag]
        stdout, stderr, retval = pyqi_system_call(cmd, shell=False,
                                                  dry_run=not self.RealRun)
        if retval is not 0:
            self._fail("Could not push tag %s, \nSTDOUT:\n%s\n\nSTDERR:\n%s",
                       stdout, stderr, tag)

    def run(self, **kwargs):
        pkg_name = kwargs['package_name']
        self.RealRun = kwargs['real_run']

        try:
            pkg_module = importlib.import_module(pkg_name)
        except ImportError:
            sys.stderr.write("Could not import %s!\n" % pkg_name)
            sys.exit(1)

        os.chdir(os.path.join(os.path.dirname(pkg_module.__file__), '..'))

        rv = self._parse_changelog()
        if rv is None:
            self._fail('Could not parse changelog')

        version, release_date = rv
        dev_version = version + '-dev'

        self._info('Releasing %s (release date %s)',
                   version, release_date.strftime('%m/%d/%Y'))
        tags = self._get_git_tags()

        if version in tags:
            self._fail('Version "%s" is already tagged', version)
        if release_date.date() != date.today():
            self._fail('Release date is not today (%s != %s)', 
                        release_date.strftime('%Y-%m-%d'),
                        date.today())

        if not self._git_is_clean():
            self._fail('You have uncommitted changes in git')

        self._set_init_version(pkg_name, version)
        self._set_setup_version(version)
        self._set_doc_version(version)
        self._make_git_commit('Bump version number to %s', version)
        self._make_git_tag(version)
        self._build_and_upload()
        self._set_init_version(pkg_name, dev_version)
        self._set_setup_version(dev_version)
        self._set_doc_version(dev_version)
        self._make_git_commit('Bump version number to %s', dev_version)
        self._git_push_branch()
        self._git_push_tag(version)

        return {}

CommandConstructor = MakeRelease
