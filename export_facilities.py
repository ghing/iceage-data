#!/usr/bin/env python
import sys
import json

from models import Facility

def export_facilities(filename):
    with open(filename, 'w') as f:
        data = []
        for facility in Facility.select().dicts():
            data.append(facility)
        json.dump(data, f)

def main(argv):
    export_facilities(argv[1])

if __name__ == "__main__":
    main(sys.argv)
