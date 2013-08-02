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

from itertools import izip
from numpy import inf, isinf
from qcli.command.core import Command, Parameter

from biom.parse import parse_biom_table

from qiime.parse import parse_mapping_file
from qiime.filter import (sample_ids_from_metadata_description, 
                          filter_samples_from_otu_table,
                          filter_mapping_file)
from qiime.format import format_mapping_file, format_biom_table

class FilterSamplesFromOTUTable(Command):
    BriefDescription = "Filters samples from an OTU table on the basis of the number of observations in that sample, or on the basis of sample metadata. Mapping file can also be filtered to the resulting set of sample ids."
    LongDescription = ''

    def __init__(self, **kwargs):
        super(FilterSamplesFromOTUTable, self).__init__(**kwargs)

    def _get_parameters(self):
        return [
                Parameter(Type='biom-table',Help='the input otu table',Name='biom-table', Required=True),
                Parameter(Type=float,Help='the minimum total observation count in a sample for that sample to be retained',Name='min-count', Default=0),
                Parameter(Type=float,Help='the maximum total observation count in a sample for that sample to be retained',Name='max-count', Default=inf,DefaultDescription='infinity'),
                Parameter(Type='sample-metadata',Help='the sample metadata',Name='sample-metadata', Default=None),
                Parameter(Type='sample-metadata',Help='the filtered sample metadata',Name='filtered-sample-metadata', Default=None,DefaultDescription='filtered mapping file is not written'),
                Parameter(Type=list,Help='list of sample ids to keep',Name='samples-to-keep', Default=None),
                Parameter(Type=str,Help='string describing valid states',Name='metadata-description', Default=None)
               ]
    
    def run(self,
            input_fp,
            output_fp,
            mapping_fp=None,
            output_mapping_fp=None,
            valid_states=None,
            min_count=None,
            max_count=None,
            sample_id_fp=None,
            **kwargs):
        result = {}
        if not ((mapping_fp and valid_states) or 
                min_count != 0 or 
                not isinf(max_count) or
                sample_id_fp != None):
            self._logger.fatal("No filtering requested. Must provide either "
                         "mapping_fp and valid states, min counts, "
                         "max counts, or sample_id_fp (or some combination of those).")
        if output_mapping_fp and not mapping_fp:
            self._logger.fatal("Must provide input mapping file to generate"
                                " output mapping file.")

        otu_table = parse_biom_table(open(input_fp,'U'))
        output_f = open(output_fp,'w')
        
        result['output-biom-table'] = output_fp
    
        if (mapping_fp and valid_states):
            sample_ids_to_keep = sample_ids_from_metadata_description(
                                  open(mapping_fp,'U'),valid_states)
        else:
            sample_ids_to_keep = otu_table.SampleIds
    
        if (sample_id_fp != None):
            sample_id_f_ids = set([l.strip().split()[0] for l in open(sample_id_fp,'U') if not l.startswith('#')])
            sample_ids_to_keep = set(sample_ids_to_keep) & sample_id_f_ids
    
        filtered_otu_table = filter_samples_from_otu_table(otu_table,
                                                            sample_ids_to_keep,
                                                            min_count,
                                                            max_count)
        output_f.write(format_biom_table(filtered_otu_table))
        output_f.close()
    
        # filter mapping file if requested
        if output_mapping_fp:
            mapping_data, mapping_headers, _ = parse_mapping_file(open(mapping_fp,'U'))
            mapping_headers, mapping_data = \
             filter_mapping_file(mapping_data, mapping_headers, filtered_otu_table.SampleIds)
            open(output_mapping_fp,'w').write(format_mapping_file(mapping_headers,mapping_data))
        
        return result 
