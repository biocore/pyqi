
Introduction
============

What is pyqi?
-------------

pyqi (canonically pronounced *pie chee*) is designed to support wrapping general *commands* in multiple types of *interfaces*, including at the command line, HTML, and API levels. 

Why should I care?
------------------

pyqi allows you to write your command once, and easily make it accessible to different types of users through different types of interfaces. In the context of pyqi, a command is a class that knows how to perform some function, and an interface is a light wrapper around that command that makes it accessible to users.

After defining and testing your command, you can **configure different types of interfaces**. This enables, for example, basic users to access your command through an **HTML interface** running on a local server, power or cluster users to access your command through a **command line interface**, and developers to access your command through an **application programmer interface (API)**. Because pyqi's interfaces are light wrappers around your underlying command, **users of each of these interfaces will be guaranteed to be accessing the same underlying functionality**.

pyqi is currently in the early stages of development, and there is a lot to be done. We're very interested in having beta users, and we fully embrace collaborative development, so if you're interested in using or developing pyqi, you should get in touch.

pyqi's only requirement is a working Python 2.7 installation.

How do I start using pyqi?
--------------------------

We've compiled tutorials to help you figure out what you need to evaluate the utility of pyqi, and then integrate pyqi into your project. The :ref:`Getting Started <getting-started>` series of tutorials progress linearly through :ref:`how to stub and build new commands <defining-new-commands>` and :ref:`how to stub and build new interfaces <defining-new-interfaces>`. These will give you an idea of what pyqi is capable of and how it works. The :ref:`using-pyqi-in-your-project` series of tutorials then give you an idea of how you could integrate pyqi into your project. This includes suggestions on :ref:`how to organize your project's repository to look like other repositories that make use of pyqi <organizing-your-repository>`, and how to define a driver script (similar to the ``pyci`` command) that will give your users access to the commands in your project. As the pyqi project stabilizes, we'll include additional :ref:`documentation for advanced developers <advanced-topics>`, who are interested in things like defining new interface types (though this is not something that is ever required for most users).

How do I get help with pyqi?
----------------------------

For now, please direct questions to gregcaporaso@gmail.com. Please report bugs and feature requests on the `pyqi issue tracker <https://github.com/bipy/pyqi/issues>`_.

.. _contributing-to-pyqi:

I'm sold. Can I help develop pyqi?
----------------------------------

Yes! pyqi is open source software, available under the BSD license.

Development is primarily occurring in the `Caporaso Lab <http://www.caporaso.us>`_ (Northern Arizona University; Argonne National Laboratories) and `Knight Lab <https://knightlab.colorado.edu/>`_  (University of Colorado; Howard Hughes Medical Institute), but the goal is for pyqi to be a very open development effort. We accept code submissions as `pull requests <https://help.github.com/articles/using-pull-requests>`_.

All source code is hosted in the `pyqi GitHub repository <https://github.com/bipy/pyqi/>`_.

Documentation index
-------------------

.. toctree::
   :maxdepth: 2

   install/index.rst
   tutorials/index.rst
   guidelines/index.rst
   scripts/index.rst


