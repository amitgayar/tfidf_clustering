import json
from collections import namedtuple
from pprint import pprint
import os


def convert(d):
    # dict -> namedtuple
    return namedtuple('GenericDict', d.keys())(**d)

file = os.path.join(os.path.dirname(__file__),'conf.json')
with open(file) as data_file:
    data = json.load(data_file)
    # pprint(data)
    data = convert(data)
