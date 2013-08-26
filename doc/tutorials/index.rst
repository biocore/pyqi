.. _tutorial_index:
.. pyqi tutorials

.. index:: Tutorials

==================
pyqi tutorials
==================

Installing pyqi
---------------

Before working through the tutorials below you'll need to have a working installation of pyqi (it's really easy to install). See our :ref:`install instructions <install-index>` before you get started.

.. _getting-started:

Getting started: defining new commands and interfaces using pyqi
----------------------------------------------------------------

This section of the documentation covers how to define a new ``Command``, its API, and its command line interface. You should work through these documents in order.

As an example, we'll define a new ``Command`` that provides a summary of a collection of biological sequences. (*Biological sequences*, in this context, are DNA sequences. These are `canonically represented <http://www.bioinformatics.org/sms2/iupac.html>`_ as strings of primarily ``A``, ``C``, ``G``, and ``T`` characters, and `fasta format <http://en.wikipedia.org/wiki/FASTA_format>`_ is the most common file format for storing biological sequences on disk.) We'll be able to pass the sequences to the ``Command``, and the result from the ``Command`` will be the number of sequences in the collection, the minimum sequence length, and the maximum sequence length. We'll then wrap that ``Command`` in an ``OptparseInterface``, which will allow users to access it from the command line providing a fasta file as input and having a summary written to file as output.

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

.. _advanced-topics:

Advanced topics
---------------

As pyqi matures we'll include tutorials covering topics such as how to define new interface types. However, given the early state of development that we're currently in, these will likely change a lot, so we recommend that if you are interested in developing new interface types now, that you get in touch (you can e-mail gregcaporaso@gmail.com for now) to discuss what you'd like to do, and possibly get involved with development of pyqi. 
