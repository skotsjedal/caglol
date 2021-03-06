# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Matchup'
        db.create_table('tournament_matchup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tournament', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tournament.Tournament'])),
            ('number', self.gf('django.db.models.fields.IntegerField')()),
            ('teamone', self.gf('smart_selects.db_fields.ChainedForeignKey')(blank=True, related_name='matchup_team_one', null=True, to=orm['league.Team'])),
            ('teamtwo', self.gf('smart_selects.db_fields.ChainedForeignKey')(blank=True, related_name='matchup_team_two', null=True, to=orm['league.Team'])),
            ('teamonescore', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('teamtwoscore', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2013, 3, 8, 0, 0), blank=True)),
            ('tier', self.gf('django.db.models.fields.IntegerField')()),
            ('seedsto', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['tournament.Matchup'], null=True, blank=True)),
        ))
        db.send_create_signal('tournament', ['Matchup'])

        # Adding unique constraint on 'Matchup', fields ['tournament', 'number']
        db.create_unique('tournament_matchup', ['tournament_id', 'number'])

        # Adding model 'Participant'
        db.create_table('tournament_participant', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tournament', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tournament.Tournament'])),
            ('team', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['league.Team'])),
            ('seed', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('placement', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('tournament', ['Participant'])

        # Adding unique constraint on 'Participant', fields ['tournament', 'team']
        db.create_unique('tournament_participant', ['tournament_id', 'team_id'])

        # Adding model 'Tournament'
        db.create_table('tournament_tournament', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('short', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('flavor', self.gf('django.db.models.fields.TextField')(default='')),
            ('t_type', self.gf('django.db.models.fields.CharField')(default='d', max_length=1)),
        ))
        db.send_create_signal('tournament', ['Tournament'])


    def backwards(self, orm):
        # Removing unique constraint on 'Participant', fields ['tournament', 'team']
        db.delete_unique('tournament_participant', ['tournament_id', 'team_id'])

        # Removing unique constraint on 'Matchup', fields ['tournament', 'number']
        db.delete_unique('tournament_matchup', ['tournament_id', 'number'])

        # Deleting model 'Matchup'
        db.delete_table('tournament_matchup')

        # Deleting model 'Participant'
        db.delete_table('tournament_participant')

        # Deleting model 'Tournament'
        db.delete_table('tournament_tournament')


    models = {
        'league.player': {
            'Meta': {'object_name': 'Player'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'realname': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            'role': ('django.db.models.fields.CharField', [], {'default': "'u'", 'max_length': '1'})
        },
        'league.team': {
            'Meta': {'object_name': 'Team'},
            'icon': ('django.db.models.fields.files.FileField', [], {'max_length': '50', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'player': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['league.Player']", 'symmetrical': 'False'}),
            'short': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'})
        },
        'tournament.matchup': {
            'Meta': {'unique_together': "(('tournament', 'number'),)", 'object_name': 'Matchup'},
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 3, 8, 0, 0)', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'seedsto': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['tournament.Matchup']", 'null': 'True', 'blank': 'True'}),
            'teamone': ('smart_selects.db_fields.ChainedForeignKey', [], {'blank': 'True', 'related_name': "'matchup_team_one'", 'null': 'True', 'to': "orm['league.Team']"}),
            'teamonescore': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'teamtwo': ('smart_selects.db_fields.ChainedForeignKey', [], {'blank': 'True', 'related_name': "'matchup_team_two'", 'null': 'True', 'to': "orm['league.Team']"}),
            'teamtwoscore': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'tier': ('django.db.models.fields.IntegerField', [], {}),
            'tournament': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tournament.Tournament']"})
        },
        'tournament.participant': {
            'Meta': {'unique_together': "(('tournament', 'team'),)", 'object_name': 'Participant'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'placement': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'seed': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['league.Team']"}),
            'tournament': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tournament.Tournament']"})
        },
        'tournament.tournament': {
            'Meta': {'object_name': 'Tournament'},
            'flavor': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'short': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            't_type': ('django.db.models.fields.CharField', [], {'default': "'d'", 'max_length': '1'})
        }
    }

    complete_apps = ['tournament']