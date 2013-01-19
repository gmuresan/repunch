from django.conf import Settings
from django.utils.datetime_safe import strftime
from location.models import *
import settings
from tools import geocode, build_address
from django.contrib.gis.db import models


def get_path(instance, filename):
    if settings.DEBUG:
        return 'media/local/retailer/' + str(instance.id) + '/' + filename
    else:
        return 'media/retailer/' + str(instance.id) + '/' + filename

class Retailer(models.Model):

    # REVERSE KEYS: employees, rewards
    
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    hours = models.TextField(max_length=100)
    category = models.CharField(max_length=25)
    phone = models.CharField(max_length=20, null=True, blank=True, verbose_name='Phone number')
    address = models.CharField(max_length=100)

    main_image = models.ImageField(upload_to=get_path, default='retailer/0/default.png')
    
    zip = models.ForeignKey(Zip)
    city = models.ForeignKey(City)

    lat = models.FloatField()
    lng = models.FloatField()
    point = models.PointField(geography=True)
    objects = models.GeoManager()

    registration_code = models.OneToOneField('RegistrationCode', null=True, blank=True)

    admin_password = models.CharField(max_length=30)
    max_level = models.IntegerField(default=0)
    num_facebook_posts = models.IntegerField(default=0)
    
    def save(self, *args, **kwargs):
        address = build_address(self.address, self.zip.code)
        location = geocode(address)
        if location:
            self.lat = location['lat']
            self.lng = location['lng']
            self.point = Point(float(self.lng), float(self.lat))

        super(Retailer,self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

class NewRetailerContact(models.Model):
    company_name = models.CharField(max_length=50)
    zip = models.IntegerField(verbose_name='Zip Code')
    person_to_contact = models.CharField(max_length=25)
    email = models.EmailField(verbose_name='E-mail Address')
    phone = models.CharField(verbose_name='Phone Number', max_length=20)
    best_time = models.CharField(verbose_name='Best time to be reached', max_length=30)

    date = models.DateTimeField()

class RetailerUpdate(models.Model):

    class Meta:
        ordering = ['-date']

    action_choices = (
        ('join', 'join'),
        ('bonus', 'bonus'),
    )

    retailer = models.ForeignKey('Retailer', related_name='updates')
    date = models.DateTimeField(auto_now_add=True, db_index=True)
    action = models.CharField(max_length=10, choices=action_choices)

    def __unicode__(self):
        if self.action == 'join':
            return self.retailer.name + " joined the re:punch network on " + strftime(self.date, "%m-%d-%y")

        if self.action == 'bonus':
            return self.retailer.name + " is offering (blank) for (blank) punches on (blank)"

class RegistrationCode(models.Model):
    code = models.CharField(max_length=50, primary_key=True)