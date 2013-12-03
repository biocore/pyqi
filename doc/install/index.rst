.. _install-index:

Installing pyqi
===============

pyqi has no dependencies outside of Python, so installing is easy.

First, decide if you want to work with the release or development version of pyqi. If you work with the release version, you'll have the most recent stable version of pyqi, but may not have access to the latest and greatest features. If you're most interested in having access to the latest features and can tolerate some instability, you should work with the development version of pyqi. If you're unsure about what you want here, you should likely work with the release version.

Installing pyqi via pip
-----------------------

The easiest way to install the latest pyqi release is via pip::

	pip install pyqi

Instead, if you'd like to install the development version of pyqi::

	pip install git+git://github.com/bipy/pyqi.git

That's it!

Manually installing pyqi
------------------------

If you decided not to install pyqi using pip, you can install it manually with the following steps:

* To use the release version of pyqi, you can download it from `here <https://pypi.python.org/pypi/pyqi/>`_. The latest release is |release|. After downloading, unzip the file with ``tar -xzf pyqi-x.y.z.tar.gz`` and change to the new ``pyqi-x.y.z`` directory, where x.y.z corresponds to the downloaded version.

* To use the latest development version of pyqi you can download it from our `GitHub repository <https://github.com/bipy/pyqi>`_ using ``git clone git@github.com:bipy/pyqi.git``. After downloading, change to the new ``pyqi`` directory.

* Next, run ``python setup.py install``. That's it!

Enabling tab completion of pyqi commands and their command line options
-----------------------------------------------------------------------

After installation, you can optionally enable bash completion for pyqi scripts, meaning that when you start typing the name of a command or an option, you can hit the tab key to complete it without typing the full name, if the name is unique. There are two steps in enabling tab completion. First, you'll need to generate the tab completion file, and then you'll need to edit your ``$HOME/.bash_profile`` file. 

To create the tab completion file for ``pyqi``, run the following commands::

	mkdir ~/.bash_completion.d
	pyqi make-bash-completion --command-config-module pyqi.interfaces.optparse.config --driver-name pyqi -o ~/.bash_completion.d/pyqi

Then, add the following lines to your ``$HOME/.bash_profile`` file::

	# enable bash completion for pyqi-based scripts
	for f in ~/.bash_completion.d/*;
	do
	   source $f;
	done

When you open a new terminal, tab completion should work for the ``pyqi`` commands and their options. You can test this by typing ``pyqi make-c`` and then hitting the tab key (there should be no space after ``pyqi make-c``).
