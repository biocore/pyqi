#!/usr/bin/env python

#-----------------------------------------------------------------------------
# Copyright (c) 2013, The BiPy Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------

from __future__ import division
from unittest import TestCase, main
import pyqi
from pyqi.commands.make_bash_completion import (BashCompletion,
                                                _get_cfg_module, _load_cfg)
from pyqi.interfaces.optparse.config.make_bash_completion import (inputs,
                                                                  outputs)

__author__ = "Daniel McDonald"
__copyright__ = "Copyright 2013, The QCLI Project"
__credits__ = ["Daniel McDonald", "Jai Ram Rideout", "Doug Wendel", "Greg Caporaso"]
__license__ = "BSD"
__version__ = "0.1.0-dev"
__maintainer__ = "Daniel McDonald"
__email__ = "mcdonadt@colorado.edu"

class BashCompletionTests(TestCase):
    def test_get_cfg_module(self):
        self.assertEqual(_get_cfg_module('pyqi'), pyqi)

    def test_load_cfg(self):
        i, o = _load_cfg('pyqi.interfaces.optparse.config',
                         'make_bash_completion')
        self.assertEqual(i, inputs)
        self.assertEqual(o, outputs)
    
    def test_init(self):
        obj = BashCompletion()

    def test_run(self):
        params = {'command_config_module':'pyqi.interfaces.optparse.config',
                  'driver_name':'pyqi'}
        obs = BashCompletion().run(**params)
        self.assertEqual(obs, {'result':outputandstuff})    

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
    COMPREPLY=( $(compgen -W "make_bash_completion make_command make_optparse" -- $cur) )
  elif [ $COMP_CWORD -gt 1 ]; then
    case "$prev" in
             "make_bash_completion")
        COMPREPLY=( $(compgen -W "--command-config-module --driver-name --output-fp" -- $cur) )
        ;;
       "make_command")
        COMPREPLY=( $(compgen -W "--author --command-version --copyright --credits --email --license --name --output-fp" -- $cur) )
        ;;
       "make_optparse")
        COMPREPLY=( $(compgen -W "--command --command-module --output-fp" -- $cur) )
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
