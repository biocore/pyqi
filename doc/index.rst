Introduction
============

What is pyqi?
-------------

pyqi (canonically pronounced *pie chee*) is a Python framework designed to support wrapping general *commands* in multiple types of *interfaces*, including at the command line, HTML, and API levels. 

pyqi's only requirement is a working Python 2.7 installation.

Why should I care?
------------------

pyqi allows you to write your command once, and easily make it accessible to different types of users through different types of interfaces. In the context of pyqi, **a command is a class that takes some inputs, performs some function, and produces some outputs**. An interface is a light wrapper around that command that makes it accessible to users.

After defining and testing your command, you can **configure different types of interfaces**. This enables, for example, basic users to access your command through an **HTML interface** running on a local server, power or cluster users to access your command through a **command line interface**, and developers to access your command through an **application programmer interface (API)**. Because pyqi's interfaces are light wrappers around your underlying command, **users of each of these interfaces will be guaranteed to be accessing the same underlying functionality**.

pyqi is currently in the early stages of development, and there is a lot to be done. We're very interested in having beta users, and we fully embrace collaborative development, so if you're interested in using or developing pyqi, you should get in touch.


How do I start using pyqi?
--------------------------

First, install pyqi (it's easy) by following our :ref:`install instructions <install-index>`. Then, you can start working through our tutorials, which are designed to help you evaluate the utility of pyqi, and then integrate pyqi into your project.

The :ref:`Getting Started <getting-started>` series of tutorials progress linearly through :ref:`how to stub and build new commands <defining-new-commands>` and :ref:`how to stub and build new interfaces <defining-new-interfaces>`. These will give you an idea of what pyqi is capable of and how it works. 

The :ref:`using-pyqi-in-your-project` series of tutorials will then give you an idea of how you could integrate pyqi into your project. This includes suggestions on :ref:`how to organize your project's repository to look like other repositories that make use of pyqi <organizing-your-repository>`, and :ref:`how to define a driver script <defining-your-command-driver>` (similar to the ``pyqi`` command which you'll become familiar with in the :ref:`Getting Started <getting-started>` tutorials) that will give your users access to the commands in your project. 

As the pyqi project matures, we'll include additional :ref:`documentation for advanced developers <advanced-topics>`, who are interested in things like defining new interface types (though this is not something that is ever required for most developers).

How do I get help with pyqi?
----------------------------

For now, please direct questions to gregcaporaso@gmail.com. Please report bugs and feature requests on the `pyqi issue tracker <https://github.com/bipy/pyqi/issues>`_.

.. _contributing-to-pyqi:

Can I help develop pyqi?
------------------------

Yes! pyqi is open source software, available under the BSD license. All source code is hosted in the `pyqi GitHub repository <https://github.com/bipy/pyqi/>`_.

Development is primarily occurring in the `Caporaso Lab <http://www.caporaso.us>`_ (Northern Arizona University; Argonne National Laboratories) and `Knight Lab <https://knightlab.colorado.edu/>`_  (University of Colorado; Howard Hughes Medical Institute), but the goal is for pyqi to be a very open development effort. We accept code submissions as `pull requests <https://help.github.com/articles/using-pull-requests>`_.


