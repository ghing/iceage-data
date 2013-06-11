#!/usr/bin/env python
import json

from models import MEN, WOMEN, CHARACTER_IDS, Person

def get_characters():
    characters = []
    for trac_id in CHARACTER_IDS:
        person = Person.select().where(Person.trac_id == trac_id).get()
        if trac_id in MEN:
            gender = 'male'
        else:
            gender = 'female'
        characters.append({
            'trac_id': person.trac_id,
            'gender': gender,
            'nationality': person.nationality.strip().lower()
        })

    return characters

def main():
    data = get_characters()
    print json.dumps(data)

if __name__ == "__main__":
    main()    
