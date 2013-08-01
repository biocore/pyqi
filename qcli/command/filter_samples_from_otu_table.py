#!/usr/bin/env python
from __future__ import division

__author__ = "Greg Caporaso"
__copyright__ = "Copyright 2013, The QIIME Project"
__credits__ = ["Greg Caporaso", "Daniel McDonald", "Doug Wendel",
               "Jai Ram Rideout"]
__license__ = "GPL"
__version__ = "0.1.0-dev"
__maintainer__ = "Greg Caporaso"
__email__ = "gregcaporaso@gmail.com"

from numpy import inf
from qcli.command.core import Command, Parameter

class FilterSamplesFromOTUTable(Command):
    BriefDescription = "Filters samples from an OTU table on the basis of the number of observations in that sample, or on the basis of sample metadata. Mapping file can also be filtered to the resulting set of sample ids."
    LongDescription = ''

    def __init__(self, **kwargs):
        super(FilterSamplesFromOTUTable, self).__init__(**kwargs)

    def _get_parameters(self):
        return [
                Parameter(Type='biom-table',Help='the input otu table',Name='biom-table', Required=True),
                Parameter(Type=float,Help='the minimum total observation count in a sample for that sample to be retained',Name='min-count', Default=0),
                Parameter(Type=float,Help='the maximum total observation count in a sample for that sample to be retained',Name='max-count', Default=inf,DefaultDescription='infinity')]
    
    def run(self, **kwargs):
        print self.Parameters
