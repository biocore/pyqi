.. _creating:

============================
Creating a qcli-based script
============================

This document covers how to create a new qcli script, and all of the options that you have for customizing how your qcli script works.

The primary object that defines a qcli script is the ``script_info`` dictionary. This is where all of the parameters and help text are defined, as well as various options you have for configuring how the script works. The easiest way to start a new qcli script is using the ``qcli_make_script`` script that is included with qcli. This document will start there, and then provide details on how to customize your script.

This page will help you develop your command line interfaces, but you should still familiarize yourself with Python's ``optparse`` module. qcli provides some convenient wrappers for ``optparse``, but will not be a replacement to a general understanding of how to interact with ``optparse`` (see the `optparse documentation <http://docs.python.org/library/optparse.html>`_). 

.. note:: As support for ``optparse`` will not continue into Python 3.0, we will transition to using ``argparse`` behind the scenes in the very near future. Our goal is to make these changes fully backward compatible so qcli users won't need to change anything or do anything differently following the transition.

Creating script templates
=========================
qcli provides a script, ``make_qcli_script`` for creating template qcli-based scripts. The output of ``make_qcli_script`` is a fully functional qcli script (though it doesn't do very much). To create a qcli script, you can do the following::
	
	qcli_make_script -o my_script.py

This will create a new qcli-based script called ``my_script.py``, and give it execute permission. To run this script in help mode from the directory where it was created, you could then call::
	
	./my_script.py -h

You should see help text printed to the terminal.

`See here for an example <https://github.com/bipy/qcli/blob/master/qcli_test_data/qcli_make_script/my_script.py>`_ of a script created with ``qcli_make_script``. 

Your next steps are to customize your template script to do what you want your script to do.

Customizing your script with script_info
========================================

To customize your script, you'll edit the values for entries in the ``script_info`` dictionary to define the options, help text, and behavior of your script. These are the core values defined in the ``script_info`` dictionary and used by qcli. You must provide values for those tagged as ``REQUIRED``, and can optionally provide values for all of the others.

+-------------------------------+-------------------------------------------------------------------------------------------------------+--------------+
|        key                    |  Description                                                                                          |    Default   |
+===============================+=======================================================================================================+==============+
| script_description            | a paragraph description of the script's functionality                                                 |    REQUIRED  |
+-------------------------------+-------------------------------------------------------------------------------------------------------+--------------+
| version                       | a version number for the script                                                                       |   REQUIRED   |
+-------------------------------+-------------------------------------------------------------------------------------------------------+--------------+
| script_usage                  | a list of tuples illustrating example usages of the script                                            |       []     |
+-------------------------------+-------------------------------------------------------------------------------------------------------+--------------+
| output_description            | a paragraph description of the script's output                                                        |       ""     |
+-------------------------------+-------------------------------------------------------------------------------------------------------+--------------+
| required_options              | a list of optparse Option objects that are required for the script to run                             |        []    |
+-------------------------------+-------------------------------------------------------------------------------------------------------+--------------+
| optional_options              | a list of optparse Option objects that are optional for the script to run                             |        []    |
+-------------------------------+-------------------------------------------------------------------------------------------------------+--------------+
| disallow_positional_arguments | do not allow positional arguments to be passed to the script                                          |  True        |
+-------------------------------+-------------------------------------------------------------------------------------------------------+--------------+
| help_on_no_arguments          | print help text if the script is called with no options or arguments                                  |   True       |
+-------------------------------+-------------------------------------------------------------------------------------------------------+--------------+
| suppress_verbose              | do not include a verbose option for the script                                                        |    False     |  
+-------------------------------+-------------------------------------------------------------------------------------------------------+--------------+
| script_usage_output_to_remove | a list of output dirs/files that must be cleaned up if running script_usage examples multiple times   |   []         |
+-------------------------------+-------------------------------------------------------------------------------------------------------+--------------+

It's also possible to add your own values to the ``script_info`` dictionary, if you'd like to use others in your code base. These following values are known to be used by tools outside of the qcli code base in ``script_info`` objects. It's best to not name new values with these names to avoid conflicts. 

+-------------------------------+-------------------------------------------------------------------------------------------------------+--------------+
|        key                    |  Description                                                                                          |    Used by   |
+===============================+=======================================================================================================+==============+
| brief_description             | a one-sentence description of the script, used by some document generators                            |    Q,T       |
+-------------------------------+-------------------------------------------------------------------------------------------------------+--------------+
| script_type                   | a definition of the type of script, used by some graphical interfaces                                 |      Q,PG    |
+-------------------------------+-------------------------------------------------------------------------------------------------------+--------------+
| optional_options_groups       | a list grouping related options under a heading [['section heading string', section_option_list], ...]|      PG      |
+-------------------------------+-------------------------------------------------------------------------------------------------------+--------------+
| authors                       | string of author names                                                                                |      PG      |
+-------------------------------+-------------------------------------------------------------------------------------------------------+--------------+
| script_name                   | a brief "human readable" name for the script, used in some graphical interfaces                       |       Q,PG   |
+-------------------------------+-------------------------------------------------------------------------------------------------------+--------------+
| output_type                   | a list of tuples noting the type (in a controlled vocabulary) of each possible output                 |       Q      |
+-------------------------------+-------------------------------------------------------------------------------------------------------+--------------+
| option_label                  | a dictionary matching option names to "human readable" names, used in some graphical interfaces       |   Q          |
+-------------------------------+-------------------------------------------------------------------------------------------------------+--------------+

"Used by" key : Q: `QIIME <http://www.qiime.org>`_; PG: PyCogent beta GUI; T: tax2tree.

Setting values in script_info
-----------------------------

The ``script_info`` object is simply a python dictionary, so the standard method for setting and working with dict entries applies. Some examples are::

	script_info['brief_description'] = "Count sequences in one or more fasta files."
	script_info['required_options'] = [
	 make_option('-i','--input_fps',
	        help='the input filepaths (comma-separated)'),
	]

Creating options
================

Typically the first thing you'll want to do is define the options that your script will take. The following covers how to create your own options, which you would include in the ``script_info['required_options']`` or ``script_info['optional_options']`` lists. Some of this is general to ``optparse`` and some is specific to qcli.

Options to your script are created with ``qcli.option_parsing.make_option``, which is a wrapper for ``optparse.make_option`` that includes support for additional option types. See the `optparse make_option documentation <http://docs.python.org/library/optparse.html#populating-the-parser>`_) for detailed information on how to create options. In your qcli-based script you can create either required options, which must be passed every time your script is called, or optional options, which do not need to be passed every time the script is called (e.g., because there is a default value in place, or they are only applicable under certain circumstances). You'll define your options by assigning lists of calls to ``make_option`` to ``script_info['required_options']`` and ``script_info['optional_options']``, respectively.

Defining one required option and one optional option might look like the following::

	script_info['required_options'] = [
	 make_option('-n','--start_integer',type='int',
	        help='the position to start counting at'),
	]
	script_info['optional_options'] = [
	 make_option('--suppress_errors',action='store_true',\
	        help='Suppress warnings about missing files [default: %default]',
	        default=False)
	]

Custom option types for files and directories
---------------------------------------------
When defining options for input or output files or directories, you should use the qcli custom option types. These standardize error handling in the case of input files which don't exist or aren't readable, or output files are passed which already exist. These custom option types are:

* ``existing_path`` : Specify a path to a directory or file. Path must exist or an error is raised.

* ``new_path`` : Specify a path to a directory or file. Path must not exist or an error is raised.

* ``existing_filepath`` : Specify a path to a file.  Path must exist or an error is raised.

* ``existing_filepaths`` : Specify a comma-separated list of file paths. All paths must exist or an error is raised. These are returned as a list split on commas.

* ``new_filepath`` :  Specify a path to a file.  Path must not exist or an error is raised.

* ``existing_dirpath`` :  Specify a path to a directory.  Path must exist or an error is raised.

* ``new_dirpath`` :  Specify a path to a directory.  Path must not exist or an error is raised.

Guidelines on values that should and should not be set when defining an option
------------------------------------------------------------------------------

* Don't define ``dest=``. By default this gets set to the long-form parameter option (e.g. ``dest='input_fp'`` is implied if your option is ``--input_fp``). Defining this as something else will confuse other people who may end up doing maintenance work on your scripts in the future.

* Always define ``default=`` for optional options, and never define ``default=`` for required options. The default value for all options is ``None``, but it's convenient to explicitly define a default for readability.

* Always define ``help=``, and provide useful information in this string. Include ``[default: %default]`` for optional options, but not for required options (as there can be no default for a required option, or it'd be optional). The ``%default`` gets replaced with the value provided for ``default=`` in the help text. It sometimes makes sense to include additional information in the ``[default:%default]`` text if the option on it's own is not informative. For example::

	make_option("--output_fp", default=None, help="output filepath [default:%default; print to stdout]")

* ``action=store`` and ``type=string`` are defaults, and therefore do not need to be included. Leave these values out to keep your code cleaner.

* If you need to pass multiple paths or strings to a single option, do this by passing a comma-separated string. The ``existing_filepaths`` option type expects strings in this format and takes care of splitting them on commas and returning a list, so if you're passing multiple input filepaths use ``type='existing_filepaths'``.

Additional useful option types
------------------------------

Flag options
^^^^^^^^^^^^

Flags are boolean options to your script. qcli supports these directly, so you should never have to define an option that explicitly takes ``True`` or ``False`` as a value on the command line.

Flags to your script should always be either ``action='store_true'`` or ``action='store_false'``, and do not need to define a type. The names of these options should suggest whether the option enables something (e.g., ``--print_to_stdout``) which would be defined with ``action='store_true'`` (i.e., default is ``False``), or whether the option disables something (e.g., ``--suppress_stdout``) which would be defined with ``action='store_false'`` (i.e., the default is ``True``). A bad name for a flag is ``--stdout`` as it's not clear what this option does.

Always define ``default`` for boolean options to set the default option for your script. If ``action='store_true'`` you should *always* pass ``default=False``. If ``action='store_false'`` you should *always* pass ``default=True``.

Choice options
^^^^^^^^^^^^^^
Use ``type=choice`` when an option is passed as a string and can be one of several acceptable values. This saves you from having to check that the user passed an acceptable value. This is done by ``optparse``, so saves you lines of code that you'd need to test, and standardizes how errors are handled. The acceptable choices are defined with ``choices=``. An example choice option definition is::

	alignment_method_choices = ['pynast','mafft','muscle']
	o = make_option('-m','--alignment_method',type='choice',
	                help='Method for aligning sequences. Valid choices are: '+\
	                ', '.join(alignment_method_choices) + ' [default: %default]',
	                choices=alignment_method_choices, default='pynast')

Note that the help text here includes the list of acceptable options. This is generally a good idea as it's convenient for the user. It's not a good idea however if this is a big list (say, more than 5 or so options). If the user passes something invalid (such as ``raxml`` in this example) the list of acceptable options will be included in the error text.



Guidelines on naming options
----------------------------

``optparse`` allows for users to define short-form (e.g., ``-i``) and long-form (``--input_fp``) option names. For options that are commonly used, define both a long-form and a short-form parameter name::

	make_option('-i','--input_dir',type="existing_filepath",help='the input directory')

For options that are infrequently used define only a long-form parameter name::

	make_option('--output_file_type',help='the file type for graphical output',default='pdf')

This helps with reducing clutter and saving convenient short-form parameter names for future options that may be added.

Make paths to files end with ``_fp`` (for *filepath*) and paths to directories end with ``_dir``. This helps users understand exactly what must be passed to a script.

Some good names for common options are listed below. You should use these whenever possible.

+-------------------------------+----------------------------------------------------------------------------------------------------+
|        Description            | Option name                                                                                        |
+===============================+====================================================================================================+
|  path to an input file        | ``-i``, ``--input_fp``                                                                             |
+-------------------------------+----------------------------------------------------------------------------------------------------+
|  path to an output file       | ``-o``, ``--output_fp``                                                                            |
+-------------------------------+----------------------------------------------------------------------------------------------------+
|  path to an input directory   | ``-i``, ``--input_dir``                                                                            |
+-------------------------------+----------------------------------------------------------------------------------------------------+
|  path to an output dir        | ``-o``, ``--output_dir``                                                                           |
+-------------------------------+----------------------------------------------------------------------------------------------------+
|  path to a log file           | ``-l``, ``--log_fp``                                                                               |
+-------------------------------+----------------------------------------------------------------------------------------------------+

Documenting your script
=======================

Script documentation
--------------------
The ``script_documentation`` entry in ``script_info`` should describe the basic functionality of your script. This entry is typically between one and four sentences in length. Don't add line breaks yourself - qcli will take care of this for you, and the formatting will look better than if you try to do it yourself as it will adjust to the size of the user's terminal.

Usage examples
--------------
The ``usage_examples`` entry in ``script_info`` should list one or more examples of commands that need to be run to execute your script. These should be actual calls to commands. A user should be able to copy this and paste it on the command line and have the script run (provided they put the right input files in place). ``script_info['usage_examples']`` must be a list of tuples with three string entries each where the first entry is a concise title for the example, the second entry is a description of the example and why certain parameter settings are being made, and the third entry should be the exact command that needs to be run. Start these examples with ``%prog`` - this gets replaced with the name of your script and is convenient so you don't have to remember to update the usage examples if the name of your script changes. Good usage examples might look like the following::

	script_info['script_usage'] = [\
	 ("Count sequences in one file",
	  "Count the sequences in a fasta file and write results to stdout.",
	  "%prog -i in.fasta"),
	 ("Count sequences in two file",
	  "Count the sequences in two fasta files and write results to stdout.",
	  "%prog -i in1.fasta,in2.fasta"),
	  ("Count the sequences in many fasta files",
	   "Count the sequences all .fasta files in current directory and write results to stdout. Note that -i option must be quoted.",
	   "%prog -i \"*.fasta\"")]

In addition to being extremely helpful for users of your code, these examples are what is tested by the `script interface testing framework <./script_interface_testing.html>`_, so there are many benefits to defining a lot of good usage examples.

Output description
------------------
The ``output_description`` entry in ``script_info`` should describe the output generated by the script. This entry is typically one to several sentences. Again, don't add line breaks yourself.

Example of a simple qcli script
===============================

The following is a complete example of a script for counting the number of nucleotide or protein sequences in a fasta file. 

::
	
	#!/usr/bin/env python
	from __future__ import division

	__author__ = "Greg Caporaso"
	__copyright__ = "Copyright 2013, The qcli project"
	__credits__ = ["Greg Caporaso"]
	__license__ = "GPL"
	__version__ = "0.0.0-dev"
	__maintainer__ = "Greg Caporaso"
	__email__ = "gregcaporaso@gmail.com"
	__status__ = "Development"
	
	from glob import glob
	from qcli.option_parsing import (
	 parse_command_line_parameters, 
	 make_option)
	
	script_info = {}
	script_info['brief_description'] = "Count sequences in one or more fasta files."
	script_info['script_description'] = "This script counts the number of sequences in one or more fasta files and prints the results to stdout."
	script_info['script_usage'] = [\
	 ("Count sequences in one file",
	  "Count the sequences in a fasta file and write results to stdout.",
	  "%prog -i in.fasta"),
	 ("Count sequences in two file",
	  "Count the sequences in two fasta files and write results to stdout.",
	  "%prog -i in1.fasta,in2.fasta"),
	  ("Count the sequences in many fasta files",
	   "Count the sequences all .fasta files in current directory and write results to stdout. Note that -i option must be quoted.",
	   "%prog -i \"*.fasta\"")]
	script_info['output_description']= "Tabular data is written to stdout."
	script_info['required_options'] = [
	 make_option('-i','--input_fps',type='existing_filepaths',
	        help='the input filepath(s) (comma-separated if more than one)'),
	]
	script_info['optional_options'] = [
	 make_option('--suppress_errors',action='store_true',\
	        help='Suppress warnings about missing files [default: %default]',
	        default=False)
	]
	script_info['version'] = __version__
	
	def main():
	    option_parser, opts, args =\
	       parse_command_line_parameters(**script_info)
	    suppress_errors = opts.suppress_errors
    
	    input_fps = []
	    for input_fp in opts.input_fps:
	        input_fps.extend(glob(input_fp))
    
	    for input_fp in input_fps:
	        i = 0
	        try:
	            input_f = open(input_fp,'U')
	        except IOError,e:
	            if suppress_errors:
	                continue
	            else:
	                print input_fp, e
	        for s in input_f:
	            if s.startswith('>'):
	                i += 1
	            else:
	                pass
	        print input_fp, i

	if __name__ == "__main__":
	    main()
	
