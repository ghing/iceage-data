from peewee import CharField, DateField, FloatField, ForeignKeyField, IntegerField, Model, SqliteDatabase

CHARACTER_IDS = [
    41407,
    114485,
    19436,
    17126,
    34512,
    149487,
    20756,
    103041,
]

MEN = [
    19436,
    17126,
    103041, 
]

WOMEN = [
    41407,
    114485,
    34512,
    149487,
    20756,
]

db = SqliteDatabase('ice_detentions.db')

class Person(Model):
    trac_id = IntegerField(primary_key=True)
    nationality = CharField(null=True)
    gender = CharField(null=True)

    class Meta:
        database = db

class Facility(Model):
    name = CharField()
    official_name = CharField()
    url = CharField()
    longitude = FloatField(null=True)
    latitude = FloatField(null=True)

    class Meta:
        database = db

class Detention(Model):
    person = ForeignKeyField(Person, related_name="detentions")
    facility = ForeignKeyField(Facility, related_name="detentions")
    book_in_date = DateField()
    book_out_date = DateField()
    book_out_reason = CharField()

    class Meta:
        database = db

class Transfer(Model):
    person = ForeignKeyField(Person, related_name="transfers")
    from_facility = ForeignKeyField(Facility, related_name="transfers_from", null=True)
    to_facility = ForeignKeyField(Facility, related_name="transfers_to", null=True)
    date = DateField()
    reason = CharField()

    class Meta:
        database = db

    def __unicode__(self):
        from_name = self.from_facility.name if self.from_facility else None
        to_name = self.to_facility.name if self.to_facility else None
        if from_name and to_name:
            str_rep = "from %s to %s" % (from_name, to_name)
        elif to_name:
            str_rep = "to %s" % (to_name)
        else:
            # from_name
            str_rep = "from %s" % (from_name)

        return "%d %s on %s (%s)" % (self.person.trac_id, str_rep, self.date, self.reason)
