#!/usr/bin/env python
import sqlite3
import sys

from peewee import prefetch
from models import db, Detention, Person, Transfer

def main(argv):
    db.connect()
    try:
        Transfer.drop_table()
    except sqlite3.OperationalError:
        pass
    Transfer.create_table()

    processed = 0
    people = Person.select()
    detentions = Detention.select().order_by(Detention.book_in_date)
    people_prefetch = prefetch(people, detentions)
    #people = Person.select().where(Person.trac_id == 16450)
    total = float(people.count())

    for person in people_prefetch:
        processed = processed + 1
        percent_complete = (processed / total) * 100
        print "Building transfers for %d (%d %%)" % (person.trac_id, percent_complete)
        previous_facility = None
        previous_detention = None

        detentions = person.detentions_prefetch

        for detention in detentions:
            if previous_detention is not None:
                reason = previous_detention.book_out_reason
            else:
                reason = ''
            Transfer.create(
                person=person,
                from_facility=previous_facility,
                to_facility=detention.facility,
                date=detention.book_in_date,
                reason=reason)
            previous_facility = detention.facility
            previous_detention = detention

        # Create outgoing transfer
        Transfer.create(
                person=person,
                from_facility=previous_facility,
                to_facility=None,
                date=previous_detention.book_out_date,
                reason=previous_detention.book_out_reason)

if __name__ == "__main__":
    main(sys.argv)
