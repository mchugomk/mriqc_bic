#!/usr/bin/env python

import sys
import argparse
import os.path
import json
import pandas as pd

# This script reads in json file output from mriqc and converts it to csv format for import into redcap.
# Currently works for T1w and bold modalities.
# To use with new Redcap project, copy forms from Redcap project 'mriqc template'

def main(json_filename):
	try:
		json_file=open(json_filename, 'r')
	except IOError as ex:
		print(ex)
	
	## Parse file name
	path, filename = os.path.split(json_filename)
	fileroot, fileext = os.path.splitext(filename)
	
	
	## Read json file and flatten
	data=json_file.read()
	json_data=json.loads(data)
	json_flat = pd.json_normalize(json_data)
	
	
	## Update json file for redcap
	
	# Change “.” to “_” in variable names
	json_flat.columns = json_flat.columns.str.replace('.','_')
	
	# Modify modality specific information
	if len(json_flat['bids_meta_modality']) == 1 and json_flat['bids_meta_modality'][0]=='T1w':
	
		# Structural: Prepend “structural_” to variable names
		json_flat = json_flat.add_prefix('structural_', 'columns')
	
		# Set bids_subject_id to bids_meta.subject_id and bids_session_id to bids_meta.session_id
		json_flat['bids_subject_id'] = json_flat['structural_bids_meta_subject_id']
		json_flat.rename(columns={'structural_bids_meta_Modality': 'structural_bids_meta_modalitytype'}, inplace=True)
		
		# Set filename
		json_flat['structural_filename']=filename
		
		# Set repeat instrument
		json_flat['redcap_repeat_instrument'] = 'mriqc_structural_iqm'
		
	elif len(json_flat['bids_meta_modality']) == 1 and json_flat['bids_meta_modality'][0]=='bold':
	
		# Functional: Prepend “functional_” to variable names
		json_flat = json_flat.add_prefix('functional_', 'columns')
	
		# Set bids_subject_id to bids_meta.subject_id and bids_session_id to bids_meta.session_id
		json_flat['bids_subject_id'] = json_flat['functional_bids_meta_subject_id']
		json_flat.rename(columns={'functional_bids_meta_Modality': 'functional_bids_meta_modalitytype'}, inplace=True)
	
		# Set filename
		json_flat['functional_filename']=filename
		
		# Set repeat instrument
		json_flat['redcap_repeat_instrument'] = 'mriqc_functional_iqm'
	
	
	# Add column for repeating instance of form
	json_flat['redcap_repeat_instance'] = 'new'
	
	# Move bids_subject_id to first position
	col = json_flat.pop("bids_subject_id")
	json_flat.insert(0, col.name, col)
	
	# Change all columns to lower case
	json_flat.columns = json_flat.columns.str.lower()
	
	
	## Save to csv with _redcap suffix
	print(os.path.join(path,fileroot+'.csv'))
	json_flat.to_csv(os.path.join(path,fileroot+'_redcap.csv'), index=False)
	json_file.close()		


if __name__ == '__main__':
	## Read input arguments
	parser = argparse.ArgumentParser(description='Prep json file from mriqc containing image quality metrics for redcap')
	parser.add_argument('--file', dest='json_file', type=str, help='Name of mriqc json file')
	
	if len(sys.argv) != 3:
		parser.print_help()
		parser.exit()
		
	args=parser.parse_args()
	
	main(args.json_file)


