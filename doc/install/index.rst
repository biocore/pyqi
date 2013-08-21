.. _install-index:

Installing pyqi
===============

pyqi has no dependencies outside of Python, so installing is easy.

* First, decide if you want to work with the release or development version of pyqi. If you work with the release version, you'll have the most recent stable version of pyqi, but may not have access to the latest and greatest features. If you're most interested in having access to the latest features and can tolerate some instability, you should work with the development version of pyqi.

 * To use the latest development version of pyqi you can download it from our `GitHub repository <https://github.com/bipy/pyqi>`_. You can do this by downloading the zip file linked from that page, or with ``git clone`` for ``git`` users. If you download as a zip, uncompress the downloaded file. Currently we do not create releases of pyqi, as the ``master`` branch is designed to always be release-quality code, so you should just always work with the head of the master branch.
 * To use the release version of pyqi, you can download it from `here <NEED LINK!!>`_.

* Next, change to the pyqi directory with ``cd pyqi`` (this will be called ``pyqi-master`` if you downloaded and uncompressed the zip file, so you'd change to that directory with ``cd pyqi-master``).
* Finally, run ``python setup.py install``.

That's it!