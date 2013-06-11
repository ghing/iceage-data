#!/usr/bin/env python
import json
import sys
from datetime import datetime

from peewee import fn

from models import Transfer


def get_boundary_dates():
    earliest_date = datetime.strptime(Transfer.select().where((Transfer.from_facility >> None) | (Transfer.to_facility >> None)).aggregate(fn.Min(Transfer.date)), "%Y-%m-%d").date()
    latest_date = datetime.strptime(Transfer.select().where((Transfer.from_facility >> None) | (Transfer.to_facility >> None)).aggregate(fn.Max(Transfer.date)), "%Y-%m-%d").date()
    return (earliest_date, latest_date)

def sets_to_lists(data):
    new_data = data.copy()
    for datestr, date_data in data['detentions'].iteritems():
        new_data['detentions'][datestr]['facilities'] = list(date_data['facilities'])

    for datestr, date_data in data['deportations'].iteritems():
        new_data['deportations'][datestr]['facilities'] = list(date_data['facilities'])

    return new_data

def get_data():
    (start, end) = get_boundary_dates()
    data = {
        'start_date': start.isoformat(),
        'end_date': end.isoformat(),
        'detentions': {},
        'deportations': {},
    }
    detentions_to_date = 0
    deportations_to_date = 0
    for transfer in Transfer.select().where(
            (Transfer.from_facility >> None) | (Transfer.to_facility >> None)).order_by(Transfer.date):
        datestr = transfer.date.isoformat()
        if transfer.from_facility is None:
            if datestr not in data['detentions']:
                data['detentions'][datestr] = {
                    'facilities': set(),
                    'to_date': detentions_to_date,
                }
            detentions_to_date += 1
            data['detentions'][datestr]['facilities'].add(transfer.to_facility.get_id())
            data['detentions'][datestr]['to_date'] = detentions_to_date
        elif transfer.to_facility is None and transfer.reason == "Removed":
            if datestr not in data['deportations']:
                data['deportations'][datestr] = {
                    'facilities': set(),
                    'to_date': deportations_to_date,
                }
            deportations_to_date += 1
            data['deportations'][datestr]['facilities'].add(transfer.from_facility.get_id())
            data['deportations'][datestr]['to_date'] = deportations_to_date
        else:
            pass

    return sets_to_lists(data)

def main(argv):
    data = get_data()
    print json.dumps(data)

if __name__ == "__main__":
    main(sys.argv)
