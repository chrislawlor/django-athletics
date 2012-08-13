# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Town'
        db.create_table('athletics_town', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('athletics', ['Town'])

        # Adding model 'Sport'
        db.create_table('athletics_sport', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
        ))
        db.send_create_signal('athletics', ['Sport'])

        # Adding model 'Position'
        db.create_table('athletics_position', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('game', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['athletics.Sport'])),
            ('description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('athletics', ['Position'])

        # Adding unique constraint on 'Position', fields ['game', 'slug']
        db.create_unique('athletics_position', ['game_id', 'slug'])

        # Adding model 'School'
        db.create_table('athletics_school', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('phone', self.gf('django.contrib.localflavor.us.models.PhoneNumberField')(max_length=20, null=True, blank=True)),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('town', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['athletics.Town'])),
            ('mascot', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('lat_long', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('school_type', self.gf('django.db.models.fields.CharField')(default='NA', max_length=2)),
            ('public', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('athletics', ['School'])

        # Adding M2M table for field administrators on 'School'
        db.create_table('athletics_school_administrators', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('school', models.ForeignKey(orm['athletics.school'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('athletics_school_administrators', ['school_id', 'user_id'])

        # Adding model 'Team'
        db.create_table('athletics_team', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('school', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['athletics.School'], null=True, blank=True)),
            ('sport', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['athletics.Sport'])),
            ('sport_type', self.gf('django.db.models.fields.CharField')(default='NA', max_length=2)),
            ('gender', self.gf('django.db.models.fields.CharField')(default='M', max_length=1)),
            ('public', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('athletics', ['Team'])

        # Adding model 'Membership'
        db.create_table('athletics_membership', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('teamseason', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['athletics.TeamSeason'])),
        ))
        db.send_create_signal('athletics', ['Membership'])

        # Adding M2M table for field positions on 'Membership'
        db.create_table('athletics_membership_positions', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('membership', models.ForeignKey(orm['athletics.membership'], null=False)),
            ('position', models.ForeignKey(orm['athletics.position'], null=False))
        ))
        db.create_unique('athletics_membership_positions', ['membership_id', 'position_id'])

        # Adding model 'CoachingPosition'
        db.create_table('athletics_coachingposition', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('teamseason', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['athletics.TeamSeason'])),
        ))
        db.send_create_signal('athletics', ['CoachingPosition'])

        # Adding model 'LeagueMembership'
        db.create_table('athletics_leaguemembership', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('league', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['athletics.League'])),
            ('team', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['athletics.Team'])),
            ('joined', self.gf('django.db.models.fields.DateField')()),
            ('left', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal('athletics', ['LeagueMembership'])

        # Adding model 'League'
        db.create_table('athletics_league', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('acryonym', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal('athletics', ['League'])

        # Adding model 'Season'
        db.create_table('athletics_season', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('year', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('sport', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['athletics.Sport'])),
        ))
        db.send_create_signal('athletics', ['Season'])

        # Adding model 'TeamSeason'
        db.create_table('athletics_teamseason', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('season', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['athletics.Season'])),
            ('team', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['athletics.Team'])),
            ('year', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('athletics', ['TeamSeason'])

        # Adding model 'Location'
        db.create_table('athletics_location', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
            ('school', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['athletics.School'], null=True, blank=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('zipcode', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('state', self.gf('django.contrib.localflavor.us.models.USStateField')(max_length=2)),
            ('lat_long', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('public', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('athletics', ['Location'])

        # Adding model 'Game'
        db.create_table('athletics_game', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('start', self.gf('django.db.models.fields.DateTimeField')()),
            ('end', self.gf('django.db.models.fields.DateTimeField')()),
            ('home_team', self.gf('django.db.models.fields.related.ForeignKey')(related_name='home_team', to=orm['athletics.Team'])),
            ('away_team', self.gf('django.db.models.fields.related.ForeignKey')(related_name='away_team', to=orm['athletics.Team'])),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['athletics.Location'])),
            ('home_team_score', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('away_team_score', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('season', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['athletics.Season'])),
            ('summary', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('athletics', ['Game'])


    def backwards(self, orm):
        # Removing unique constraint on 'Position', fields ['game', 'slug']
        db.delete_unique('athletics_position', ['game_id', 'slug'])

        # Deleting model 'Town'
        db.delete_table('athletics_town')

        # Deleting model 'Sport'
        db.delete_table('athletics_sport')

        # Deleting model 'Position'
        db.delete_table('athletics_position')

        # Deleting model 'School'
        db.delete_table('athletics_school')

        # Removing M2M table for field administrators on 'School'
        db.delete_table('athletics_school_administrators')

        # Deleting model 'Team'
        db.delete_table('athletics_team')

        # Deleting model 'Membership'
        db.delete_table('athletics_membership')

        # Removing M2M table for field positions on 'Membership'
        db.delete_table('athletics_membership_positions')

        # Deleting model 'CoachingPosition'
        db.delete_table('athletics_coachingposition')

        # Deleting model 'LeagueMembership'
        db.delete_table('athletics_leaguemembership')

        # Deleting model 'League'
        db.delete_table('athletics_league')

        # Deleting model 'Season'
        db.delete_table('athletics_season')

        # Deleting model 'TeamSeason'
        db.delete_table('athletics_teamseason')

        # Deleting model 'Location'
        db.delete_table('athletics_location')

        # Deleting model 'Game'
        db.delete_table('athletics_game')


    models = {
        'athletics.coachingposition': {
            'Meta': {'object_name': 'CoachingPosition'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'teamseason': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['athletics.TeamSeason']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'athletics.game': {
            'Meta': {'object_name': 'Game'},
            'away_team': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'away_team'", 'to': "orm['athletics.Team']"}),
            'away_team_score': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'end': ('django.db.models.fields.DateTimeField', [], {}),
            'home_team': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'home_team'", 'to': "orm['athletics.Team']"}),
            'home_team_score': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['athletics.Location']"}),
            'season': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['athletics.Season']"}),
            'start': ('django.db.models.fields.DateTimeField', [], {}),
            'summary': ('django.db.models.fields.TextField', [], {}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'})
        },
        'athletics.league': {
            'Meta': {'object_name': 'League'},
            'acryonym': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'teams': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['athletics.Team']", 'through': "orm['athletics.LeagueMembership']", 'symmetrical': 'False'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'athletics.leaguemembership': {
            'Meta': {'object_name': 'LeagueMembership'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'joined': ('django.db.models.fields.DateField', [], {}),
            'league': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['athletics.League']"}),
            'left': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['athletics.Team']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'})
        },
        'athletics.location': {
            'Meta': {'object_name': 'Location'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat_long': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'school': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['athletics.School']", 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'state': ('django.contrib.localflavor.us.models.USStateField', [], {'max_length': '2'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'athletics.membership': {
            'Meta': {'object_name': 'Membership'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'positions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['athletics.Position']", 'null': 'True', 'blank': 'True'}),
            'teamseason': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['athletics.TeamSeason']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'athletics.position': {
            'Meta': {'unique_together': "(['game', 'slug'],)", 'object_name': 'Position'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'game': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['athletics.Sport']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'})
        },
        'athletics.school': {
            'Meta': {'object_name': 'School'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'administrators': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "''", 'null': 'True', 'symmetrical': 'False', 'to': "orm['auth.User']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat_long': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'mascot': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'phone': ('django.contrib.localflavor.us.models.PhoneNumberField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'school_type': ('django.db.models.fields.CharField', [], {'default': "'NA'", 'max_length': '2'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'town': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['athletics.Town']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'athletics.season': {
            'Meta': {'object_name': 'Season'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sport': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['athletics.Sport']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'year': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'athletics.sport': {
            'Meta': {'object_name': 'Sport'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'})
        },
        'athletics.team': {
            'Meta': {'object_name': 'Team'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'gender': ('django.db.models.fields.CharField', [], {'default': "'M'", 'max_length': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'school': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['athletics.School']", 'null': 'True', 'blank': 'True'}),
            'sport': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['athletics.Sport']"}),
            'sport_type': ('django.db.models.fields.CharField', [], {'default': "'NA'", 'max_length': '2'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'})
        },
        'athletics.teamseason': {
            'Meta': {'object_name': 'TeamSeason'},
            'coaches': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'coaching_seasons'", 'symmetrical': 'False', 'through': "orm['athletics.CoachingPosition']", 'to': "orm['auth.User']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'roster': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'playing_seasons'", 'symmetrical': 'False', 'through': "orm['athletics.Membership']", 'to': "orm['auth.User']"}),
            'season': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['athletics.Season']"}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['athletics.Team']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'year': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'athletics.town': {
            'Meta': {'object_name': 'Town'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
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
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
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
        }
    }

    complete_apps = ['athletics']