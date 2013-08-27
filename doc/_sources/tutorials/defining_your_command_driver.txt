.. _defining-your-command-driver:

Defining your command driver
============================

It's possible to run your ``OptparseInterfaces`` using the ``pyqi`` command, as illustrated in :ref:`running-our-command`, but that mechanism is clunky and not how you'd want your users to interact with your software. To handle this more gracefully, you can create a shell script that can be distributed with your package and used as the primary driver for all ``OptparseInterfaces``. 

Creating the driver shell script
--------------------------------

To define a driver command for your project, create a new file named as you'd like your users to access your code. For example, the driver for the ``biom-format`` package is called ``biom``, and the driver for the ``pyqi`` package is called ``pyqi``. In this example our driver name will be ``my-project``. Add the following two lines to that file, replacing ``my-project`` with your driver name::

	#!/bin/sh
	exec pyqi --driver-name my-project --command-config-module my_project.interfaces.optparse.config -- "$@"

The value passed with ``--command-config-module`` must be the directory where the ``OptparseInterface`` configuration files can be found. If you followed the suggestions in :ref:`organizing-your-repository` the above should work.

The driver script should then be made executable with::

	chmod +x my-project

You'll next need to ensure that the directory containing this driver file is in your ``PATH`` environment variable. Again, if you followed the recommendations in :ref:`organizing-your-repository` and if your project directory is under ``$HOME/code``, you can do this by running::

	export PATH=$HOME/code/my-project/scripts/:$PATH

You should now be able to run::
	
	my-project

This will print a list of the commands that are available via the driver script, which will be all of the ``Commands`` for which you've defined ``OptparseInterfaces``. If one of these commands is called ``my-command``, you can now run it as follows to get the help text associated with that command::
	
	my-project my-command -h

The command names that you pass to the driver (``my-command``, in this example) match the name of the ``OptparseInterface`` config file, minus the ``.py``. The driver also matches the dashed version of a command name, so ``my-command`` and ``my_command`` both map to the same command.

Configuring bash completion
---------------------------

One very useful feature for your driver script is to enable tab-completion of commands and command line options (meaning that when a user starts typing the name of a command or an option, they can hit the tab key to complete it without typing the full name, if the name is unique). pyqi facilitates this with the ``pyqi make-bash-completion`` command. There are two steps in enabling tab completion. First, you'll need to generate the tab completion file, and then you'll need to edit your ``$HOME/.bash_profile`` file. 

To create the tab completion file for ``my-project``, run the following commands (again, this is assuming that your ``OptparseInterface`` config files are located as described in :ref:`organizing-your-repository`)::

	mkdir ~/.bash_completion.d
	pyqi make-bash-completion --command-config-module my_project.interfaces.optparse.config --driver-name my-project -o ~/.bash_completion.d/my-project

Then, add the following lines to your ``$HOME/.bash_profile`` file::

	# enable bash completion for pyqi-based scripts
	for f in ~/.bash_completion.d/*;
	do
	   source $f;
	done

When you open a new terminal, tab completion should work for the ``my-project`` commands and their options.
