# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Zip'
        db.create_table('location_zip', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.IntegerField')(unique=True, db_index=True)),
            ('lat', self.gf('django.db.models.fields.FloatField')()),
            ('lng', self.gf('django.db.models.fields.FloatField')()),
            ('point', self.gf('django.contrib.gis.db.models.fields.PointField')()),
        ))
        db.send_create_signal('location', ['Zip'])

        # Adding model 'State'
        db.create_table('location_state', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('short', self.gf('django.db.models.fields.CharField')(max_length=2)),
        ))
        db.send_create_signal('location', ['State'])

        # Adding model 'City'
        db.create_table('location_city', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('state', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['location.State'], null=True, blank=True)),
        ))
        db.send_create_signal('location', ['City'])

        # Adding M2M table for field zip on 'City'
        db.create_table('location_city_zip', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('city', models.ForeignKey(orm['location.city'], null=False)),
            ('zip', models.ForeignKey(orm['location.zip'], null=False))
        ))
        db.create_unique('location_city_zip', ['city_id', 'zip_id'])


    def backwards(self, orm):
        
        # Deleting model 'Zip'
        db.delete_table('location_zip')

        # Deleting model 'State'
        db.delete_table('location_state')

        # Deleting model 'City'
        db.delete_table('location_city')

        # Removing M2M table for field zip on 'City'
        db.delete_table('location_city_zip')


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
            'code': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.FloatField', [], {}),
            'lng': ('django.db.models.fields.FloatField', [], {}),
            'point': ('django.contrib.gis.db.models.fields.PointField', [], {})
        }
    }

    complete_apps = ['location']
