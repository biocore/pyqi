.. _qcli_make_script:

.. index:: qcli_make_script

*qcli_make_script* -- Create a template qcli script.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Description:**

This script will create a template qcli script and make it executable.


**Usage:** :file:`qcli_make_script [options]`

**Input Arguments:**

.. note::

	
	**[REQUIRED]**
		
	-o, `-`-output_fp
		The output filepath.
	
	**[OPTIONAL]**
		
	-a, `-`-author_name
		The script author's (probably you) name to be included in the header variables. This will typically need to be enclosed  in quotes to handle spaces. [default:AUTHOR_NAME]
	-e, `-`-author_email
		The script author's (probably you) e-mail address to be included in the header variables. [default:AUTHOR_EMAIL]
	-c, `-`-copyright
		The copyright information to be included in the header variables. [default:Copyright 2013, The BiPy project]


**Output:**

The result of this script is a qcli template script.


**Example usage:**

Create a new script

::

	qcli_make_script -a "Greg Caporaso" -e gregcaporaso@gmail.com -o my_script.py


