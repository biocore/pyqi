#!/usr/bin/env python

#-----------------------------------------------------------------------------
# Copyright (c) 2013, The BiPy Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------

from __future__ import division
from pyqi.core.command import Command, Parameter

__author__ = "Daniel McDonald"
__copyright__ = "Copyright 2013, The QCLI Project"
__credits__ = ["Daniel McDonald", "Jai Ram Rideout", "Doug Wendel", "Greg Caporaso"]
__license__ = "BSD"
__version__ = "0.1.0-dev"
__maintainer__ = "Daniel McDonald"
__email__ = "mcdonadt@colorado.edu"

import importlib
def _get_cfg_module(desc):
    mod = importlib.import_module(desc)
    return mod

def _load_cfg(mod, cmd):
    foo = __import__(mod, fromlist=[cmd])
    actual_cmd_mod = getattr(foo, cmd)
    return (getattr(actual_cmd_mod, 'param_conversions'), 
            getattr(actual_cmd_mod, 'additional_options'))

# Based on http://stackoverflow.com/questions/5302650/multi-level-bash-completion
script_fmt = """_%(driver)s_complete()
{
  local cur prev

  COMPREPLY=()
  cur=${COMP_WORDS[COMP_CWORD]}
  prev=${COMP_WORDS[COMP_CWORD-1]}

  if [ $COMP_CWORD -gt 1 ]; then
    prev=${COMP_WORDS[1]}
  fi  

  if [ $COMP_CWORD -eq 1 ]; then
    COMPREPLY=( $(compgen -W "%(command_list)s" -- $cur) )
  elif [ $COMP_CWORD -gt 1 ]; then
    case "$prev" in
      %(commands)s
      *)
        ;;
    esac
  fi

  return 0
} &&
complete -F _%(driver)s_complete -f %(driver)s
"""

command_fmt = """       "%(command)s")
        COMPREPLY=( $(compgen -W "%(options)s" -- $cur) )
        ;;
"""

class BashCompletion(Command):
    BriefDescription = "Construct a bash completion script"
    LongDescription = """Construct a bash tab completion script that will search through available commands and options"""

    def run(self, **kwargs):
        driver = kwargs['driver_name']
        cfg_dir = kwargs['command_cfg_directory']
        cfg_mod = _get_cfg_module(cfg_dir)
        command_list = ' '.join(cfg_mod.__all__[:])

        commands = []
        for cmd in cfg_mod.__all__:
            param_convs, added_opts = _load_cfg(cfg_dir, cmd)
            
            command_options = []
            command_options.extend(['--%s' % n for n in param_convs.keys()])
            command_options.extend(['--%s' % o.LongName for o in added_opts])
            opts = ' '.join(command_options)

            commands.append(command_fmt % {'command':cmd, 'options':opts})

        all_commands = ''.join(commands)
        return {'result':script_fmt % {'driver':driver, 
                                       'commands':all_commands,
                                       'command_list':command_list}}

    def _get_parameters(self):
        return [Parameter(Name='command_cfg_directory',Required=True,Type=str,
                          Help='The CLI command configuration directory'),
                 Parameter(Name='driver_name',Required=True,Type=str,
                           Help='Name of the driver script')]

CommandConstructor = BashCompletion
