import datetime
from django.contrib.auth.models import User
from django.db import models

class Code(models.Model):
    code = models.CharField(max_length=30, unique=True)
    retailer = models.ForeignKey('retailer.Retailer')
    used = models.BooleanField(default=False)

    def __unicode__(self):
        return self.code

class Punch(models.Model):
    date = models.DateTimeField(default=datetime.datetime.now)
    retailer = models.ForeignKey('retailer.Retailer')

class Reward(models.Model):
    punches = models.IntegerField()
    text = models.CharField(max_length=50)
    active = models.BooleanField(default=True)
    shareable = models.BooleanField(default=True)
    retailer = models.ForeignKey('retailer.Retailer', related_name='rewards')

class EarnedReward(models.Model):
    date = models.DateTimeField(default=datetime.datetime.now)
    reward = models.ForeignKey(Reward)
    redeemed = models.BooleanField(default=False)

    
    






