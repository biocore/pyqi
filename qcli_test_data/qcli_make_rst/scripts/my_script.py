#!/usr/bin/env python
# File created on 12 Jun 2013
from __future__ import division

__author__ = "Greg Caporaso"
__copyright__ = "Copyright 2013, The BiPy project"
__credits__ = ["Greg Caporaso"]
__license__ = "GPL"
__version__ = "0.0.0"
__maintainer__ = "Greg Caporaso"
__email__ = "gregcaporaso@gmail.com"
__status__ = "Development"


from qcli import (parse_command_line_parameters, 
                  make_option)

script_info = {}
script_info['brief_description'] = "An example script."
script_info['script_description'] = "This script is just an example, nothing exciting here."
script_info['script_usage'] = []
script_info['script_usage'].append(("Example usage","Run the script in help mode","%prog -h"))
script_info['output_description']= "No output is created... it's just an example."
script_info['required_options'] = [
 make_option('-i','--input_fp',type="existing_filepath",help='the input filepath'),
]
script_info['optional_options'] = [
 make_option('-o','--output_dir',type="new_dirpath",help='the output directory [default: %default]'),
]
script_info['version'] = __version__

def main():
    option_parser, opts, args =\
       parse_command_line_parameters(**script_info)


if __name__ == "__main__":
    main()