#!/usr/bin/env python

import json
from pprint import pprint


def read_json(filename):
    with open(filename) as f:
        return json.load(f)


def main():
    data = read_json(insomnia_data.json)
    pprint(data)


if __name__ == "__main__":
    main()


