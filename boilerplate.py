""" 
Docstring: I hate when ex-java developers spam unnecessary boilerplate abstractions that do nothing 'just-in-case' so that the code is 'future-proof' and 'universal'.
Nevertheless, in each ML project I find myself surrounded by dozens of throwaway scripts that get really messy when shared over github/box/gdrive/devboxes/ec2 instances.
Please use it as your default starting python file.
"""
__author__ = "Filip Drapejkowski"
__version__ = "1.0.0"

import argparse

def main(args):
    if args.verbose > 0:
        print("Reading from ", args.input_path)
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="This script does nothing.")
    parser.add_argument("--input_path", help="Input txt file path with data about nothing.", default="input_file.txt")
    parser.add_argument("--output_path", help="Output file that can be loaded into oblivion.", default="output_file.json")
    parser.add_argument('--verbose', '-v', action='count', default=0)
    parser.add_argument("--version", action="version", version="%(prog)s " + __version__)
    args = parser.parse_args()
    main(args)
