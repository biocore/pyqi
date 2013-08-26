.. _defining-new-commands:

Defining new commands
=====================

A pyqi ``Command`` is a class that accepts inputs, does some work, and produces outputs. A ``Command`` is designed to be interface agnostic, so ideally should not be tied to a filesystem (i.e., it shouldn't do I/O or take filepaths) though there are some exceptions. Your ``Command`` class ultimately defines an API for your ``Command`` that can then easily be wrapped in other interface types (for example, a command line interface and/or a web interface) which handle input and output in an interface-specific way. This strategy also facilitates unit testing of your ``Command`` (by separating core functionality, which is essential to test, from interfaces, which can be very difficult to test in an automated fashion), parallel processing with your ``Command``, and constructing workflows that chain multiple ``Commands`` together. In general, your ``Command`` should take structured input (for example, a list of tuples or a numpy array), not a file that needs to be parsed.

This document describes how to create your first ``pyqi`` ``Command``.

Stubbing a new command
----------------------

After installing pyqi, you can easily stub (i.e., create templates for) new commands using ``pyqi make-command``. You can get usage information by calling::

	pyqi make-command -h

To create our sequence collection summarizer, we can start by stubbing a ``SequenceCollectionSummarizer`` class::

	pyqi make-command -n SequenceCollectionSummarizer -a "Greg Caporaso" -c "Copyright 2013, Greg Caporaso" -e "gregcaporaso@gmail.com" -l BSD --command-version 0.0.1 -o sequence_collection_summarizer.py

If you run this command locally, substituting your own name and email address where applicable, you'll have a new file called ``sequence_collection_summarizer.py``, which will look roughly like the following::

	#!/usr/bin/env python
	from __future__ import division

	__author__ = "Greg Caporaso"
	__copyright__ = "Copyright 2013, Greg Caporaso"
	__credits__ = ["Greg Caporaso"]
	__license__ = "BSD"
	__version__ = "0.0.1"
	__maintainer__ = "Greg Caporaso"
	__email__ = "gregcaporaso@gmail.com"

	from pyqi.core.command import Command, Parameter, ParameterCollection

	class SequenceCollectionSummarizer(Command):
	    BriefDescription = "FILL IN A 1 SENTENCE DESCRIPTION"
	    LongDescription = "GO INTO MORE DETAIL"
	    Parameters = ParameterCollection([
	        Parameter(Name='foo', DataType=str,
	                  Description='some required parameter', Required=True),
	        Parameter(Name='bar', DataType=int,
	                  Description='some optional parameter', Required=False,
	                  Default=1)
	    ])

	    def run(self, **kwargs):
	        # EXAMPLE:
	        # return {'result_1': kwargs['foo'] * kwargs['bar'],
	        #         'result_2': "Some output bits"}
	        raise NotImplementedError("You must define this method")

	CommandConstructor = SequenceCollectionSummarizer

Defining a command
------------------

There are several values that you'll need to fill in to define your command based on the stub that is created by ``make-command``. The first, which are the easiest, are ``BriefDescription`` and ``LongDescription``. ``BriefDescription`` should be a one sentence description of your command, and ``LongDescription`` should be a more detailed explanation (usually 2-3 sentences). These are used in auto-generated documentation.

Next, you'll need to define the parameters that your new command can take. Each of these parameters will be an instance of the ``pyqi.core.command.Parameter`` class.

Our ``SequenceCollectionSummarizer`` command will take one required parameter and one optional parameter. The required parameter will be called ``seqs``, and will be a list (or some other iterable type) of tuples of (sequence identifier, sequence) pairs. For example::

	[('sequence1','ACCGTGGACCAA'),('sequence2','TGTGGA'), ...]

We'll also need to provide a description of this parameter (used in documentation), its type, and indicate that it is required. The final Parameter definition should look like this::

	Parameter(Name='seqs', DataType=list,
	         Description='sequences to be summarized', Required=True)

The optional parameter will be called ``suppress_length_summary``, and if passed will indicate that we don't want information on sequence lengths included in our output summary. The ``Parameter`` definition in this case should look like this::

	Parameter(Name='suppress_length_summary', DataType=bool,
	         Description='do not generate summary information on the sequence lengths', 
	         Required=False, Default=False)

The only additional ``Parameter`` that is passed here, relative to our ``seqs`` parameter, is ``Default``. Because this parameter isn't required, it's necessary to give it a default value here. All of the ``Parameters`` should be included in a ``pyqi.core.command.ParameterCollection`` object (as in the stubbed file).

.. note:: There are a few restrictions on what ``Name`` can be set to for a ``Parameter``. It must be a `valid python identifier <http://docs.python.org/2/reference/lexical_analysis.html#identifiers>`_ (e.g., it cannot contain ``-`` characters or begin with a number) so the ``Command`` can be called with named options instead of passing a dict. ``Parameter`` names also must be unique for a ``Command``.

Next, we'll need to define what our ``Command`` will actually do. This is done in the ``run`` method, and all results are returned in a dictionary. The run method for our ``SequenceCollectionSummarizer`` object would look like the following::

	def run(self, **kwargs):
	    """
	    """
	    num_seqs = 0
	    sequence_lengths = []
	    for seq_id, seq in kwargs['seqs']:
	        num_seqs += 1
	        sequence_lengths.append(len(seq))
       
	    if kwargs['suppress_length_summary']:
	        min_length = None
	        max_length = None
	    else:
	        min_length = min(sequence_lengths)
	        max_length = max(sequence_lengths)
   
	    return {'num-seqs':num_seqs,
	            'min-length':min_length,
	            'max-length':max_length}

In practice, if your ``Command`` is more complex than our ``SequenceCollectionSummarizer`` (which it probably is), you can define other methods that are called by ``run``. These should likely be private methods.

.. note:: ``kwargs`` is validated prior to ``run`` being called, so that any required ``kwargs`` that are missing will raise an error, and any optional ``kwargs`` that are missing will have their default values filled in. To customize the validation that is performed on ``kwargs`` for your ``Command`` you should override ``_validate_kwargs`` in your ``Command``.

A complete example Command
--------------------------

The following illustrates a complete python file defining a new pyqi ``Command``::

	#!/usr/bin/env python
	from __future__ import division

	__author__ = "Greg Caporaso"
	__copyright__ = "Copyright 2013, Greg Caporaso"
	__credits__ = ["Greg Caporaso"]
	__license__ = "BSD"
	__version__ = "0.0.1"
	__maintainer__ = "Greg Caporaso"
	__email__ = "gregcaporaso@gmail.com"

	from pyqi.core.command import Command, Parameter, ParameterCollection

	class SequenceCollectionSummarizer(Command):
	    BriefDescription = "Generate summary statistics on a collection of sequences."
	    LongDescription = "Provide the number of sequences, the minimum sequence length, and the maximum sequence length given a collection of sequences. Sequences should be provided as a list (or other iterable object) of tuples of (sequence id, sequence) pairs."
	    Parameters = ParameterCollection([
	        Parameter(Name='seqs', DataType=list,
	                  Description='sequences to be summarized', Required=True),
	        Parameter(Name='suppress_length_summary', DataType=bool,
	                  Description='do not generate summary information on the sequence lengths', 
	                  Required=False,Default=False)
	    ])

	    def run(self, **kwargs):
	        """
	        """
	        num_seqs = 0
	        sequence_lengths = []
	        for seq_id, seq in kwargs['seqs']:
	            num_seqs += 1
	            sequence_lengths.append(len(seq))
            
	        if kwargs['suppress_length_summary']:
	            min_length = None
	            max_length = None
	        else:
	            min_length = min(sequence_lengths)
	            max_length = max(sequence_lengths)
        
	        return {'num-seqs':num_seqs,
	                'min-length':min_length,
	                'max-length':max_length}

	CommandConstructor = SequenceCollectionSummarizer

At this stage you have defined a new command and its API. To access the API in the python terminal, you could do the following::

	# Import your new class
	>>> from sequence_collection_summarizer import SequenceCollectionSummarizer
	# Instantiate it
	>>> s = SequenceCollectionSummarizer()
	# Call the command, passing a list of (seq id, sequence) tuples as input. 
	# Note that because the parameters are provided as kwargs, you need to 
	# pass the parameter with a keyword.
	>>> r = s(seqs=[('sequence1','ACCGTGGACCAA'),('sequence2','TGTGGA')])
	# You can now see the full output of the command by inspecting the 
	# result dictionary.
	>>> r
	{'max-length': 12, 'min-length': 6, 'num-seqs': 2}
	# Alternatively, you can access each value independently, as with any dictionary.
	>>> print r['num-seqs']
	2
	>>> print r['min-length']
	6
	>>> print r['max-length']
	12
	# You can call this command again with different input.
	# For example, we can call the command again passing the
	# suppress_length_summary parameter.
	>>> r = s(seqs=[('sequence1','ACCGTGGACCAA'),('sequence2','TGTGGA')],suppress_length_summary=True)
	>>> r
	{'max-length': None, 'min-length': None, 'num-seqs': 2}

