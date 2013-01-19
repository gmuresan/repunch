from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from location.models import Zip, City
from punchcode.models import *
from retailer.models import Retailer

class Account(User):

    user = models.OneToOneField(User)

    phone = models.CharField(max_length=20, null=True, blank=True, verbose_name='Phone Number')
    zip = models.ForeignKey(Zip, null=True, blank=True)

    notifications = models.ManyToManyField('Notification', null=True, blank=True)

    user_types = (
        ('user','user'),
        ('retailer','retailer'),
        ('employee','employee')
    )

    type = models.CharField(choices=user_types, max_length=10)

    def __unicode__(self):
        return self.user.first_name + " " + self.user.last_name

    class Meta:
        abstract = True

class UserAccount(Account):
    facebook_uid = models.CharField(max_length=50, blank=True, null=True, db_index=True)
    access_token = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    token_expiration_date = models.DateTimeField(null=True, blank=True)
    age = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=6, choices=(('male','male'),('female','female')), blank=True, null=True)
    facebook_post_method = models.CharField(max_length=4, choices=(('auto', 'Automatic'), ('ask','Ask Every Time'), ('off', 'Off')))

    earned_rewards = models.ManyToManyField('punchcode.EarnedReward', blank=True)

    punches = models.ManyToManyField('punchcode.Punch', blank=True)
    pending_facebook_posts = models.ManyToManyField('PendingFacebookPost', blank=True)
    subscribed_retailers = models.ManyToManyField('retailer.Retailer', blank=True, related_name='users_subscribed')
    visited_retailers = models.ManyToManyField('retailer.Retailer', blank=True, related_name='users_visited')

    def __unicode__(self):
        return self.user.first_name + " " + self.user.last_name

class RetailerAccount(Account):

    retailer = models.ForeignKey(Retailer, related_name='retailer_accounts', null=True)

    logs = models.ManyToManyField('Log', null=True, blank=True)

    def __unicode__(self):
        return self.retailer.name


class Employee(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    username = models.CharField(max_length=30)

    retailer = models.ForeignKey(Retailer, related_name='employees')


class Notification(models.Model):
    text = models.CharField(max_length=250)
    date = models.DateTimeField(default=datetime.datetime.now)
    
    def __unicode__(self):
        return self.text

class Log(models.Model):
    employee = models.ForeignKey('Employee')
    date = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=20)
    code = models.ForeignKey(Code)

class UserUpdate(models.Model):

    class Meta:
        ordering = ['-date']
        get_latest_by = 'date'

    action_choices = (
        ('join', 'join'),
        ('punch', 'punch'),
        ('redeem', 'redeem'),
        ('earn', 'earn'),
        ('fb_punch', 'fb_punch')

    )

    user = models.ForeignKey('UserAccount', related_name='updates')
    date = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=10, choices=action_choices)
    retailer = models.ForeignKey('retailer.Retailer', null=True, blank=True)
    reward = models.ForeignKey('punchcode.Reward', null=True, blank=True)

    def __unicode__(self):
        if self.action == "punch":
            return "You were punched at " + self.retailer.name + " on " + self.date.strftime("%m-%d-%y")

        if self.action == "redeem":
            return "You redeemed a reward for a " + self.reward.text + " at " + self.retailer.name + " on " + self.date.strftime("%m-%d-%y")

        if self.action == 'earn':
            return "You earned a reward for a " + self.reward.text + " at " + self.retailer.name + " on " + self.date.strftime("%m-%d-%y")

        if self.action == 'join':
            return "You joined repunch on " + self.date.strftime("%m-%d-%y")

        if self.action == 'fb_punch':
            return "You received a free punch for posting your activity to Facebook on " + self.date.strftime("%m-%d-%y")


class PendingFacebookPost(models.Model):
    retailer = models.ForeignKey('retailer.Retailer')
    date = models.DateTimeField(auto_now=True)



