# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Retailer.phone'
        db.add_column('retailer_retailer', 'phone', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Retailer.phone'
        db.delete_column('retailer_retailer', 'phone')


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
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
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
