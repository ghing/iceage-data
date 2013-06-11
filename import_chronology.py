#!/usr/bin/env python
import sys
import sqlite3
from datetime import datetime
from csv import DictReader

from models import db, Facility, Detention, Person

def main(argv):
    db.connect()
    try:
        Detention.drop_table()
    except sqlite3.OperationalError:
        pass
    Detention.create_table()

    with open(argv[1]) as f:
        date_format = '%d-%b-%y'
        csv_file = DictReader(f)
        for line in csv_file:
            person = Person.select().where(Person.trac_id == line['TRAC Assigned Identifier for Individual'].strip()).get()
            facility = Facility.select().where(Facility.name == line['Detention Facility'].strip()).get()
            attrs = {
                'person': person,
                'facility': facility,
                'book_in_date': datetime.strptime(line['Book-In Date'].strip(), date_format).date(),
                'book_out_date': datetime.strptime(line['Book-Out Date'].strip(), date_format).date(),
                'book_out_reason': line['Reason for Book-Out'].strip(),
            }
            Detention.create(**attrs)


if __name__ == "__main__":
    main(sys.argv)
