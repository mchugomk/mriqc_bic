#!/usr/bin/env python

import sys
import argparse
import os.path
import pandas as pd
import glob
import mriqc_to_redcap

# Run mriqc_to_redcap on a list of subjects and sessions specified in csv file

def main(mriqc_path, csv_filename):

	if not os.path.isdir(mriqc_path):
		raise FileNotFoundError(f'Directory not found: {mriqc_path}')

	try:
		mriqc_df = pd.read_csv(csv_filename)
	except IOError as ex:
		print(ex)
	
	for index, row in mriqc_df.iterrows():
		subject_id = row['subject_id']
		session_id = row['session_id']
		mriqc_json = glob.glob(os.path.join(mriqc_path, subject_id, session_id, '**/*.json'), recursive=True)		
		for json_file in mriqc_json:
			mriqc_to_redcap.main(json_file)


if __name__ == '__main__':

	## Read input arguments
	parser = argparse.ArgumentParser(description='Convert mriqc json file output to csv files for upload to redcap')
	parser.add_argument('--mriqc_path', dest='mriqc_path', type=str, help='Name of directory containing mriqc output')
	parser.add_argument('--csv_filename', dest='csv_filename', type=str, help='Path to csv file containing list of BIDS subject and session IDs to be converted to redcap csv format')
	
	if len(sys.argv) != 5:
		parser.print_help()
		parser.exit()
		
	args=parser.parse_args()
	
	main(args.mriqc_path, args.csv_filename)

	