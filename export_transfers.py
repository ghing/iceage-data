#!/usr/bin/env python
from datetime import datetime, timedelta
import sys
import json

from peewee import fn
from models import Facility, Transfer

def flatten_connections(connections):
    flattened = []

    for facility_id, transfers_to in connections.iteritems():
        for transfer_facility_id in transfers_to.keys():
           flattened.append([facility_id, transfer_facility_id])

    return flattened


def get_boundary_dates():
    earliest_date = datetime.strptime(Transfer.select().aggregate(fn.Min(Transfer.date)), "%Y-%m-%d").date()
    latest_date = datetime.strptime(Transfer.select().aggregate(fn.Max(Transfer.date)), "%Y-%m-%d").date()
    return (earliest_date, latest_date)


def get_transfers_for_date(date):
    transfers = []

    for facility in Facility.select():
        for transfer in Transfer.select().where(
                (Transfer.date == date) & (Transfer.from_facility == facility)):
            if transfer.to_facility is not None:
                transfers.append([facility.get_id(), transfer.to_facility.get_id()])

    return transfers
        

def get_transfers():
    (start, end) = get_boundary_dates()
    transfers = {
      'start_date': start.isoformat(),
      'end_date': end.isoformat(),
      'transfers': {}
    }
    current = start
    while current <= end:
        current += timedelta(days=1)
        todays_transfers = get_transfers_for_date(current)
        if len(todays_transfers):
            transfers['transfers'][current.isoformat()] = todays_transfers

    return transfers

def main(argv):
    transfers = get_transfers()
    print json.dumps(transfers)

if __name__ == "__main__":
    main(sys.argv)
