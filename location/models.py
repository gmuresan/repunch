import pdb
from django.contrib.gis.geos.point import Point
from django.db import models
from django.contrib.gis.db import models
from tools import build_address, geocode

class Zip(models.Model):
    code = models.IntegerField(unique=True, db_index=True)
    objects = models.GeoManager()
    lat = models.FloatField()
    lng = models.FloatField()
    point = models.PointField(geography=True)

    def save(self, *args, **kwargs):
        address = self.code
        location = geocode(address)
        self.lat = location['lat']
        self.lng = location['lng']
        self.point = Point(float(self.lng), float(self.lat))
        super(Zip, self).save(*args, **kwargs)

    
    def __unicode__(self):
        return str(self.code)


class State(models.Model):
    name = models.CharField(max_length=50)
    short = models.CharField(max_length=2)

    def __unicode__(self):
        return self.name


class CityManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)

class City(models.Model):
    objects = CityManager()

    name = models.CharField(max_length=50)
    state = models.ForeignKey(State, null=True, blank=True)
    zip = models.ManyToManyField(Zip)

    def save(self, *args, **kwargs):
        super(City,self).save()
        if self.state is None and self.zip.count() > 0:
            address = build_address(str(self.name), str(self.zip.all()[0].code))
            location = geocode(address)
            state, created = State.objects.get_or_create(name=location['state'], short=location['state_short'])
            self.state = state
        super(City,self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

    
