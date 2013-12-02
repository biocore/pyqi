#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    make-release
    ~~~~~~~~~~~~

    This code is adapted from the Flask project 
    (https://raw.github.com/mitsuhiko/flask/)
    
    :copyright: (c) 2011 by Armin Ronacher.
    :license: BSD, see Flask's LICENSE file for more details.

"""
import importlib
import sys
import os
import re
from datetime import datetime, date
from pyqi.util import pyqi_system_call

_date_clean_re = re.compile(r'(\d+)(st|nd|rd|th)')
DRY_RUN=True

def parse_changelog():
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
            return version, parse_date(datestr)

def bump_version(version):
    try:
        parts = map(int, version.split('.'))
    except ValueError:
        fail('Current version is not numeric')
    parts[-1] += 1
    return '.'.join(map(str, parts))

def parse_date(string):
    string = _date_clean_re.sub(r'\1', string)
    return datetime.strptime(string, '%B %d %Y')

def set_filename_version(filename, version_number, pattern):
    changed = []
    def inject_version(match):
        before, old, after = match.groups()
        changed.append(True)
        return before + version_number + after
    with open(filename) as f:
        contents = re.sub(r"^(\s*%s\s*=\s*')(.+?)(')(?sm)" % pattern,
                          inject_version, f.read())

    if not changed:
        fail('Could not find %s in %s', pattern, filename)
    
    if not DRY_RUN:
        with open(filename, 'w') as f:
            f.write(contents)

def set_init_version(pkg_name, version):
    info('Setting __init__.py version to %s', version)
    set_filename_version('%s/__init__.py' % pkg_name, version, '__version__')

def set_setup_version(version):
    info('Setting setup.py version to %s', version)
    set_filename_version('setup.py', version, '__version__')

def build_and_upload():
    cmd = [sys.executable, 'setup.py', 'sdist', 'upload']
    stdout, stderr, retval = pyqi_system_call(cmd, dry_run=DRY_RUN)
    if retval is not 0:
        fail("Could not build and upload, \nSTDOUT:\n%s\n\nSTDERR:\n%s", stdout, 
                stderr)

def fail(message, *args):
    print >> sys.stderr, 'Error:', message % args
    sys.exit(1)

def info(message, *args):
    print >> sys.stderr, message % args

def get_git_tags():
    cmd = ['git', 'tag']
    stdout, stderr, retval = pyqi_system_call(cmd, dry_run=DRY_RUN)
    if retval is not 0:
        fail("Could not git tag, \nSTDOUT:\n%s\n\nSTDERR:\n%s", stdout, stderr)

    return stdout.splitlines()

def git_is_clean():
    cmd = ['git','diff','--porcelain']
    stdout, stderr, retval = pyqi_system_call(cmd, dry_run=DRY_RUN)
    return retval == 0

def make_git_commit(message, *args):
    message = message % args
    cmd = ['git', 'commit', '-am', message]
    stdout, stderr, retval = pyqi_system_call(cmd, dry_run=DRY_RUN)
    if retval is not 0:
        fail("Could not git commit, \nSTDOUT:\n%s\n\nSTDERR:\n%s", stdout, 
                stderr)

def make_git_tag(tag):
    info('Tagging "%s"', tag)
    cmd = ['git', 'tag', tag]
    stdout, stderr, retval = pyqi_system_call(cmd, dry_run=DRY_RUN)
    if retval is not 0:
        fail("Could not git tag, \nSTDOUT:\n%s\n\nSTDERR:\n%s", stdout, 
                stderr)

def usage():
    script_name = os.path.basename(sys.argv[0])
    print >> sys.stderr, "Usage: %s pkg_name [real-run]" % script_name
    sys.exit(1)

def main():
    if len(sys.argv) < 2:
        usage()

    if len(sys.argv) == 3:
        if sys.argv[2] != 'real-run':
            usage()
        global DRY_RUN
        DRY_RUN = True

    pkg_name = sys.argv[1]

    try:
        pkg_module = importlib.import_module(pkg_name)
    except ImportError:
        print >> sys.stderr, "Could not import %s!" % pkg_name
        sys.exit(1)

    os.chdir(os.path.join(os.path.dirname(pkg_module.__file__), '..'))
    
    rv = parse_changelog()
    if rv is None:
        fail('Could not parse changelog')

    version, release_date = rv
    dev_version = bump_version(version) + '-dev'

    info('Releasing %s (release date %s)',
         version, release_date.strftime('%m/%d/%Y'))
    tags = get_git_tags()

    if version in tags:
        fail('Version "%s" is already tagged', version)
    if release_date.date() != date.today():
        fail('Release date is not today (%s != %s)')

    if not git_is_clean():
        fail('You have uncommitted changes in git')

    set_init_version(pkg_name, version)
    set_setup_version(version)
    make_git_commit('Bump version number to %s', version)
    make_git_tag(version)
    build_and_upload()
    set_init_version(pkg_name, dev_version)
    set_setup_version(dev_version)

if __name__ == '__main__':
    main()
