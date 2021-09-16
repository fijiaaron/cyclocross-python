#!/usr/bin/env python

import argparse

import setup
from uci.cyclocross.results import CyclocrossResultsFrame

def get_competitions(season):
	log = setup.create_logger()
	driver = setup.get_chromedriver()

	print(f"get competitions for {season} season")



def get_args():

	parser = argparse.ArgumentParser(description='Get Cyclocross competitions for season')
	parser.add_argument("-s", "--season", type=str, help="season (year) default is latest", default="latest")
	return parser.parse_args()

if __name__ == "__main__":
	args = get_args()
	print("args: ", args)

	get_competitions(args.season)
