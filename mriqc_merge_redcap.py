#!/usr/bin/env python

import sys
import argparse
import os.path
import pandas as pd
import glob

# This script merges all csv file output from mriqc_to_redcap.py found in <mriqc_path> for import into redcap.
# Currently works for T1w and bold modalities. 
# To use with new Redcap project, copy forms from Redcap project 'mriqc template'

def main(mriqc_path):

	if not os.path.isdir(mriqc_path):
		raise FileNotFoundError(f'Directory not found: {mriqc_path}')

	modality_list=['T1w', 'bold']
	
	for modality in modality_list:
		modality_pattern = 'sub-*' + modality + '*redcap.csv'
		mriqc_csv_outfile = 'mriqc_redcap_' + modality + '.csv'
		
		mriqc_csv = glob.glob(os.path.join(mriqc_path,'**/'+modality_pattern), recursive=True)		
		if any(mriqc_csv):
			mriqc_df = pd.concat([pd.read_csv(f, dtype='str') for f in mriqc_csv], ignore_index=True) # prevents 0-padded numbers from being converted
			mriqc_df.to_csv(os.path.join(mriqc_path, mriqc_csv_outfile), index=False)
		else:
			print(f'No files found matching: {modality_pattern}')


if __name__ == '__main__':

	## Read input arguments
	parser = argparse.ArgumentParser(description='Merge all redcap csv files from mriqc for T1w and bold data.')
	parser.add_argument('--mriqc_path', dest='mriqc_path', type=str, help='Name of directory containing mriqc output')
	
	if len(sys.argv) != 3:
		parser.print_help()
		parser.exit()
		
	args=parser.parse_args()

	main(args.mriqc_path)
	