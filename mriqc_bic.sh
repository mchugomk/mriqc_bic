#!/bin/bash

## Run mriqc on bids-compliant dataset from BIC


## Variables to specify data folders 
mriqc_version=22.0.6										# mriqc version to run
nprocs=10 													# run with 10 cores
mem=10000													# run with 10GB memory
work_dir=$HOME/work 										# working directory

date
now=`date +"%Y%m%d%H%M%S"` 


## Process command line arguments
usage(){ echo "Usage: `basename $0` -b <bids_dir> -p <participant_id> -s <session_id>
b:	directory with bids compliant data
p:	bids ID for participant
s:	session ID for participant data

Runs mriqc for <participant_id> and <session_id> in <bids_dir>
Output will be placed in <bids_dir>/derivatives/mriqc

Example: `basename $0` -b /path/to/bids_data -p sub-001 -s ses-01
" 1>&2; exit 1; }

if [ $# -ne 6 ]; then
	usage
fi
	
while getopts "b:p:s:" opt; do
    case "${opt}" in
    	b)
    		bids_dir=${OPTARG}
    		;;
        p)
            participant_id=${OPTARG}
            ;;
        s)
        	session_id=${OPTARG}
        	;;
        *)
            usage
            ;;
    esac
done
shift $((OPTIND-1))

## Variables to specify data folders 
# bids_dir=/data/analysis/maureen/rto/data/bids_data		# bids data directory
output_dir=$bids_dir/derivatives/mriqc						# mriqc output directory
log_dir=$bids_dir/derivatives/logs							# directory to save log file 


## Save output from command line to log file
mriqc_logfile=$log_dir/mriqc_output_${participant_id}_${session_id}_${now}.log

## Run mriqc-docker and save output to mriqc_logfile
date > $mriqc_logfile # Overwrite existing log file

echo "Running $0 for $participant_id $session_id" >> $mriqc_logfile
echo "docker run -it --rm \
-v ${bids_dir}:/data:ro \
-v ${output_dir}:/out nipreps/mriqc:${mriqc_version} \
-v ${work_dir}:/scratch \
/data /out participant \
--participant_label $participant_id \
--session_id $session_id \
--nprocs $nprocs \
--mem $mem \
-w /scratch 2>&1 | tee -a $fmriprep_logfile
" >> $mriqc_logfile
	
docker run -it --rm \
	-v ${bids_dir}:/data:ro \
	-v ${output_dir}:/out nipreps/mriqc:${mriqc_version} \
	-v ${work_dir}:/scratch \
	/data /out participant \
	--participant_label $participant_id \
	--session_id $session_id \
	--nprocs $nprocs \
	--mem $mem \
	-w /scratch 2>&1 | tee -a $fmriprep_logfile

date >> $mriqc_logfile	

date