.. _defining-new-interfaces:

Defining new interfaces
=======================

After defining a new ``Command`` and its API, as covered in :ref:`defining-new-commands`, you're ready to create a first user interface for that command. In this tutorial we'll define a command line interface for the ``SequenceCollectionSummarizer`` command. 

The main differences that need to be handled when defining a command line interface are that we'll want the user to provide their sequence collection on the command line, and we'll want to write the output to a filepath that the user specifies on the command line. This is different than what happens in ``SequenceCollectionSummarizer``, where the input and output are python objects. This is a very important distinction - since our derived ``Commands`` are meant to be interface-independent, they should not do things like require files as input. In some rare circumstances, it may be required for a ``Command`` to write files as its output (for example, if storing the output in memory is intractable).

pyqi currently provides support for building command line interfaces based on python's `optparse <http://docs.python.org/2/library/optparse.html>`_ module. Your interface will ultimately be an instance of ``pyqi.interfaces.optparse.OptparseInterface``, but the interface class itself is generated dynamically. As a developer, you only define the configuration for the interface via an *interface configuration file* (which is a valid python file) - you won't actually define the interface class itself. If this sounds confusing, just get started - it's easier than it sounds.

Stubbing a new command line interface
-------------------------------------

pyqi provides a command, ``make-optparse``, that allows developers to easily stub (i.e., create templates for) their optparse interface configuration files. After installing pyqi, you can get usage information by calling::

	pyqi make-optparse -h

To create your interface, you'll need to pass the ``Command`` as a fully specified python module name, the name of the module where that ``Command`` is defined, ownership information (e.g., author name, copyright, license, etc.) and the path where the new configuration file should be written. For example, to create a stub for an ``OptparseInterface`` for our ``SequenceCollectionSummarizer`` command, you could run the following::

	pyqi make-optparse -c sequence_collection_summarizer.SequenceCollectionSummarizer -m sequence_collection_summarizer -a "Greg Caporaso" --copyright "Copyright 2013, Greg Caporaso" -e "gregcaporaso@gmail.com" -l BSD --config-version 0.0.1 -o summarize_sequence_collection.py

.. warning:: For the above command to work, the directory containing ``sequence_collection_summarizer.py`` will need to be in your ``$PYTHONPATH``. 

The resulting file will look something like this::

	#!/usr/bin/env python
	from __future__ import division

	__author__ = "Greg Caporaso"
	__copyright__ = "Copyright 2013, Greg Caporaso"
	__credits__ = ["Greg Caporaso"]
	__license__ = "BSD"
	__version__ = "0.0.1"
	__maintainer__ = "Greg Caporaso"
	__email__ = "gregcaporaso@gmail.com"

	from pyqi.core.interfaces.optparse import (OptparseUsageExample,
	                                           OptparseOption, OptparseResult)
	from pyqi.core.command import make_parameter_collection_lookup_f
	from sequence_collection_summarizer import CommandConstructor

	# If you need access to input or output handlers provided by pyqi, consider
	# importing from the following modules:
	# pyqi.core.interfaces.optparse.input_handler
	# pyqi.core.interfaces.optparse.output_handler
	# pyqi.interfaces.optparse.input_handler
	# pyqi.interfaces.optparse.output_handler

	# Convenience function for looking up parameters by name.
	param_lookup = make_parameter_collection_lookup_f(CommandConstructor)

	# Examples of how the command can be used from the command line using an
	# optparse interface.
	usage_examples = [
	    OptparseUsageExample(ShortDesc="A short single sentence description of the example",
	                         LongDesc="A longer, more detailed description",
	                         Ex="%prog --foo --bar some_file")
	]

	# inputs map command line arguments and values onto Parameters. It is possible
	# to define options here that do not exist as parameters, e.g., an output file.
	inputs = [
	    # An example option that has a direct relationship with a Parameter.
	    # OptparseOption(Parameter=param_lookup('name_of_a_parameter'),
	    #                InputType='existing_filepath', # the optparse type of input
	    #                InputAction='store', # the optparse action
	    #                InputHandler=None, # Apply a function to the input value to convert it into the type expected by Parameter.DataType
	    #                ShortName='n', # a parameter short name, can be None
	    #                # Name='foo', # implied by Parameter.Name. Can be overwritten here if desired
	    #                # Required=False, # implied by Parameter.Required. Can be promoted by setting True
	    #                # Help='help', # implied by Parameter.Description. Can be overwritten here if desired
	    #                # Default=None, # implied by Parameter.Default. Can be overwritten here if desired
	    #                # DefaultDescription=None, # implied by Parameter.DefaultDescription. Can be overwritten here if desired
	    #                convert_to_dashed_name=True), # whether the Name (either implied by Parameter or defined above) should have underscores converted to dashes when displayed to the user
	    #
	    # An example option that does not have an associated Parameter.
	    # OptparseOption(Parameter=None,
	    #                InputType='new_filepath',
	    #                InputAction='store',
	    #                InputHandler=None, # we don't need an InputHandler because this option isn't being converted into a format that a Parameter expects
	    #                ShortName='o',
	    #                Name='output-fp',
	    #                Required=True,
	    #                Help='output filepath')

	    OptparseOption(Parameter=param_lookup('seqs'),
	                   InputType=<type 'list'>,
	                   InputAction='store', # default is 'store', change if desired
	                   InputHandler=None, # must be defined if desired
	                   ShortName=None), # must be defined if desired
	                   # Name='seqs', # implied by Parameter
	                   # Required=True, # implied by Parameter
	                   # Help='sequences to be summarized', # implied by Parameter
                   
	    OptparseOption(Parameter=param_lookup('suppress_length_summary'),
	                   InputType=<type 'bool'>,
	                   InputAction='store', # default is 'store', change if desired
	                   InputHandler=None, # must be defined if desired
	                   ShortName=None), # must be defined if desired
	                   # Name='suppress_length_summary', # implied by Parameter
	                   # Required=False, # implied by Parameter
	                   # Help='do not generate summary information on the sequence lengths', # implied by Parameter
	                   # Default=False, # implied by Parameter
	                   # DefaultDescription=None, # implied by Parameter


	]

	# outputs map result keys to output options and handlers. It is not necessary
	# to supply an associated option, but if you do, it must be an option from the
	# inputs list (above).
	outputs = [
	    # An example option that maps to a result key.
	    # OptparseResult(ResultKey='some_result',
	    #                OutputHandler=write_string, # a function applied to the value at ResultKey
	    #
	    #                # the name of the option (defined in inputs, above), whose
	    #                # value will be made available to OutputHandler. This name
	    #                # can be either an underscored or dashed version of the
	    #                # option name (e.g., 'output_fp' or 'output-fp')
	    #                OptionName='output-fp'), 
	    #
	    # An example option that does not map to a result key.
	    # OptparseResult(ResultKey='some_other_result',
	    #                OutputHandler=print_string)
	]


There are three lists of values that we'll need to populate here to define the optparse interface for our ``SequenceCollectionSummarizer`` command. These are the ``inputs``, the ``outputs``, and the ``usage_examples``. We'll also need to define an input handler and an output handler to tell the ``OptparseInterface`` how to take input from the command line and turn it into something that ``SequenceCollectionSummarizer`` can use, and to take output from ``SequenceCollectionSummarizer`` and turn it into something a command line user will want. ``make-optparse`` will auto-populate the ``inputs`` based on the ``Parameters``, but some changes will usually be required (detailed below). The following sections describe each of these steps.

.. note:: There is a fourth value that is required when defining an optparse interface, which is the version string of the command/interface (e.g., ``0.0.1``). This value has already been filled in for us in the configuration file template (see ``__version__`` at the top of the file). You can specify the version string when creating the configuration file template via ``--config-version``. In the example above, we specified a version string of ``0.0.1``.

Defining usage examples
-----------------------

The first thing to do when defining the ``OptparseInterface`` for our ``SequenceCollectionSummarizer`` command is define a set of usage examples. While in practice this documentation step may seem like something you'd want to do last, it's really helpful to do first to get you thinking about how you'd like to interact with your command from the command line. 

Usage examples are defined as instances of the ``pyqi.interface.optparse.UsageExample`` class, and are instantiated with three parameters: ``ShortDescription``, ``LongDescription``, and ``Ex``. ``Ex`` is the usage example itself, ``ShortDescription`` is a one sentence description of what ``Ex`` will do, and ``LongDescription`` elaborates on what ``Ex`` does. Find the ``usage_examples`` list in your new ``summarize_sequence_collection.py`` file, and replace its definition with::

	usage_examples = [
	    OptparseUsageExample(ShortDesc="Summarize the input sequence collection and write the result to file.",
	                         LongDesc="Read the file specified by -i, and compute the number of sequences in the file, and the minimum and maximum sequence lengths. Write all of that information to path specified by -o.",
	                         Ex="%prog -i seqs.fna -o seqs.summary.txt"),
	    OptparseUsageExample(ShortDesc="Summarize the input sequence collection and write the result to file, excluding information on sequence lengths.",
	                         LongDesc="Read the file specified by -i, compute the number of sequences in the file, and write that information to path specified by -o.",
	                         Ex="%prog -i seqs.fna -o seqs.summary.txt --suppress-length-summary")
	]

Here we define two usage examples, each of which gives us an idea about how we want our script to behave: we want it to take an ``i`` parameter (where the user passes their input file name), an ``o`` parameter (where the user passes their output file name), and an optional parameter called ``suppress-length-summary`` which controls some of the script behavior. 

 .. warning:: You shouldn't ever include the name of the script when defining ``UsageExample.Ex``, but instead include the text ``%prog``. This will be automatically replaced with the script name, so if you ever change the name of the script in the future, the change will take effect in all of your usage examples without you having to remember to update them.

Defining inputs
---------------

Next we'll define the list of ``inputs`` that should be associated with our ``OptparseInterface``. Each of these inputs will be an instance of a ``pyqi.core.interface.optparse.OptparseOption`` object. These will roughly map on to the ``Parameters`` that we defined for ``SequenceCollectionSummarizer``, but there are usually additional interface options relative to command parameters, as we'll see here. 

For the ``OptparseOptions`` that map onto ``Parameters`` directly, you can look up the corresponding ``Parameter`` in the ``param_lookup`` dictionary (which is created for you by ``make-optparse``), and most of the information in the ``OptparseOption`` will be auto-populated for you. ``make-optparse`` will actually fill in as much information as possible for each ``OptparseOption`` that corresponds to an existing ``Parameter``. 

In our example, you'll notice that there are two ``OptparseOptions`` that are already defined. There are a few values that may need to be changed here. In almost all cases, you'll need to change the ``InputType``, which is set to the ``Parameter``' ``DataType`` value by default, but should be updated to the ``optparse`` type. You can find discussion of these types in the :ref:`optparse type definitions <optparse-types>` section. Note that the ``InputType`` should be ``None`` for command line flags, as the type describes the value that is passed via that option, and command line flags don't take a value. The other value that often will need to be changed is ``InputHandler``, which tells ``OptparseInterface`` how to transform the ``OptparseOption`` into the corresponding ``Parameter``. In our case, for our ``seqs`` ``OptparseOption``, that involves converting a filepath into a list of tuples of (sequence id, sequence) pairs. First let's define the ``OptparseOptions``, and then we'll define a new ``InputHandler``.

The ``OptparseOptions`` corresponding to the existing ``Parameters`` should look like this::

	inputs = [

	    OptparseOption(Parameter=param_lookup('seqs'),
	                   InputType='existing_filepath',
	                   InputAction='store',
	                   InputHandler=parse_fasta,
	                   ShortName='i'),
                   
	    OptparseOption(Parameter=param_lookup('suppress_length_summary'),
	                   InputType=None,
	                   InputAction='store_true',
	                   InputHandler=None,
	                   ShortName=None),
	]

These definitions are exactly as generated by ``make-optparse``, except that many of the comments have been removed, and we've modified the ``InputTypes`` and the ``InputHandler`` for our ``seqs`` option. In the :ref:`next section <defining-input-handlers>` we'll define this new ``parse_fasta`` input handler, but first we'll add one more OptparseOption which is specific to our command line interface.

The output from our ``SequenceCollectionSummarizer`` is a dictionary, where some of the values are integers and some of the values may be ``None``. Generally a command line user will want to have information printed to stdout or to file. We'll define our interface so that the output is written to file with some basic formatting put in place. To do this, we need to define a new OptparseOption to allow the user to specify the path where output should be written. This ``OptparseOption`` does not map onto one of our existing ``Parameters``, and should be defined as follows::

	OptparseOption(Parameter=None,
	               InputType='new_filepath',
	               InputAction='store',
	               ShortName='o',
	               Name='output-fp',
	               Required=True,
	               Help='path where output should be written')

Notice the ``Parameter=None`` parameter here: this indicates that this ``OptparseOption`` does not correspond to one of the ``SequenceCollectionSummarizer`` parameters. 

You should include this ``OptparseOption`` definition in the ``inputs`` list to define the three options for our command line interface.

.. _defining-input-handlers:

Defining input handlers
-----------------------

Input handlers tell the ``OptparseInterface`` class how to take input from the command line and get it into the form that the ``Command`` is expecting. In our case, the user will be providing a filepath on the command line, and our ``SequenceCollectionSummarizer`` expects to receive a list (or other iterable object) of tuples of (sequence id, sequence) pairs. Our input handler is therefore a simple fasta parser, which is a `generator <http://docs.python.org/2/tutorial/classes.html#generators>`_ of (sequence id, sequence) tuples. We can define this as follows::

	def parse_fasta(fp):
	    """
	       fp: path to a fasta-formatted file
       
	       This function is a fasta record generator, yielding 
	        (sequence id, sequence) pairs when provided with a 
	        valid fasta file.
       
	       NO ERROR CHECKING IS PERFORMED!
	    """
	    # Always open files for reading in python using mode 'U'
	    # to correctly handle different types of line breaks
	    f = open(fp,'U')
	    seq_id = None
	    seq = []
	    for line in f:
	        line = line.strip()
	        if line.startswith('>'):
	            if len(seq) != 0:
	                # we've completed a fasta record
	                yield seq_id, ''.join(seq)
	            seq_id = line[1:]
	            seq = []
	        else:
	            seq.append(line)
	    yield seq_id, ''.join(seq)
	    f.close()

This definition can go in the interface configuration file that we've been working on in this tutorial. Alternatively, if your input handler is generally useful for your project you can centralize it within your project (see :ref:`organizing-your-repository`), or if you think it's generally useful for pyqi users, you should consider submitting it to the pyqi project :ref:`contributing it to pyqi <contributing-to-pyqi>`.

Defining outputs
----------------

The last thing we need to do is define which of the outputs generated by ``SequenceCollectionSummarizer`` are things we care about with this interface, and tell our ``OptparseInterface`` how to handle those. We do this by defining the ``outputs`` list of ``pyqi.core.interfaces.optparse.OptparseResult`` objects. In our case, we'll want to write all of the values that are not ``None`` to the filepath specified by the user with ``output-fp``. To do that, we need to handle three possible outputs, so we'll define those outputs and write an output handler. You should start with the stubbed ``outputs`` list to define how you want to handle each of the parameters. We'll do this as follows::

	outputs = [
	    OptparseResult(ResultKey='num-seqs',
	                   OutputHandler=append_datum_to_file,
	                   OptionName='output-fp'), 
	    OptparseResult(ResultKey='min-length',
	                   OutputHandler=append_datum_to_file,
	                   OptionName='output-fp'), 
	    OptparseResult(ResultKey='max-length',
	                   OutputHandler=append_datum_to_file,
	                   OptionName='output-fp'), 

	]

In this case, each of our ``OptparseResults`` are associated with a single ``OptionName``: ``output-fp``. We do this because each of these should be written to the same file, but in practice each of these could be associated with different ``OptionNames`` (e.g., if each should be written to a different file), or ``OptionName=None``, if (for example) a particular result should be written to stdout or stderr. We'll next define the new output handler, ``append_datum_to_file``, used by each of these ``OptparseResult`` objects.

Defining output handlers
------------------------

Each of these ``OptparseResult`` objects uses the same ``OutputHandler``, which we need to define now. This will take the result and write it to the file specified by the user as ``output-fp``. This should look like the following::

	def append_datum_to_file(result_key, data, option_value=None):
	    """Append summary information to a file.
	    """
	    # don't do anything if data is None
	    if data is None:
	        return
    
	    # If option_value is None when this output handler is called, 
	    # the interface developer did something wrong when defining
	    # the OptparseResults. Politely alert the developer that
	    # this output handler isn't associated with an option
	    # (it needs to be associated with an output filepath).
	    if option_value is None:
	        raise IncompetentDeveloperError(
	         "Cannot write output without a filepath.")
    
	    # open the output file for appending, and write the 
	    # summary information to a single tab-separated line
	    with open(option_value, 'a') as f:
	        f.write('%s\t%d\n' % (result_key, data))

Complete OptparseInterface configuration file
---------------------------------------------

At this stage we've fully configured our interface. The final interface configuration file should look like this::

	#!/usr/bin/env python
	from __future__ import division

	__author__ = "Greg Caporaso"
	__copyright__ = "Copyright 2013, Greg Caporaso"
	__credits__ = ["Greg Caporaso"]
	__license__ = "BSD"
	__version__ = "0.0.1"
	__maintainer__ = "Greg Caporaso"
	__email__ = "gregcaporaso@gmail.com"

	from pyqi.core.interfaces.optparse import (OptparseUsageExample,
	                                           OptparseOption, OptparseResult)
	from pyqi.core.command import make_parameter_collection_lookup_f
	from sequence_collection_summarizer import CommandConstructor
	from pyqi.core.exception import IncompetentDeveloperError
	import os

	param_lookup = make_parameter_collection_lookup_f(CommandConstructor)

	def parse_fasta(fp):
	    """
	       fp: path to a fasta-formatted file
       
	       This function is a fasta record generator, yielding 
	        (sequence id, sequence) pairs when provided with a 
	        valid fasta file.
       
	       NO ERROR CHECKING IS PERFORMED!
	    """
	    # Always open files for reading in python using mode 'U'
	    # to correctly handle different types of line breaks
	    f = open(fp,'U')
	    seq_id = None
	    seq = []
	    for line in f:
	        line = line.strip()
	        if line.startswith('>'):
	            if len(seq) != 0:
	                # we've completed a fasta record
	                yield seq_id, ''.join(seq)
	            seq_id = line[1:]
	            seq = []
	        else:
	            seq.append(line)
	    yield seq_id, ''.join(seq)

	def append_datum_to_file(result_key, data, option_value=None):
	    """Append summary information to a file.
	    """
	    # don't do anything if data is None
	    if data is None:
	        return
    
	    # If option_value is None when this output handler is called, 
	    # the interface developer did something wrong when defining
	    # the OptparseResults. Politely alert the developer that
	    # this output handler isn't associated with an option
	    # (it needs to be associated with an output filepath).
	    if option_value is None:
	        raise IncompetentDeveloperError(
	         "Cannot write output without a filepath.")
    
	    # open the output file for appending, and write the 
	    # summary information to a single tab-separated line
	    with open(option_value, 'a') as f:
	        f.write('%s\t%d\n' % (result_key, data))

	usage_examples = [
	    OptparseUsageExample(ShortDesc="Summarize the input sequence collection and write the result to file.",
	                         LongDesc="Read the file specified by -i, and compute the number of sequences in the file, and the minimum and maximum sequence lengths. Write all of that information to path specified by -o.",
	                         Ex="%prog -i seqs.fna -o seqs.summary.txt"),
	    OptparseUsageExample(ShortDesc="Summarize the input sequence collection and write the result to file, excluding information on sequence lengths.",
	                         LongDesc="Read the file specified by -i, compute the number of sequences in the file, and write that information to path specified by -o.",
	                         Ex="%prog -i seqs.fna -o seqs.summary.txt --suppress-length-summary")
	]

	inputs = [

	    OptparseOption(Parameter=param_lookup('seqs'),
	                   InputType='existing_filepath',
	                   InputAction='store',
	                   InputHandler=parse_fasta,
	                   ShortName='i'),
                   
	    OptparseOption(Parameter=param_lookup('suppress_length_summary'),
	                   InputType=None,
	                   InputAction='store_true',
	                   InputHandler=None,
	                   ShortName=None),

	    OptparseOption(Parameter=None,
	                   InputType='new_filepath',
	                   InputAction='store',
	                   ShortName='o',
	                   Name='output-fp',
	                   Required=True,
	                   Help='path where output should be written')
	]

	outputs = [
	    OptparseResult(ResultKey='num-seqs',
	                   OutputHandler=append_datum_to_file,
	                   OptionName='output-fp'), 
	    OptparseResult(ResultKey='min-length',
	                   OutputHandler=append_datum_to_file,
	                   OptionName='output-fp'), 
	    OptparseResult(ResultKey='max-length',
	                   OutputHandler=append_datum_to_file,
	                   OptionName='output-fp'), 

	]

.. _running-our-command:

Running our Command via its OptparseInterface
---------------------------------------------

To run this, there are a couple of additional things you need to do. First, you need to confirm that the directory where you've written these files is accessible via your ``PYTHONPATH``. For example, if you've been working in ``$HOME/code/pyqi_experiments/``, you should have ``$HOME/code/`` in your ``PYTHONPATH``. You can add that as follows::
	
	export PYTHONPATH=$HOME/code/:$PYTHONPATH

Next, so you can import from that directory, it'll need to contain an ``__init__.py`` file. That file can be empty, but it does need to exist. You can do this as follows::
	
	touch $HOME/code/pyqi_experiments/__init__.py

Now we're ready to run our ``Command`` via its ``OptparseInterface``. You can do this as follows::
	
	pyqi --command-config-module pyqi_experiments -- summarize-sequence-collection -h

This will print the help text associated with the ``summarize_sequence_collection`` ``OptparseInterface`` configuration file that we just created.

.. note:: The ``pyqi`` driver that we used above recognizes command names that match an ``OptparseInterface`` configuration file in the ``--command-config-module`` directory, minus the ``.py``. For example, we created a ``summarize_sequence_collection.py`` configuration file in the ``pyqi_experiments`` directory, so the ``pyqi`` driver recognizes the ``summarize_sequence_collection`` command. It also recognizes the dashed version of a command name, such as ``summarize-sequence-collection``. These names both map to the same command.

You can test the command by applying it to some sequence collection as follows::

	pyqi --command-config-module pyqi_experiments -- summarize-sequence-collection -i seqs.fna -o seqs.summary.txt

If ``seqs.fna`` contains the following::

	>s1
	ACCTTTAACC
	>s2
	CCGG
	>s3
	AAAAAAAAAAAAAAAAAAAAAAAAAAA

The resulting ``seqs.summary.txt`` should contain the following lines::

	num-seqs	3
	min-length	4
	max-length	27

Calling your command via the pyqi driver itself, as we're doing here, is a little clunky. Creating a project-specific driver however is very simple (it's a two-line shell script) and is covered in :ref:`defining-your-command-driver`.

.. _optparse-types:

OptparseOption Types
--------------------
pyqi defines several new option types in addition to the optparse's built-in option types. All of the available option types are:

+------------------------------+------------------------------------------------------------+
| option type                  | brief description                                          |
+==============================+============================================================+
| string                       | a string                                                   |
+------------------------------+------------------------------------------------------------+
| int                          | an int                                                     |
+------------------------------+------------------------------------------------------------+
| long                         | a long                                                     |
+------------------------------+------------------------------------------------------------+
| float                        | a float                                                    |
+------------------------------+------------------------------------------------------------+
| complex                      | a complex number                                           |
+------------------------------+------------------------------------------------------------+
| choice                       | one value from a list of choices                           |
+------------------------------+------------------------------------------------------------+
| existing_path                | path to an existing file or directory                      |
+------------------------------+------------------------------------------------------------+
| new_path                     | path to a new file or directory                            |
+------------------------------+------------------------------------------------------------+
| existing_filepath            | path to an existing file                                   |
+------------------------------+------------------------------------------------------------+
| existing_filepaths           | path to one or more existing files                         |
+------------------------------+------------------------------------------------------------+
| new_filepath                 | path to a new file                                         |
+------------------------------+------------------------------------------------------------+
| existing_dirpath             | path to an existing directory                              |
+------------------------------+------------------------------------------------------------+
| existing_dirpaths            | path to one or more existing directories                   |
+------------------------------+------------------------------------------------------------+
| new_dirpath                  | path to a new directory                                    |
+------------------------------+------------------------------------------------------------+
| multiple_choice              | one or more values from a list of choices                  |
+------------------------------+------------------------------------------------------------+
| blast_db                     | a blast database                                           |
+------------------------------+------------------------------------------------------------+

Thoughts and guidelines on designing command line interfaces
------------------------------------------------------------

Based on our experiences developing command line interfaces for `QIIME <http://www.qiime.org>`_, we've compiled some thoughts on best practices, which you can find in :ref:`optparse-guidelines`. 


