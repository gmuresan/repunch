# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Code'
        db.create_table('punchcode_code', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
            ('retailer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['retailer.Retailer'])),
            ('used', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('punchcode', ['Code'])

        # Adding model 'Punch'
        db.create_table('punchcode_punch', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('retailer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['retailer.Retailer'])),
        ))
        db.send_create_signal('punchcode', ['Punch'])

        # Adding model 'Reward'
        db.create_table('punchcode_reward', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('punches', self.gf('django.db.models.fields.IntegerField')()),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('shareable', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('retailer', self.gf('django.db.models.fields.related.ForeignKey')(related_name='rewards', to=orm['retailer.Retailer'])),
        ))
        db.send_create_signal('punchcode', ['Reward'])

        # Adding model 'EarnedReward'
        db.create_table('punchcode_earnedreward', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('reward', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['punchcode.Reward'])),
            ('redeemed', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('punchcode', ['EarnedReward'])

    def backwards(self, orm):
        # Deleting model 'Code'
        db.delete_table('punchcode_code')

        # Deleting model 'Punch'
        db.delete_table('punchcode_punch')

        # Deleting model 'Reward'
        db.delete_table('punchcode_reward')

        # Deleting model 'EarnedReward'
        db.delete_table('punchcode_earnedreward')

    models = {
        'location.city': {
            'Meta': {'object_name': 'City'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['location.State']", 'null': 'True', 'blank': 'True'}),
            'zip': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['location.Zip']", 'symmetrical': 'False'})
        },
        'location.state': {
            'Meta': {'object_name': 'State'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'short': ('django.db.models.fields.CharField', [], {'max_length': '2'})
        },
        'location.zip': {
            'Meta': {'object_name': 'Zip'},
            'code': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.FloatField', [], {}),
            'lng': ('django.db.models.fields.FloatField', [], {}),
            'point': ('django.contrib.gis.db.models.fields.PointField', [], {'geography': 'True'})
        },
        'punchcode.code': {
            'Meta': {'object_name': 'Code'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'retailer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['retailer.Retailer']"}),
            'used': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'punchcode.earnedreward': {
            'Meta': {'object_name': 'EarnedReward'},
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'redeemed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'reward': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['punchcode.Reward']"})
        },
        'punchcode.punch': {
            'Meta': {'object_name': 'Punch'},
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'retailer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['retailer.Retailer']"})
        },
        'punchcode.reward': {
            'Meta': {'object_name': 'Reward'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'punches': ('django.db.models.fields.IntegerField', [], {}),
            'retailer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'rewards'", 'to': "orm['retailer.Retailer']"}),
            'shareable': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'retailer.registrationcode': {
            'Meta': {'object_name': 'RegistrationCode'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '50', 'primary_key': 'True'})
        },
        'retailer.retailer': {
            'Meta': {'object_name': 'Retailer'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'admin_password': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'category': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['location.City']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'hours': ('django.db.models.fields.TextField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.FloatField', [], {}),
            'lng': ('django.db.models.fields.FloatField', [], {}),
            'max_level': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'point': ('django.contrib.gis.db.models.fields.PointField', [], {'geography': 'True'}),
            'registration_code': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['retailer.RegistrationCode']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'updates': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'retailer'", 'blank': 'True', 'to': "orm['retailer.RetailerUpdate']"}),
            'zip': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['location.Zip']"})
        },
        'retailer.retailerupdate': {
            'Meta': {'ordering': "['-date']", 'object_name': 'RetailerUpdate'},
            'action': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['punchcode']