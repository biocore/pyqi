#!/usr/bin/env python

from qcli.interface.cli import CLOption, UsageExample, ParameterConversion
from qcli.qiime_backports.command.filter_samples_from_otu_table import FilterSamplesFromOTUTable as \
        CommandConstructor

usage_examples = [
        UsageExample(ShortDesc="Abundance filtering (low coverage)",
                     LongDesc="Filter samples with fewer than 150 observations from the otu table.",
                     Ex="%prog -i otu_table.biom -o otu_table_no_low_coverage_samples.biom -n 150"),
        UsageExample(ShortDesc="Abundance filtering (high coverage)",
                     LongDesc="Filter samples with fewer than 150 observations from the otu table.",
                     Ex="%prog -i otu_table.biom -o otu_table_no_high_coverage_samples.biom -x 149")
        ]

param_conversions = {
        'biom-table':ParameterConversion(ShortName="i",
                                         LongName="input_fp",
                                         CLType="existing_filepath"),
        'min-count':ParameterConversion(ShortName="n",
                                        LongName="min_count",
                                        CLType="float")
        }

additional_options = [
        CLOption(Type='biom-table',
                 Help='the output otu table',
                 Name='biom-table',
                 Required=True,
                 LongName='output_fp',
                 CLType='new_filepath',
                 ShortName='o')
        ]
