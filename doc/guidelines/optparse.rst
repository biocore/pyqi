.. _optparse-guidelines:

Guidelines for creating pyqi-based optparse interfaces
==========================================================

This document covers some general suggestions for ``OptparseInterfaces`` with pyqi. These ideas have evolved from our experiences with `QIIME <http://www.qiime.org>`_. Ideally this document will continue to evolve with time, so if you have suggestions for things that should be included please consider submitting them as a `pull request <https://help.github.com/articles/using-pull-requests>`_.  

**Design convenient command line interfaces.** The goal of your interface is to make things easy for the user (who is often you). This section covers some guidelines for how to do that.

**Have people who are better programmers than you interact with your command line interface and give you feedback on it.** If your script is difficult to work with, or has requirements that are not intuitive for users who frequently work with command line applications, people won't use your code. 

**If there are tasks that are automatable, automate them.** For example, if you can make a good guess at what an output file should be named from an input file and a parameter choice, do that and use it as the default output path (but allow the user to overwrite it with a command line option).

**Define sensible default values for your command line options.** If most of the time that a script is used it will require a parameter to be set to a certain value, make that value the default to simplify the interface.

**Have the user specify named options rather than positional arguments.** The latter are more difficult to work with as users need to remember the order that they need to be passed. pyqi scripts do not allow positional arguments. Note that the idea of avoiding positional arguments contradicts `what Python's optparse docs say <http://docs.python.org/2/library/optparse.html#what-are-options-for>`_. We disagree with their comment that all required options should be passed as positional arguments. 

**Avoid making assumptions about how a script will be run.** Perhaps most importantly, don't assume that the script will be run from the same directory that the script lives in. Users often want to copy executables into a centralized directory on their system (e.g., ``/usr/local/bin``). Facilitate that by not requiring that the script is run from a specific location. If you rely on data files, you have other options such as having users set an environment variable that defines where data files live on the system. Test your script from multiple locations on the file system!

**Test calling your script in invalid ways to ensure that it provides informative error messages.** Python's traceback errors are generally not very informative for users, so you should test calling your scripts incorrectly to detect cases when the script might result in uninformative error messages. You should then catch these cases and provide useful error messages. 

**Define where output will be stored based on how many output files are created.** If a single file is created by your script, give the user control over the output filepath on the command line (usually with a parameter named ``-o`` or ``--output-fp``). If multiple files are created by your script, allow the user to define a directory name, and store all of the output files in that directory with names that you pre-define within your script. Define these options using the option types ``new_filepath`` and ``new_dirpath``, respectively. These will raise errors if the file or directory already exists, which is generally good as it avoids overwriting results that may have taken a long time to generate. We've found that this is the most convenient way for users to define where the output of scripts should live, but there are likely special cases where you'd want to deviate from this general guideline. Do *always* give the user control over the name of either the file or the directory where output will be created. You don't want them to have to move a file to a different location if they want to run your script multiple times.
