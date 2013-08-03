#!/usr/bin/env python

__author__ = "Greg Caporaso"
__copyright__ = "Copyright 2013, The QIIME Project"
__credits__ = ["Greg Caporaso"]
__license__ = "GPL"
__version__ = "0.1.0-dev"
__maintainer__ = "Greg Caporaso"
__email__ = "gregcaporaso@gmail.com"

from __future__ import division
from os import makedirs

from qiime.util import (parse_command_line_parameters, 
                        make_option, 
                        get_options_lookup,
                        load_qiime_config,)
from qiime.parse import parse_qiime_parameters
from qiime.workflow.util import (validate_and_set_jobs_to_start, call_commands_serially,
                            print_commands, no_status_updates, print_to_stdout)
from qiime.workflow.pick_open_reference_otus import (
                        pick_subsampled_open_reference_otus,
                        iterative_pick_subsampled_open_reference_otus)

from qcli.core.command import Command, Parameter

class PickOpenReferenceOTUs(Command):
    BriefDescription = "Assign OTUs using an open-reference OTU picking protocol"
    LongDescription = "OTUs are assigned to against the reference collection, and reads which do not hit the reference at greater than or equal to the similarity threshold are assigned de novo. This is the subsampled OTU picking workflow documented [here](http://qiime.org/tutorials/open_reference_illumina_processing.html)."

    def run(self, **kwargs):
        print_only = False
        if prefilter_percent_id == 0.0:
            prefilter_percent_id = None

        if otu_picking_method == 'uclust':
            denovo_otu_picking_method = 'uclust'
            reference_otu_picking_method = 'uclust_ref'
        elif otu_picking_method == 'usearch61':
            denovo_otu_picking_method = 'usearch61'
            reference_otu_picking_method = 'usearch61_ref'
        else:
            # it shouldn't be possible to get here
            self._logger.fatal(\
             'Unkown OTU picking method: %s' % otu_picking_method)

        parallel = parallel
        # No longer checking that jobs_to_start > 2, but
        # commenting as we may change our minds about this.
        #if parallel: raise_error_on_parallel_unavailable()

        if parameter_fp:
            try:
                parameter_f = open(parameter_fp, 'U')
            except IOError:
                self._logger.fatal(
                 "Can't open parameters file (%s). Does it exist? Do you have read access?"\
                 % parameter_fp)
            params = parse_qiime_parameters(parameter_f)
            parameter_f.close()
        else:
            params = parse_qiime_parameters([]) 
            # empty list returns empty defaultdict for now

        jobs_to_start = jobs_to_start
        default_jobs_to_start = qiime_config['jobs_to_start']
        validate_and_set_jobs_to_start(params,
                                       jobs_to_start,
                                       default_jobs_to_start,
                                       parallel,
                                       option_parser)

        try:
            makedirs(output_dir)
        except OSError:
            if force:
                pass
            else:
                self.logger.fatal("Output directory already exists. Please choose"
                    " a different directory, or force overwrite with -f.")

        if print_only:
            command_handler = print_commands
        else:
            command_handler = call_commands_serially

        if verbose:
            status_update_callback = print_to_stdout
        else:
            status_update_callback = no_status_updates

        if len(input_fps) == 1:
            pick_subsampled_open_reference_otus(input_fp=input_fps[0], 
                                      refseqs_fp=refseqs_fp,
                                      output_dir=output_dir,
                                      percent_subsample=percent_subsample,
                                      new_ref_set_id=new_ref_set_id,
                                      command_handler=command_handler,
                                      params=params,
                                      min_otu_size=min_otu_size,
                                      run_assign_tax=not suppress_taxonomy_assignment,
                                      run_align_and_tree=not suppress_align_and_tree,
                                      qiime_config=qiime_config,
                                      prefilter_refseqs_fp=prefilter_refseqs_fp,
                                      prefilter_percent_id=prefilter_percent_id,
                                      step1_otu_map_fp=step1_otu_map_fp,
                                      step1_failures_fasta_fp=step1_failures_fasta_fp,
                                      parallel=parallel,
                                      suppress_step4=suppress_step4,
                                      logger=None,
                                      denovo_otu_picking_method=denovo_otu_picking_method,
                                      reference_otu_picking_method=reference_otu_picking_method,
                                      status_update_callback=status_update_callback)
        else:    
            iterative_pick_subsampled_open_reference_otus(input_fps=input_fps,
                                  refseqs_fp=refseqs_fp,
                                  output_dir=output_dir,
                                  percent_subsample=percent_subsample,
                                  new_ref_set_id=new_ref_set_id,
                                  command_handler=command_handler,
                                  params=params,
                                  min_otu_size=min_otu_size,
                                  run_assign_tax=not suppress_taxonomy_assignment,
                                  run_align_and_tree=not suppress_align_and_tree,
                                  qiime_config=qiime_config,
                                  prefilter_refseqs_fp=prefilter_refseqs_fp,
                                  prefilter_percent_id=prefilter_percent_id,
                                  step1_otu_map_fp=step1_otu_map_fp,
                                  step1_failures_fasta_fp=step1_failures_fasta_fp,
                                  parallel=parallel,
                                  suppress_step4=suppress_step4,
                                  logger=None,
                                  denovo_otu_picking_method=denovo_otu_picking_method,
                                  reference_otu_picking_method=reference_otu_picking_method,
                                  status_update_callback=status_update_callback)

        def _get_parameters(self):
            # EXAMPLE:
            # return [Parameter(Name='foo',Required=True,Type=str,
            #                   Help='some required parameter),
            #         Parameter(Name='bar',Required=False,Type=int,
            #                   Help='some optional parameter,Default=1)]
            raise NotImplementedError("Must define _get_parameters.")

CommandConstructor = PickOpenReferenceOTUs
