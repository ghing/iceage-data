#!/usr/bin/env python
import sys
import json

from models import Facility

def flatten_connections(connections):
    flattened = []

    for facility_id, transfers_to in connections.iteritems():
        for transfer_facility_id in transfers_to.keys():
           flattened.append([facility_id, transfer_facility_id])

    return flattened
        

def get_connections():
    connections = {}
    for facility in Facility.select(): 
        for transfer in facility.transfers_from:
            if facility.get_id() not in connections:
                connections[facility.get_id()] = {}
            if transfer.to_facility is not None:
                connections[facility.get_id()][transfer.to_facility.get_id()] = True

    return connections

def main(argv):
    with open(argv[1], 'w') as f:
        connections = flatten_connections(get_connections())
        json.dump(connections, f)

if __name__ == "__main__":
    main(sys.argv)
