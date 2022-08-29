#!/bin/bash

## Run mriqc on bids-compliant dataset from CUA BIC


## Study specific variables to specify data folders and license files
bids_dir=/data/analysis/maureen/adak/data/bids_data			# bids data directory
output_dir=$bids_dir/derivatives/fmriprep_3mm				# fmriprep output directory
log_dir=$bids_dir/derivatives/logs							# directory to save log file 
mriqc_version=22.0.6										# mriqc version to run
nprocs=10 													# run with 10 cores
mem=10000													# run with 10GB memory
work_dir=$HOME/work 										# working directory


date
now=`date +"%Y%m%d%H%M%S"` 


## Process command line arguments
usage(){ echo "Usage: `basename $0` -p <participant_id> 
p:	bids ID for participant


Example: `basename $0` -p sub-235 
" 1>&2; exit 1; }

if [ $# -ne 2 ]; then
	usage
fi
	
while getopts "p:" opt; do
    case "${opt}" in
        p)
            participant_id=${OPTARG}
            ;;
        t)
            task_id=${OPTARG}
            ;;
        *)
            usage
            ;;
    esac
done
shift $((OPTIND-1))




## Example from readthedocs
docker run -it --rm \
	-v <bids_dir>:/data:ro \
	-v <output_dir>:/out nipreps/mriqc:${mriqc_version} \
	/data /out participant \
	--participant_label 001 002 003