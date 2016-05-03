pyqi: expose your interface
===========================

[![Build Status](https://travis-ci.org/bipy/pyqi.png?branch=master)](https://travis-ci.org/bipy/pyqi)

**This project is no longer under active development. We have shifted to using [click](http://click.pocoo.org/) for our command line interfaces, and are now supporting different interface types more directly with the [QIIME 2 framework](https://github.com/qiime2/qiime2). You may be interested in exploring those two projects.**

pyqi (canonically pronounced *pie chee*) is designed to support wrapping general commands in multiple types of interfaces, including at the command line, HTML, and API levels. We're currently in the early stages of development, and there is a lot to be done. We're very interested in having beta users, and we fully embrace collaborative development, so if you're interested in using or developing pyqi, you should get in touch. For now, you can direct questions to gregcaporaso@gmail.com.

Development is primarily occurring in the [Caporaso](www.caporaso.us) and [Knight](https://knightlab.colorado.edu/) labs (at Northern Arizona University and University of Colorado, respectively), but the goal is for this to be a very open development effort. We accept code submissions as [pull requests](https://help.github.com/articles/using-pull-requests).

pyqi derives from code that was originally developed to support [QIIME](www.qiime.org)'s command line interface, but our interface needs for QIIME and other bioinformatics packages have expanded, and it now makes more sense that this be a stand-alone package.
