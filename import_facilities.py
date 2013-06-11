#!/usr/bin/env python
import sys
import sqlite3
from csv import DictReader

from models import db, Facility

def main(argv):
    db.connect()
    try:
        Facility.drop_table()
    except sqlite3.OperationalError:
        pass
    Facility.create_table()

    with open(argv[1]) as f:
        csv_file = DictReader(f)
        for line in csv_file:
            attrs = {
                'name': line['name'].strip(),
                'official_name': line['official_name'].strip(),
                'url': line['url'].strip(),
            }
            if len(line['geo_latitude']):
                attrs['latitude'] = float(line['geo_latitude'].strip())
            if len(line['geo_longitude']):
                attrs['longitude'] = float(line['geo_longitude'].strip())
            Facility.create(**attrs)

if __name__ == "__main__":
    main(sys.argv)
