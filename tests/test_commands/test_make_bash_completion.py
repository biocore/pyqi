#!/usr/bin/env python
from __future__ import division

#-----------------------------------------------------------------------------
# Copyright (c) 2013, The BiPy Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------

import sys
from os import mkdir
from os.path import dirname, join
from shutil import copy, rmtree
from tempfile import mkdtemp
from unittest import TestCase, main
import pyqi
from pyqi.commands.make_bash_completion import BashCompletion, _get_cfg_module

__credits__ = ["Daniel McDonald", "Jai Ram Rideout", "Doug Wendel",
               "Greg Caporaso"]

class BashCompletionTests(TestCase):
    def setUp(self):
        """Set up data for unit tests."""
        self.cmd = BashCompletion()

        # Create a temporary directory that we can copy two config files into.
        # This module can then be passed to BashCompletion so that we don't
        # have to update the expected output each time we make an interface
        # change to pyqi. The temporary directory/module structure looks like
        # the following:
        #
        #     <temp dir>/
        #         pyqi_test/
        #             __init__.py
        #             make_bash_completion.py
        #             make_optparse.py
        #
        # Note that <temp dir> is added to sys.path in setUp and then removed
        # in tearDown. Imports can then function as normal, e.g.:
        #
        #     import pyqi_test.make_bash_completion
        #     ...
        #
        self.temp_module_dir = mkdtemp()
        self.temp_module_name = 'pyqi_test'
        self.temp_config_dir = join(self.temp_module_dir,
                                    self.temp_module_name)
        mkdir(self.temp_config_dir)

        module = _get_cfg_module('pyqi.interfaces.optparse.config')
        module_dir = dirname(module.__file__)

        make_bash_completion_fp = join(module_dir, 'make_bash_completion.py')
        copy(make_bash_completion_fp, self.temp_config_dir)

        make_optparse_fp = join(module_dir, 'make_optparse.py')
        copy(make_optparse_fp, self.temp_config_dir)

        with open(join(self.temp_config_dir, '__init__.py'), 'w') as f:
            f.write('')

        sys.path.append(self.temp_module_dir)

    def tearDown(self):
        sys.path.remove(self.temp_module_dir)
        rmtree(self.temp_module_dir)

    def test_get_cfg_module(self):
        self.assertEqual(_get_cfg_module('pyqi'), pyqi)

    def test_run(self):
        params = {'command_config_module':self.temp_module_name,
                  'driver_name':'pyqi'}
        obs = self.cmd(**params)
        self.assertEqual(list(obs.keys()), ['result'])
        self.assertEqual(obs['result'], outputandstuff)


outputandstuff = """_pyqi_complete()
{
  local cur prev

  COMPREPLY=()
  cur=${COMP_WORDS[COMP_CWORD]}
  prev=${COMP_WORDS[COMP_CWORD-1]}

  if [ $COMP_CWORD -gt 1 ]; then
    prev=${COMP_WORDS[1]}
  fi  

  if [ $COMP_CWORD -eq 1 ]; then
    COMPREPLY=( $(compgen -W "make-bash-completion make-optparse" -- $cur) )
  elif [ $COMP_CWORD -gt 1 ]; then
    case "$prev" in
             "make-bash-completion")
        COMPREPLY=( $(compgen -W "--command-config-module --driver-name --output-fp" -- $cur) )
        ;;
       "make-optparse")
        COMPREPLY=( $(compgen -W "--author --command --command-module --config-version --copyright --credits --email --license --output-fp" -- $cur) )
        ;;

      *)
        ;;
    esac
  fi

  return 0
} &&
complete -F _pyqi_complete -f pyqi
"""


if __name__ == '__main__':
    main()
