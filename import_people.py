#!/usr/bin/env python
import sys
import sqlite3
from csv import DictReader

from models import db, Person 

def main(argv):
    db.connect()
    try:
        Person.drop_table()
    except sqlite3.OperationalError:
        pass
    Person.create_table()

    with open(argv[1]) as f:
        csv_file = DictReader(f)
        for line in csv_file:
            attrs = {
                'trac_id': float(line['TRAC Assigned Identifier for Individual'].strip()),
                'nationality': line['Nationality'].strip(),
                'gender': line['Gender'].strip(),
            }
            try:
                person = Person.select().where((Person.trac_id == attrs['trac_id']) & (Person.nationality == attrs['nationality'])).get()
            except Person.DoesNotExist:
                person = Person.create(**attrs)

if __name__ == "__main__":
    main(sys.argv)
