#!env/bin/python

import sklearn
import json
from pprint import pprint


def read_json():
    with open("insomnia_data.json") as f:
        return json.load(f)




def main():
    data = read_json()
    pprint(data)



if __name__ == "__main__":
    main()


