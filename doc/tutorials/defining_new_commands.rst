.. _defining-new-commands:

Defining new commands
=====================



Stubbing a new command
----------------------

After installing pyqi, you can easily stub new commands using ``pyqi make_command``. You can get usage information by calling::

	pyqi make_command -h

To create our sequence collection summarizer, we can start by creating a ``SequenceCollectionSummarizer`` class::

	pyqi make_command -n SequenceCollectionSummarizer -a "Greg Caporaso" -c "Copyright 2013, Greg Caporaso" -e "gregcaporaso@gmail.com" -l BSD --command-version 0.0.1 -o sequence_collection_summarizer.py

If you run this command locally, substituting your own name and email address where applicable, you'll have a new file called ``sequence_collection_summarizer.py``, which will look roughly like the following::

	#!/usr/bin/env python

	from __future__ import division
	from pyqi.core.command import Command, Parameter, ParameterCollection

	__author__ = "Greg Caporaso"
	__copyright__ = "Copyright 2013, Greg Caporaso"
	__credits__ = ["Greg Caporaso"]
	__license__ = "BSD"
	__version__ = "0.0.1"
	__maintainer__ = "Greg Caporaso"
	__email__ = "gregcaporaso@gmail.com"

	from __future__ import division
	from pyqi.core.command import Command, Parameter

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

There are several values that you'll need to fill in to define your command based on the stub that is created by ``make_command``. The first, which are the easiest, are ``BriefDescription`` and ``LongDescription``. ``BriefDescription`` should be a one sentence description of your command, and ``LongDescription`` should be a more detail explanation (usually 2-3 sentences). 

Next, you'll need to define the parameters that your new command can take. Each of these parameters will be an instance of the pyqi.core.command.Parameter class.

For our command, we'll define one required parameter and one optional parameter. The required parameter will be called ``seqs``, and will be a list of tuples of (sequence identifier, sequence) pairs. For example::

	[('sequence1','ACCGTGGACCAA'),('sequence2','TGTGGA'), ...]

We'll also need to provide a description of this parameter (used in documentation), its type, and indicate that it is required. The final Parameter definition should look like this::

	Parameter(Name='seqs', DataType=list,
	         Description='sequences to be summarized', Required=True)

The optional parameter will be called ``suppress_length_summary``, and if passed will indicate that we don't want information on sequence lengths included in our output summary. The ``Parameter`` definition in this case should look like this::

	Parameter(Name='suppress_length_summary', DataType=bool,
	         Description='do not generate summary information on the sequence lengths', 
	         Required=False,Default=False)

The only additional ``Parameter`` that is passed here, relative to our ``seqs`` parameter, is ``Default``. Because this parameter isn't required, it's necessary to give it a default value here.

Next, you'll need to define what your command will actually do. This is done in the ``run`` method, and all results are returned in a dictionary. The run method for our ``SequenceCollectionSummarizer`` object would look like the following::

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

A complete example command
--------------------------

The following illustrates a complete file defining a new pyqi Command::

	#!/usr/bin/env python

	from __future__ import division
	from pyqi.core.command import Command, Parameter, ParameterCollection

	__author__ = "Greg Caporaso"
	__copyright__ = "Copyright 2013, Greg Caporaso"
	__credits__ = ["Greg Caporaso"]
	__license__ = "BSD"
	__version__ = "0.0.1"
	__maintainer__ = "Greg Caporaso"
	__email__ = "gregcaporaso@gmail.com"

	class SequenceCollectionSummarizer(Command):
	    BriefDescription = "Generate summary statistics on a collection of sequences."
	    LongDescription = "Provided the number of sequences, the minimum sequence length, and the maximum sequence length given a collection of sequences. Sequences should be provided as a list (or generator) of tuples of (sequence id, sequence) pairs."
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

At this stage you have defined a new command its API. To access the API in the python terminal, you could do the following::

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
	# You can now call this command again, either with different input or different 
	# parameter settings. For example, we can call the command again passing the 
	# suppress_length_summary parameter.
	>>> r = s(seqs=[('sequence1','ACCGTGGACCAA'),('sequence2','TGTGGA')],suppress_length_summary=True)
	>>> r
	{'max-length': None, 'min-length': None, 'num-seqs': 2}

