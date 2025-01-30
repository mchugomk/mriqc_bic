#!/usr/bin/env python

import sys
import argparse
import os.path
import json
import pandas as pd

# This script reads in json file output from mriqc and converts it to csv format.

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
	
	
	## Save to csv
	json_flat['filename']=filename
	print(os.path.join(path,fileroot+'.csv'))
	json_flat.to_csv(os.path.join(path,fileroot+'.csv'), index=False)
	json_file.close()


if __name__ == '__main__':

	## Read input arguments
	parser = argparse.ArgumentParser(description='Read in json file from mriqc containing image quality metrics and save as csv.')
	parser.add_argument('--file', dest='json_file', type=str, help='Name of mriqc json file')
	
	if len(sys.argv) != 3:
		parser.print_help()
		parser.exit()
		
	args=parser.parse_args()

	main(args.json_file)
