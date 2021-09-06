#!/usr/bin/env python 

def get_competitions(season):
    print(f"get competitions for {season} season")
    
def get_args():
    import argparse

    parser = argparse.ArgumentParser(description='Get Cyclocross competitions for season')
    parser.add_argument("-s", "--season", type=str, help="season (year) default is latest", default="latest")
    return parser.parse_args()

if __name__ == "__main__":
    args = get_args()
    print("args: ", args)

    get_competitions(args.season)
