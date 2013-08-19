.. _tutorial_index:
.. pyqi tutorials

.. index:: Tutorials

==================
pyqi tutorials
==================

.. _getting-started:

Getting started: defining new commands and interfaces using pyqi
----------------------------------------------------------------

This section of the documentation covers how to define a new ``Command``, its API, and its command line interface. You should work through these documents in order.

As an example, we'll define a new Command that provides a summary of a collection of biological sequences. We should be able to pass the sequences to the Command as a list of tuples, and the result from the command should contain the number of input sequences, the minimum sequence length, and the maximum sequence length. We'll use this example through-out this section of the tutorial.

.. toctree::
   :maxdepth: 2
   
   defining_new_commands.rst
   defining_new_interfaces.rst
   organizing_your_repository.rst

Advanced topics
---------------


