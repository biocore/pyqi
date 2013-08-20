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

.. _using-pyqi-in-your-project:

Using pyqi in your project
--------------------------

After you've experimented with defining a toy pyqi ``Command``, its API, and an ``OptparseInterface``, you are ready to start thinking about integrating pyqi into your project. This section of the documentation begins by providing suggestions for organizing your code to match best with the organization of pyqi and projects that use pyqi. We then cover how to define a command line driver (similar to the ``pyqi`` command) that can be used with your optparse interfaces, to customize how your users will interact with your project. 

.. toctree::
   :maxdepth: 2
   
   organizing_your_repository.rst
   defining_your_command_driver.rst

Advanced topics
---------------


