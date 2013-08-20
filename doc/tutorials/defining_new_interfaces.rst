.. _defining-new-interfaces:

Defining new interfaces
=======================

After defining a new command and its API, as covered in :ref:`defining-new-commands`, you're ready to create a first user interface for that command. In this tutorial we'll define a command line interface for the ``SequenceCollectionSummarizer`` command. 

The main differences that need to be handled when defining a command line interface are that we'll want the user to provide their sequence collection on the command line, and we'll want to write the output to a file path that the user specifies on the command line. This is different than what happens in ``SequenceCollectionSummarizer``, where the input and output are python objects. This is a very important distinction - since our derived ``Commands`` are meant to be interface-independent, they should not do things like require files as input. In some rare circumstances, it may be required for a ``Command`` to write files as its output.

pyqi currently provides support for building command line interfaces based on python's `optparse <http://docs.python.org/2/library/optparse.html>`_ module. Your interface will ultimately be an instance of ``pyqi.interfaces.optparse.OptparseInterface``, but the interface class itself is generated dynamically. As a developer, you only define the configuration for the interface via in *interface configuration file* (which is a valid python file) - you won't actually define the interface class itself. If this sounds confusing, just get started - it's easier than it sounds.

Stubbing a new command line interface
-------------------------------------

pyqi provides a command, ``make_optparse``, that allows developers to easily define their optparse interface configuration files. After installing pyqi, you can get usage information by calling::

	pyqi make_optparse -h

To create your interface, you'll need to pass the ``Command`` as a fully specified python import (**WHAT DO YOU CALL THAT**), the name of the module where that ``Command`` is defined, and the path where the new configuration file should be written. For example, to create a stub for an optparse interface for our ``SequenceCollectionSummarizer`` command, you could run the following::

	pyqi make_optparse -c sequence_collection_summarizer.SequenceCollectionSummarizer -m sequence_collection_summarizer -o summarize_sequence_collection.py

.. warning:: For the above command to work, the directory containing ``sequence_collection_summarizer.py`` will need to be in your ``$PYTHONPATH``. 

The resulting file will look something like this::

```
	#!/usr/bin/env python

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

```

There are three specific things that we'll need to fill in here to define the optparse interface for our SequenceCollectionSummarizer command. These are the ``inputs``, the ``outputs``, and the ``usage_examples``. The following sections describe each of these steps.

Defining usage examples
-----------------------

The first thing to do when defining the optparse interface for our ``SequenceCollectionSummarizer`` command is define a set of usage examples. While this documentation step may seem like something you'd want to do last, it's really helpful to do first to get you thinking about how you'd like to interact with your command from the command line. 

Usage examples are defined as instances of the ``pyqi.interface.optparse.UsageExample`` class, and are instantiated with three parameters: ``ShortDescription``, ``LongDescription``, and ``Ex``. ``Ex`` is the usage example itself; ``ShortDescription`` is a one sentence description of what ``Ex`` will do, and ``LongDescription`` elaborates on what ``Ex`` does. Find the ``usage_examples`` list in your new ``summarize_sequence_collection.py`` file, and replace its definition with::

	usage_examples = [
	    OptparseUsageExample(ShortDesc="Summarize the input sequence collection and write the result to file.",
	                         LongDesc="Read the file at input_fp, and compute the number of sequences in the file, as well as the minimum and maximum sequence lengths. Write all of that information to output_fp.",
	                         Ex="%prog --input_fp seqs.fna --output_fp seqs.summary.txt"),
	    OptparseUsageExample(ShortDesc="Summarize the input sequence collection and write the result to file, excluding information on sequence lengths.",
	                         LongDesc="Read the file at input_fp, and compute the number of sequences in the file. Write that information to output_fp.",
	                         Ex="%prog --input_fp seqs.fna --output_fp seqs.summary.txt --suppress-length-summary")
	]

Here we define two usage examples, each of which gives us an idea about how we want our script to behave: we want it to take an ``input_fp``, an ``output_fp``, and an optional parameter called ``suppress-length-summary``. 

 .. warning:: Don't ever include the name of the script when defining ``UsageExample.Ex``, but instead include the text ``%prog``. This will be automatically replaced with the script name, so if you ever change the name of the script in the future, the change will take affect in all of your usage examples.


