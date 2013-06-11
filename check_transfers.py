#!/usr/bin/env python
from models import Person, Transfer

def check_transfers_per_person():
    for p in Person.select():
        # Each person should have only one incoming and one outgoing transfer
        in_transfers = p.transfers.where(Transfer.from_facility >> None)
        out_transfers = p.transfers.where(Transfer.to_facility >> None)
        if in_transfers.count() > 1:
            print "More than one incoming transfer for person %d" % (p.trac_id)
            print list(in_transfers)

        if out_transfers.count() > 1:
            print "More than one outgoing transfer for person %d" % (p.trac_id)
            print list(out_transfers)

def check_total_transfers():
    num_people = Person.select().count()
    total_incoming = Transfer.select().where(Transfer.from_facility >> None).count()
    total_outgoing = Transfer.select().where(Transfer.to_facility >> None).count()
    if total_incoming == num_people and total_outgoing == num_people:
        print "Looks good"
        return True

    if total_incoming != num_people:
        print "Incoming transfers don't match: %d != %d" % (total_incoming, num_people)

    if total_outgoing != num_people:
        print "Outgoing transfers don't match: %d != %d" % (total_outgoing, num_people)

    return False

def main():
    if not check_total_transfers():
        check_transfers_per_person()

if __name__ == "__main__":
    main()
