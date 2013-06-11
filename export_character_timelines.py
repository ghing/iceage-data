#!/usr/bin/env python
import json

from models import CHARACTER_IDS, Transfer, Person

def get_timelines():
    timelines = {}
    for person in Person.select().where(Person.trac_id << CHARACTER_IDS):
        for transfer in person.transfers:
            transfer_date = transfer.date.isoformat()
            if transfer_date not in timelines:
                timelines[transfer_date] = {}
            reason = transfer.reason.strip()
            if transfer.from_facility is None:
                # Work around some facilities not having "Official Names"
                facility_name = transfer.to_facility.official_name or transfer.to_facility.name
                message = "Detained and sent to %s" % (facility_name)
            elif reason == "Transferred":
                message = "Transferred to %s" % (transfer.to_facility.official_name)
            elif transfer.reason == "Removed":
                message = "Deported"
            else:
                message = "Left ICE custody (%s)" % (reason)
            timelines[transfer_date][person.trac_id] = message
    return timelines

def main():
    timelines = get_timelines()
    print json.dumps(timelines)

if __name__ == "__main__":
    main()    
