#!/usr/bin/env python
# File created on 12 Jun 2013
from __future__ import division

__author__ = "Greg Caporaso"
__copyright__ = "Copyright 2013, The BiPy project"
__credits__ = ["Greg Caporaso"]
__license__ = "GPL"
__version__ = "0.1.0-dev"
__maintainer__ = "Greg Caporaso"
__email__ = "gregcaporaso@gmail.com"


from qcli import (parse_command_line_parameters, 
                  make_option)

script_info = {}
script_info['brief_description'] = ""
script_info['script_description'] = ""
script_info['script_usage'] = []
script_info['script_usage'].append(("","",""))
script_info['output_description']= ""
script_info['required_options'] = [
 # Example required option
 #make_option('-i','--input_fp',type="existing_filepath",help='the input filepath'),
]
script_info['optional_options'] = [
 # Example optional option
 #make_option('-o','--output_dir',type="new_dirpath",help='the output directory [default: %default]'),
]
script_info['version'] = __version__



def main():
    option_parser, opts, args =\
       parse_command_line_parameters(**script_info)


if __name__ == "__main__":
    main()