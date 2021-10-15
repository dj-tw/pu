"""
Data from here
https://www.census.gov/programs-surveys/sipp/data/datasets/2019-data/2019.html
"""

from csv import DictReader
import json


def read():
    filename = 'data/pu2019.csv'
    return (dict(row) for row in DictReader(open(filename, 'r'), delimiter='|'))


def read_schema():
    filename = 'data/pu2019_schema.json'
    return json.load(open(filename, 'r'))
