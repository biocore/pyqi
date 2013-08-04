#!/usr/bin/env python

#-----------------------------------------------------------------------------
# Copyright (c) 2013, The BiPy Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------

from __future__ import division
from pyqi.pyqi_command.make_bash_completion import BashCompletion, \
        _get_cfg_module, _load_cfg
from unittest import TestCase, main
from pyqi.pyqi_command.cli.make_bash_completion import param_conversions, \
        additional_options
import pyqi

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
        pc, ao = _load_cfg('pyqi.pyqi_command.cli', 'make_bash_completion')
        self.assertEqual(pc, param_conversions)
        self.assertEqual(ao, additional_options)
    
    def test_init(self):
        obj = BashCompletion()

    def test_run(self):
        params = {'command_cfg_directory':'pyqi.pyqi_command.cli',
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
    COMPREPLY=( $(compgen -W "make_bash_completion make_cli make_command" -- $cur) )
  elif [ $COMP_CWORD -gt 1 ]; then
    case "$prev" in
             "make_bash_completion")
        COMPREPLY=( $(compgen -W "--driver_name --command_cfg_directory --output_fp" -- $cur) )
        ;;
       "make_cli")
        COMPREPLY=( $(compgen -W "--command --mod --output-fp" -- $cur) )
        ;;
       "make_command")
        COMPREPLY=( $(compgen -W "--license --name --copyright --author --func_version --credits --email --output-fp" -- $cur) )
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
