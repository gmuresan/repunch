# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'UserAccount'
        db.create_table('account_useraccount', (
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, primary_key=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('zip', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['location.Zip'], null=True, blank=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('facebook_uid', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=50, null=True, blank=True)),
            ('access_token', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=255, null=True, blank=True)),
            ('token_expiration_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('age', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=6, null=True, blank=True)),
            ('facebook_post_method', self.gf('django.db.models.fields.CharField')(max_length=4)),
        ))
        db.send_create_signal('account', ['UserAccount'])

        # Adding M2M table for field notifications on 'UserAccount'
        db.create_table('account_useraccount_notifications', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('useraccount', models.ForeignKey(orm['account.useraccount'], null=False)),
            ('notification', models.ForeignKey(orm['account.notification'], null=False))
        ))
        db.create_unique('account_useraccount_notifications', ['useraccount_id', 'notification_id'])

        # Adding M2M table for field earned_rewards on 'UserAccount'
        db.create_table('account_useraccount_earned_rewards', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('useraccount', models.ForeignKey(orm['account.useraccount'], null=False)),
            ('earnedreward', models.ForeignKey(orm['punchcode.earnedreward'], null=False))
        ))
        db.create_unique('account_useraccount_earned_rewards', ['useraccount_id', 'earnedreward_id'])

        # Adding M2M table for field punches on 'UserAccount'
        db.create_table('account_useraccount_punches', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('useraccount', models.ForeignKey(orm['account.useraccount'], null=False)),
            ('punch', models.ForeignKey(orm['punchcode.punch'], null=False))
        ))
        db.create_unique('account_useraccount_punches', ['useraccount_id', 'punch_id'])

        # Adding M2M table for field pending_facebook_posts on 'UserAccount'
        db.create_table('account_useraccount_pending_facebook_posts', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('useraccount', models.ForeignKey(orm['account.useraccount'], null=False)),
            ('pendingfacebookpost', models.ForeignKey(orm['account.pendingfacebookpost'], null=False))
        ))
        db.create_unique('account_useraccount_pending_facebook_posts', ['useraccount_id', 'pendingfacebookpost_id'])

        # Adding M2M table for field subscribed_retailers on 'UserAccount'
        db.create_table('account_useraccount_subscribed_retailers', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('useraccount', models.ForeignKey(orm['account.useraccount'], null=False)),
            ('retailer', models.ForeignKey(orm['retailer.retailer'], null=False))
        ))
        db.create_unique('account_useraccount_subscribed_retailers', ['useraccount_id', 'retailer_id'])

        # Adding M2M table for field visited_retailers on 'UserAccount'
        db.create_table('account_useraccount_visited_retailers', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('useraccount', models.ForeignKey(orm['account.useraccount'], null=False)),
            ('retailer', models.ForeignKey(orm['retailer.retailer'], null=False))
        ))
        db.create_unique('account_useraccount_visited_retailers', ['useraccount_id', 'retailer_id'])

        # Adding model 'RetailerAccount'
        db.create_table('account_retaileraccount', (
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, primary_key=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('zip', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['location.Zip'], null=True, blank=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('retailer', self.gf('django.db.models.fields.related.ForeignKey')(related_name='retailer_accounts', null=True, to=orm['retailer.Retailer'])),
        ))
        db.send_create_signal('account', ['RetailerAccount'])

        # Adding M2M table for field notifications on 'RetailerAccount'
        db.create_table('account_retaileraccount_notifications', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('retaileraccount', models.ForeignKey(orm['account.retaileraccount'], null=False)),
            ('notification', models.ForeignKey(orm['account.notification'], null=False))
        ))
        db.create_unique('account_retaileraccount_notifications', ['retaileraccount_id', 'notification_id'])

        # Adding M2M table for field logs on 'RetailerAccount'
        db.create_table('account_retaileraccount_logs', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('retaileraccount', models.ForeignKey(orm['account.retaileraccount'], null=False)),
            ('log', models.ForeignKey(orm['account.log'], null=False))
        ))
        db.create_unique('account_retaileraccount_logs', ['retaileraccount_id', 'log_id'])

        # Adding model 'Employee'
        db.create_table('account_employee', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('retailer', self.gf('django.db.models.fields.related.ForeignKey')(related_name='employees', to=orm['retailer.Retailer'])),
        ))
        db.send_create_signal('account', ['Employee'])

        # Adding model 'Notification'
        db.create_table('account_notification', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal('account', ['Notification'])

        # Adding model 'Log'
        db.create_table('account_log', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('employee', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['account.Employee'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('action', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('code', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['punchcode.Code'])),
        ))
        db.send_create_signal('account', ['Log'])

        # Adding model 'UserUpdate'
        db.create_table('account_userupdate', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='updates', to=orm['account.UserAccount'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('action', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('retailer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['retailer.Retailer'], null=True, blank=True)),
            ('reward', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['punchcode.Reward'], null=True, blank=True)),
        ))
        db.send_create_signal('account', ['UserUpdate'])

        # Adding model 'PendingFacebookPost'
        db.create_table('account_pendingfacebookpost', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('retailer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['retailer.Retailer'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('account', ['PendingFacebookPost'])


    def backwards(self, orm):
        
        # Deleting model 'UserAccount'
        db.delete_table('account_useraccount')

        # Removing M2M table for field notifications on 'UserAccount'
        db.delete_table('account_useraccount_notifications')

        # Removing M2M table for field earned_rewards on 'UserAccount'
        db.delete_table('account_useraccount_earned_rewards')

        # Removing M2M table for field punches on 'UserAccount'
        db.delete_table('account_useraccount_punches')

        # Removing M2M table for field pending_facebook_posts on 'UserAccount'
        db.delete_table('account_useraccount_pending_facebook_posts')

        # Removing M2M table for field subscribed_retailers on 'UserAccount'
        db.delete_table('account_useraccount_subscribed_retailers')

        # Removing M2M table for field visited_retailers on 'UserAccount'
        db.delete_table('account_useraccount_visited_retailers')

        # Deleting model 'RetailerAccount'
        db.delete_table('account_retaileraccount')

        # Removing M2M table for field notifications on 'RetailerAccount'
        db.delete_table('account_retaileraccount_notifications')

        # Removing M2M table for field logs on 'RetailerAccount'
        db.delete_table('account_retaileraccount_logs')

        # Deleting model 'Employee'
        db.delete_table('account_employee')

        # Deleting model 'Notification'
        db.delete_table('account_notification')

        # Deleting model 'Log'
        db.delete_table('account_log')

        # Deleting model 'UserUpdate'
        db.delete_table('account_userupdate')

        # Deleting model 'PendingFacebookPost'
        db.delete_table('account_pendingfacebookpost')


    models = {
        'account.employee': {
            'Meta': {'object_name': 'Employee'},
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'retailer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'employees'", 'to': "orm['retailer.Retailer']"}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'account.log': {
            'Meta': {'object_name': 'Log'},
            'action': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'code': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['punchcode.Code']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'employee': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['account.Employee']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'account.notification': {
            'Meta': {'object_name': 'Notification'},
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        'account.pendingfacebookpost': {
            'Meta': {'object_name': 'PendingFacebookPost'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'retailer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['retailer.Retailer']"})
        },
        'account.retaileraccount': {
            'Meta': {'object_name': 'RetailerAccount'},
            'logs': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['account.Log']", 'null': 'True', 'blank': 'True'}),
            'notifications': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['account.Notification']", 'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'retailer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'retailer_accounts'", 'null': 'True', 'to': "orm['retailer.Retailer']"}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'primary_key': 'True'}),
            'zip': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['location.Zip']", 'null': 'True', 'blank': 'True'})
        },
        'account.useraccount': {
            'Meta': {'object_name': 'UserAccount'},
            'access_token': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'age': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'earned_rewards': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['punchcode.EarnedReward']", 'symmetrical': 'False', 'blank': 'True'}),
            'facebook_post_method': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'facebook_uid': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '6', 'null': 'True', 'blank': 'True'}),
            'notifications': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['account.Notification']", 'null': 'True', 'blank': 'True'}),
            'pending_facebook_posts': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['account.PendingFacebookPost']", 'symmetrical': 'False', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'punches': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['punchcode.Punch']", 'symmetrical': 'False', 'blank': 'True'}),
            'subscribed_retailers': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'users_subscribed'", 'blank': 'True', 'to': "orm['retailer.Retailer']"}),
            'token_expiration_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'primary_key': 'True'}),
            'visited_retailers': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'users_visited'", 'blank': 'True', 'to': "orm['retailer.Retailer']"}),
            'zip': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['location.Zip']", 'null': 'True', 'blank': 'True'})
        },
        'account.userupdate': {
            'Meta': {'ordering': "['-date']", 'object_name': 'UserUpdate'},
            'action': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'retailer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['retailer.Retailer']", 'null': 'True', 'blank': 'True'}),
            'reward': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['punchcode.Reward']", 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'updates'", 'to': "orm['account.UserAccount']"})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 6, 5, 0, 38, 44, 845425)'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 6, 5, 0, 38, 44, 845295)'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
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
            'point': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'registration_code': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['retailer.RegistrationCode']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'zip': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['location.Zip']"})
        }
    }

    complete_apps = ['account']
