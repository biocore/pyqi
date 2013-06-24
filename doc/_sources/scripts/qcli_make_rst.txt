.. _qcli_make_rst:

.. index:: qcli_make_rst

*qcli_make_rst* -- Make Sphinx RST file for one or more qcli-based scripts
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Description:**

This script will take a qcli script and convert the usage strings and options to generate a documentation .rst file.


**Usage:** :file:`qcli_make_rst [options]`

**Input Arguments:**

.. note::

	
	**[REQUIRED]**
		
	-i, `-`-input_fps
		The input file(s) to generate rst files for
	-o, `-`-output_dir
		The directory where the resulting rst file(s) should be written


**Output:**

This script will output one or more Sphinx rst-formatted files.


**Create RST for many files:**

Create rst files for all files ending with .py in the scripts/ directory. Write the rst files to the rst directory. Note that if the value you pass for -i contains a wildcard character (e.g., "*"), the value must be wrapped in quotes.

::

	qcli_make_rst -i "scripts/*py" -o rst


