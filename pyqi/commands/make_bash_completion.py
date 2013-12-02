#!/usr/bin/env python

#-----------------------------------------------------------------------------
# Copyright (c) 2013, The BiPy Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------

from __future__ import division

__credits__ = ["Daniel McDonald", "Jai Ram Rideout", "Doug Wendel",
    "Greg Caporaso"]

import importlib
from pyqi.core.command import (Command, CommandIn, CommandOut, 
    ParameterCollection)
from pyqi.core.interface import get_command_names, get_command_config

def _get_cfg_module(desc):
    """Load a module"""
    mod = importlib.import_module(desc)
    return mod

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
    
    CommandIns = ParameterCollection([
        CommandIn(Name='command_config_module', DataType=str,
                  Description="CLI command configuration module",
                  Required=True),
        CommandIn(Name='driver_name', DataType=str,
                  Description="name of the driver script", Required=True)
    ])

    CommandOuts = ParameterCollection([
        CommandOut(Name='result', DataType=str,
                   Description="result bash completion script")
    ])

    def run(self, **kwargs):
        driver = kwargs['driver_name']
        cfg_mod_path = kwargs['command_config_module']
        cfg_mod = _get_cfg_module(cfg_mod_path)
        command_names = get_command_names(cfg_mod_path)
        command_list = ' '.join(command_names)

        commands = []
        for cmd in command_names:
            cmd_cfg, _ = get_command_config(cfg_mod_path, cmd,
                                            exit_on_failure=False)

            if cmd_cfg is not None:
                command_options = []
                command_options.extend(
                        sorted(['--%s' % p.Name for p in cmd_cfg.inputs]))
                opts = ' '.join(command_options)

                commands.append(command_fmt % {'command':cmd, 'options':opts})

        all_commands = ''.join(commands)
        return {'result':script_fmt % {'driver':driver,
                                       'commands':all_commands,
                                       'command_list':command_list}}

CommandConstructor = BashCompletion
