.. _organizing-your-repository:

Organizing your repository
==========================

This document covers suggestions for organizing your repository to align with how pyqi and projects that use pyqi are organized. Following these guidelines is not a requirement, but may simplify using pyqi in your project. Version 1.1.3 of the `biom-format <http://www.biom-format.org>`_ project was the first project to use pyqi for its commands and interfaces, so the structure of that repository is used as an example here.


Structure of the biom-format project
------------------------------------

This directory tree (created with the unix ``tree`` command) illustrates the structure of the biom-format repository (some files that are not relevant to this discussion have been omitted to keep this as simple as possible). Annotations have been added following ``##`` to reference specific directories. 

::

	biom-format/
	├── ChangeLog
	├── COPYING
	├── doc
	├── examples
	├── images
	├── INSTALL
	├── python-code
	│   ├── biom ## Library code directory
	│   │   ├── biomdb.py
	│   │   ├── commands ## derived Command classes
	│   │   │   ├── __init__.py
	│   │   │   ├── installation_informer.py
	│   │   │   ├── metadata_adder.py
	│   │   │   ├── table_subsetter.py
	│   │   │   ├── table_summarizer.py
	│   │   │   └── table_validator.py
	│   │   ├── csmat.py
	│   │   ├── dbdata.py
	│   │   ├── exception.py
	│   │   ├── __init__.py
	│   │   ├── interfaces ## per-interface-type directories
	│   │   │   ├── __init__.py
	│   │   │   └── optparse ## derived OptparseInterface classes
	│   │   │       ├── config
	│   │   │       │   ├── add_metadata.py
	│   │   │       │   ├── __init__.py
	│   │   │       │   ├── show_install_info.py
	│   │   │       │   ├── subset_table.py
	│   │   │       │   ├── summarize_table.py
	│   │   │       │   └── validate_table.py
	│   │   │       ├── __init__.py
	│   │   │       ├── input_handler.py ## general purpose OptparseInterface input handler functions
	│   │   │       └── output_handler.py ## general purpose OptparseInterface output handler functions
	│   │   ├── parse.py
	│   │   ├── sparsedict.py
	│   │   ├── sparsemat.py
	│   │   ├── table.py
	│   │   ├── unit_test.py
	│   │   └── util.py
	│   ├── support-code
	│   └── tests ## Test code directory
	│       ├── bench
	│       ├── __init__.py
	│       ├── test_biomdb.py
	│       ├── test_commands # unit tests of the derived Command classes
	│       │   ├── __init__.py
	│       │   ├── test_installation_informer.py
	│       │   ├── test_metadata_adder.py
	│       │   ├── test_table_subsetter.py
	│       │   ├── test_table_summarizer.py
	│       │   └── test_table_validator.py
	│       ├── test_csmat.py
	│       ├── test_dbdata.py
	│       ├── test_interfaces # unit tests of input and output handlers
	│       │   ├── __init__.py
	│       │   ├── test_optparse
	│   │   │       ├── __init__.py
	│   │   │       ├── test_input_handler.py ## tests of OptparseInterface input handler functions
	│   │   │       └── test_output_handler.py ## tests of OptparseInterface output handler functions
	│       ├── test_parse.py
	│       ├── test_sparsedict.py
	│       ├── test_sparsemat.py
	│       ├── test_table.py
	│       ├── test_unit_test.py
	│       └── test_util.py
	├── R-code
	├── README.md
	├── scripts
	│   └── biom ## biom command driver
	├── setup.py
	└── support_files

Discussion of the biom-format directory structure
-------------------------------------------------

Under the ``biom`` *library code directory*, there are two directories that house pyqi-related code. The first is ``commands``, which contains derivations of the ``Command`` class (see :ref:`defining-new-commands` for discussion of these files). All of the ``biom-format`` commands are therefore defined in this directory. The second is ``interfaces``, which contains all of the derivations of the pyqi ``Interface`` class, and which are nested based on interface type. Currently ``biom-format`` only implements ``OptparseInterface`` classes, so there is only an ``optparse`` directory, but by nesting these on an per-interface-type basis we avoid name conflicts if multiple interfaces types were defined. 

Under the ``biom/interfaces/optparse`` directory, there is a ``config`` directory which contains all of the config files (see :ref:`defining-new-interfaces` for discussion of these files). There are also top-level ``input_handler.py`` and ``output_handler.py`` files. These files contain general purpose input and output handlers that may be used in multiple ``OptparseInterfaces``. Since input and output handlers are interface specific, it makes sense for these files to be contained under the ``biom/interfaces/optparse`` directory. 

Under the ``tests`` directory there are subdirectories for ``test_commands`` and ``test_interfaces``. The ``test_commands`` directory should contain a file corresponding to each file in the ``biom/commands`` directory, and should provide extensive unit testing of each of your commands. The ``test_interfaces`` directory is more minimal as typically there is not any functionality in the interfaces (the files are just providing configuration details). The exception is the input and output handlers, so there are test files corresponding to the files where those are defined. Note that the nesting of all test files matches the nesting in the library code directory.

Finally, under the ``scripts`` directory there is a single executable, ``biom``, which is the ``OptparseInterface`` command driver. This is a simple shell script that allows users to access the ``OptparseInterfaces`` defined in the ``biom-format`` project. Defining this script for your project is covered in :ref:`defining-your-command-driver`.

