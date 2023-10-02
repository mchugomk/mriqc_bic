#!/bin/bash

## Run mriqc on bids-compliant dataset from BIC


## Variables to specify data folders 
mriqc_version=23.1.0		# mriqc version to run
nprocs=10 			# run with 10 cores
mem=10000			# run with 10GB memory
work_dir=$HOME/work 		# working directory


## Process command line arguments
usage(){ echo "Usage: `basename $0` -b <bids_dir> 
b:	directory with bids compliant data


Runs mriqc version ${mriqc_version} group analysis for participants in <bids_dir>
Temporary files will be stored in $HOME/work
Output will be placed in <bids_dir>/derivatives/mriqc

Example: `basename $0` -b /path/to/bids_data 
" 1>&2; exit 1; }

if [ $# -ne 2 ]; then
	usage
fi
	
while getopts "b:" opt; do
    case "${opt}" in
    	b)
    		bids_dir=${OPTARG}
    		;;
        *)
            usage
            ;;
    esac
done
shift $((OPTIND-1))

date
now=`date +"%Y%m%d%H%M%S"` 

## Variables to specify data folders 
output_dir=$bids_dir/derivatives/mriqc				# mriqc output directory
log_dir=$bids_dir/derivatives/logs					# directory to save log file 


## Save output from command line to log file
mriqc_logfile=$log_dir/mriqc_output_group_${now}.log

## Run mriqc-docker and save output to mriqc_logfile
date > $mriqc_logfile # Overwrite existing log file

## Run on T1 first 
echo "Running $0 for $bids_dir" 2>&1 | tee -a $mriqc_logfile
echo "docker run -it --rm \
-v ${bids_dir}:/data:ro \
-v ${output_dir}:/out \
-v ${work_dir}:/scratch \
nipreps/mriqc:${mriqc_version} \
/data /out group \
--nprocs $nprocs \
--mem $mem \
--no-sub \
-m T1w \
-w /scratch 2>&1 | tee -a $mriqc_logfile
" 2>&1 | tee -a $mriqc_logfile

docker run -it --rm \
	-v ${bids_dir}:/data:ro \
	-v ${output_dir}:/out \
	-v ${work_dir}:/scratch \
	nipreps/mriqc:${mriqc_version} \
		/data /out group \
		--nprocs $nprocs \
		--mem $mem \
		--no-sub \
		-m T1w  \
		-w /scratch 2>&1 | tee -a $mriqc_logfile
		
## Run on bold data 
echo "Running $0 for $bids_dir" 2>&1 | tee -a $mriqc_logfile
echo "docker run -it --rm \
-v ${bids_dir}:/data:ro \
-v ${output_dir}:/out \
-v ${work_dir}:/scratch \
nipreps/mriqc:${mriqc_version} \
/data /out group \
--nprocs $nprocs \
--mem $mem \
--no-sub \
-m bold \
-w /scratch 2>&1 | tee -a $mriqc_logfile
" 2>&1 | tee -a $mriqc_logfile

docker run -it --rm \
	-v ${bids_dir}:/data:ro \
	-v ${output_dir}:/out \
	-v ${work_dir}:/scratch \
	nipreps/mriqc:${mriqc_version} \
		/data /out group \
		--nprocs $nprocs \
		--mem $mem \
		--no-sub \
		-m bold  \
		-w /scratch 2>&1 | tee -a $mriqc_logfile

date >> $mriqc_logfile	

date
