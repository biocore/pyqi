.. _testing:

Script interface testing
========================

It is often difficult to test script interfaces, which are often the primary point of interaction with users. So, for example, if python script contains code that looks like this:: 

	from qiime.filter import filter_samples_from_otu_table
	from qiime.filter import filter_otus_from_otu_table
	
	...
	
	if run_mode == 'filter_samples':
		filter_samples_from_otu_table(...)
	elif run_mode == 'filter_otus':
		filter_otus_from_otu_table(...)
	else:
		raise ValueError, "Unknown run_mode."

and a developer accidentally removes the ``from qiime.filter import filter_otus_from_otu_table`` line but manually only tests with ``run_mode == 'filter_samples'``, they likely would not catch the error before release of the software. These types of errors generally result in cryptic error messages, which frustrates users and increases technical support loads. As powerful as the underlying code may be, this simple, common mistake makes it useless to the end user.

To detect these types of errors, qcli implements a script interface testing framework that makes use of the ``usage_examples`` in the ``script_info`` object that is implemented by all scripts. This framework relies on a set of example files that can be used as additional documentation of qcli-based scripts, as well as a function for running the script usage tests which, for example, can be called from within your continuous integration testing framework.

The following sections first illustrate how to apply this testing framework locally, and then how to develop qcli scripts so they can be used with this framework.

Running script usage tests
===========================

After obtaining the ``qcli`` repository, you can ``cd`` to ``qcli/tests`` directory. You'll see a script called ``all_tests.py``. You can run this from the ``tests`` directory by calling::

	./all_tests.py --suppress_unit_tests

This will run all of the script usage tests which are currently defined in verbose mode. You can run specific tests by passing the names of those tests via the ``--script_tests`` parameter. For example, to run only the tests for ``qcli_make_script`` and ``qcli_make_rst`` you can run the following::

	./all_tests.py --suppress_unit_tests --script_tests add_qiime_labels,make_otu_table

These tests will print output to the screen.

The recommended way of testing qcli is to run qcli's unit tests and script usage tests. You can do this simply by running::

	./all_tests.py

How the script usage tests work
===============================
You'll see many sub-directories in ``qcli_test_data`` with names corresponding to the names of qcli scripts. Each of these directories contains example input and output for the corresponding qcli script. For example, the ``qcli_make_rst`` directory contains the following test data for the ``qcli_make_rst`` script::

	ls -R qcli_test_data/qcli_make_rst
	rst	scripts

	qcli_test_data/qcli_make_rst/rst:
	my_script.rst

	qcli_test_data/qcli_make_rst/scripts:
	my_script.py

If you call ``qcli_make_rst.py -h``, you'll see the following usage examples::

	Example usage:
	Print help message and exit
	 qcli_make_rst -h

	Example: Create an example script
	 qcli_make_rst -i scripts -o rst

What you'll notice is that the usage example input and output files correspond to the files in ``qcli/qcli_test_data/qcli_make_rst``. The script interface testing works by copying all of the files in ``qcli_make_rst`` to a temporary directory, changing into that directory, running each of the usage examples, and confirming that the script exited successfully (i.e., with an exit status of ``0``).

 .. warning:: Currently the script usage tests only test whether a script exits successfully: they do not check whether the results correspond to the example output. The reasoning is that that would duplicate the functionality of the unit tests (which isn't a bad thing, except that implementing this would be a lot of work). These are tests that the interfaces themselves are working.

If you don't see a directory corresponding to a script name in the ``qcli_test_data`` directory, that means that a script interface test has not been defined for that script.

Adding script interface testing for new scripts
===============================================

Adding new script interface tests is easy. All you do is create a new test directory under your repository's ``test_data`` directory (by convention this would be named ``<repo>_test_data``, where ``<repo>`` would be replaced with the name of your repository), where the name of the directory corresponds to the script's name. For example, if you're adding tests for ``my_script.py`` or ``my_script`` (i.e., with or without the ``.py`` extension), you'd add a directory called ``my_script``. In that directory you would create example input and output files for all of the script usage examples that are defined in your script. Make several usage examples that make use of different paths through your script. 

Full paths
----------
If you recommend that your users specify full paths (which is often safer for jobs that run in parallel on clusters), in your usage example, replace the full path with $PWD. For example (from QIIME's ``pick_de_novo_otus.py``)::

	Simple example: The following command will start an analysis on seqs.fna (-i), which is a
	post-split_libraries fasta file. The sequence identifiers in this file should be of the form
	<sample_id>_<unique_seq_id>. The following steps, corresponding to the preliminary data 
	preparation, are applied: Pick de novo OTUs at 97%; pick a representative sequence for each 
	OTU (the OTU centroid sequence); align the representative set with PyNAST; assign taxonomy 
	with RDP classifier; filter the alignment prior to tree building - remove positions which 
	are all gaps, and specified as 0 in the lanemask; build a phylogenetic tree with FastTree; 
	build an OTU table. All output files will be written to the directory specified by -o, and 
	subdirectories as appropriate. ALWAYS SPECIFY ABSOLUTE FILE PATHS (absolute path represented 
	here as $PWD, but will generally look something like /home/ubuntu/my_analysis/).
	 pick_de_novo_otus.py -i $PWD/seqs.fna -o $PWD/otus/

Cleaning up output files
------------------------
If your scripts require that the user-specified output directory does not exist when the script runs, but you provide example output in the test directory, you can tell the testing framework to clean up any existing output directories before running. To automatically remove output directories prior to running the tests, add the ``script_usage_output_to_remove`` entry to your script info. For example, from QIIME's ``pick_de_novo_otus.py``::

	script_info['script_usage_output_to_remove'] = ['$PWD/otus/']





