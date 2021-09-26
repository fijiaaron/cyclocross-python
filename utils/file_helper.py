import os
import csv
import json

from utils import setup

def save_csv(obj:dict, filename:str, filepath=None, append_date=False):
	'''
	save dict to a csv file

	Arguments:
		obj - the dict to save as csv
		filename - the name of the file to save
		filepath - the directory to save -- default to current directory
		append_date - add date stamp to filename: filename_2021-01-31.csv
	'''

	log = setup.create_logger(__name__)

	if append_date:
		filename += "_" + setup.datestamp()

	if not filename.endswith(".csv"):
		filename += ".csv"

	if filepath:
		filename = os.path.join(filepath, filename)

	log.debug(f"saving CSV {filename}")

	with open(filename, mode="w") as csvfile:
		keys = obj[0].keys()
		csv_writer = csv.DictWriter(csvfile, keys)
		csv_writer.writeheader()
		csv_writer.writerows(obj)

	return filename
		

def save_json(obj, filename:str, filepath=None, append_date=False):
	'''
	save object to json file
	
	Arguments:
		obj - the object to convert to json and save
		filename - the name of the file to save
		filepath - the directory to save -- default to current directory
		append_date - add date stamp to filename: filename_2021-01-31.csv
	'''
	
	log = setup.create_logger(__name__)

	if append_date:
		filename += "_" + setup.datestamp()

	if not filename.endswith(".json"):
		filename += ".json"

	if filepath:
		filename = os.path.join(filepath, filename)

	log.debug(f"saving JSON {filename}")

	with open(filename, mode="w", encoding="utf8") as jsonfile:
		json.dump(obj, jsonfile, indent=4, ensure_ascii=False)

	return filename
