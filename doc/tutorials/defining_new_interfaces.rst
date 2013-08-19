.. _defining-new-interfaces:

Defining new interfaces
=======================

After defining a new command and its API, as covered in :ref:`defining-new-commands`, you're ready to create a first user interface for that command. In this tutorial we'll define a command line interface for the ``SequenceCollectionSummarizer`` command. The differences that we'll need to handle here are that we'll want to user to provide their sequence collection on the command line, and we'll want to write the output to a filepath that the user specifies. This is different than what happens in ``SequenceCollectionSummarizer``, where the input and output are python objects. This is a very important distinction - since our derived ``Commands`` are meant to be interface-independent, they should not do things like require files as input. In some rare circumstances, it may be required for a ``Command`` to write files as its output.