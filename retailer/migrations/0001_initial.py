# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Retailer'
        db.create_table('retailer_retailer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('hours', self.gf('django.db.models.fields.TextField')(max_length=100)),
            ('category', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('zip', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['location.Zip'])),
            ('city', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['location.City'])),
            ('lat', self.gf('django.db.models.fields.FloatField')()),
            ('lng', self.gf('django.db.models.fields.FloatField')()),
            ('point', self.gf('django.contrib.gis.db.models.fields.PointField')()),
            ('max_level', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('registration_code', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['retailer.RegistrationCode'], unique=True, null=True, blank=True)),
            ('admin_password', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal('retailer', ['Retailer'])

        # Adding model 'NewRetailerContact'
        db.create_table('retailer_newretailercontact', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('company_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('zip', self.gf('django.db.models.fields.IntegerField')()),
            ('person_to_contact', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('best_time', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('retailer', ['NewRetailerContact'])

        # Adding model 'RetailerUpdate'
        db.create_table('retailer_retailerupdate', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('retailer', self.gf('django.db.models.fields.related.ForeignKey')(related_name='updates', to=orm['retailer.Retailer'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('action', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal('retailer', ['RetailerUpdate'])

        # Adding model 'RegistrationCode'
        db.create_table('retailer_registrationcode', (
            ('code', self.gf('django.db.models.fields.CharField')(max_length=50, primary_key=True)),
        ))
        db.send_create_signal('retailer', ['RegistrationCode'])


    def backwards(self, orm):
        
        # Deleting model 'Retailer'
        db.delete_table('retailer_retailer')

        # Deleting model 'NewRetailerContact'
        db.delete_table('retailer_newretailercontact')

        # Deleting model 'RetailerUpdate'
        db.delete_table('retailer_retailerupdate')

        # Deleting model 'RegistrationCode'
        db.delete_table('retailer_registrationcode')


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
            'point': ('django.contrib.gis.db.models.fields.PointField', [], {})
        },
        'retailer.newretailercontact': {
            'Meta': {'object_name': 'NewRetailerContact'},
            'best_time': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'company_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person_to_contact': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'zip': ('django.db.models.fields.IntegerField', [], {})
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
            'point': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'registration_code': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['retailer.RegistrationCode']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'zip': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['location.Zip']"})
        },
        'retailer.retailerupdate': {
            'Meta': {'ordering': "['-date']", 'object_name': 'RetailerUpdate'},
            'action': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'retailer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'updates'", 'to': "orm['retailer.Retailer']"})
        }
    }

    complete_apps = ['retailer']
