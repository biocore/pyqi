
Documentation
=============

About qcli
----------

qcli (canonically pronounced *queue sea el eye*) contains tools for developing and testing command line interfaces in Python. Features include:

 * A consistent look-and-feel for all of your script interfaces and their associated help text. Building your first working qcli-based script is as easy as installing qcli and running ``qcli_make_script``. 
 * An automated test framework, which can supplement unit tests (which typically don't test command line interfaces) to alert you of changes that break your usage examples.
 * An automated documentation framework. Sphinx-compatible rst files can be auto-generated for your qcli scripts.

qcli is being designed to make `QIIME <http://www.qiime.org>`_'s Command Line Interface framework a standalone package so it can be used in tools other than QIIME without the very heavy-weight dependency of QIIME itself. The name of this package may change as it reaches maturity. qcli is very light-weight. Its only requirement is a working Python 2.6 installation. 

Documentation index
-------------------

.. toctree::
   :maxdepth: 2

   install/index.rst
   tutorials/index.rst
   guidelines/index.rst
   scripts/index.rst

Getting involved in development
-------------------------------

qcli is open source software, available under GPL.

Development is currently occurring primarily in the `Caporaso <http://www.caporaso.us>`_ and `Knight <https://knightlab.colorado.edu/>`_ labs (at Northern Arizona University and University of Colorado, respectively), but the goal is for qcli to be a very open development effort. 

All source code is hosted in the `qcli GitHub repository <https://github.com/bipy/qcli/>`_. We accept code submissions as `pull requests <https://help.github.com/articles/using-pull-requests>`_.

Getting help with qcli
----------------------

For now, please direct questions to gregcaporaso@gmail.com. Please report bugs and feature requests on the `qcli issue tracker <https://github.com/bipy/qcli/issues>`_.

