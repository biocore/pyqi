#!/usr/bin/env python

__author__ = "Greg Caporaso"
__copyright__ = "Copyright 2013, The QIIME Project"
__credits__ = ["Greg Caporaso", "Daniel McDonald", "Doug Wendel",
               "Jai Ram Rideout"]
__license__ = "GPL"
__version__ = "0.1.0-dev"
__maintainer__ = "Greg Caporaso"
__email__ = "gregcaporaso@gmail.com"

from pyqi.interface.cli import CLOption, UsageExample, ParameterConversion
from pyqi.qiime_backports.command.filter_samples_from_otu_table import FilterSamplesFromOTUTable as \
        CommandConstructor


usage_examples = [
        UsageExample(ShortDesc="Abundance filtering (low coverage)",
                     LongDesc="Filter samples with fewer than 150 observations from the otu table.",
                     Ex="%prog -i otu_table.biom -o otu_table_no_low_coverage_samples.biom -n 150"),
        UsageExample(ShortDesc="Abundance filtering (high coverage)",
                     LongDesc="Filter samples with fewer than 150 observations from the otu table.",
                     Ex="%prog -i otu_table.biom -o otu_table_no_high_coverage_samples.biom -x 149"),
        UsageExample(ShortDesc="Metadata-based filtering (positive)",
                     LongDesc="Filter samples from the table, keeping samples where the value for 'Treatment' in the mapping file is 'Control'",
                     Ex="%prog -i otu_table.biom -o otu_table_control_only.biom -m map.txt -s 'Treatment:Control'"),
        UsageExample(ShortDesc="Metadata-based filtering (negative)",
                     LongDesc="Filter samples from the table, keeping samples where the value for 'Treatment' in the mapping file is not 'Control'",
                     Ex="%prog -i otu_table.biom -o otu_table_not_control.biom -m map.txt -s 'Treatment:*,!Control'"),
        UsageExample(ShortDesc="List-based filtering",
                     LongDesc="Filter samples where the id is listed in samples_to_keep.txt",
                     Ex="%prog -i otu_table.biom -o otu_table_samples_to_keep.biom --sample_id_fp samples_to_keep.txt")
        ]

param_conversions = {
        'biom-table':ParameterConversion(ShortName="i",
                                         LongName="input_fp",
                                         CLType="existing_filepath"),
        'min-count':ParameterConversion(ShortName="n",
                                        LongName="min_count",
                                        CLType=float),
        'max-count':ParameterConversion(ShortName="x",
                                        LongName="max_count",
                                        CLType=float),
        'sample-metadata':ParameterConversion(ShortName='m',
                                              LongName='mapping_fp',
                                              CLType='existing_filepath'),
        'metadata-description':ParameterConversion(ShortName='s',
                                                   LongName='valid_states',
                                                   CLType=str),
        'samples-to-keep':ParameterConversion(ShortName=None,
                                           LongName='sample_id_fp',
                                           CLType='existing_filepath'),
        'filtered-sample-metadata':ParameterConversion(ShortName=None,
                                                       LongName='output_mapping_fp',
                                                       CLType='new_filepath')
        }

additional_options = [
        CLOption(Type='biom-table',
                 Help='the output otu table',
                 Name='biom-table',
                 Required=True,
                 LongName='output_fp',
                 CLType='new_filepath',
                 ShortName='o'),
        ]

output_map = {}
