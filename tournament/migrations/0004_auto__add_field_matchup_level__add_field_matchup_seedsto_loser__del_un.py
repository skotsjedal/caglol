# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'Matchup', fields ['tier', 'tournament', 'number']
        db.delete_unique('tournament_matchup', ['tier', 'tournament_id', 'number'])

        # Adding field 'Matchup.level'
        db.add_column('tournament_matchup', 'level',
                      self.gf('django.db.models.fields.CharField')(default='w', max_length=1),
                      keep_default=False)

        # Adding field 'Matchup.seedsto_loser'
        db.add_column('tournament_matchup', 'seedsto_loser',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='seeds_to_loser', null=True, blank=True, to=orm['tournament.Matchup']),
                      keep_default=False)

        # Adding unique constraint on 'Matchup', fields ['tier', 'tournament', 'number', 'level']
        db.create_unique('tournament_matchup', ['tier', 'tournament_id', 'number', 'level'])


    def backwards(self, orm):
        # Removing unique constraint on 'Matchup', fields ['tier', 'tournament', 'number', 'level']
        db.delete_unique('tournament_matchup', ['tier', 'tournament_id', 'number', 'level'])

        # Deleting field 'Matchup.level'
        db.delete_column('tournament_matchup', 'level')

        # Deleting field 'Matchup.seedsto_loser'
        db.delete_column('tournament_matchup', 'seedsto_loser_id')

        # Adding unique constraint on 'Matchup', fields ['tier', 'tournament', 'number']
        db.create_unique('tournament_matchup', ['tier', 'tournament_id', 'number'])


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
            'Meta': {'unique_together': "(('tournament', 'tier', 'number', 'level'),)", 'object_name': 'Matchup'},
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 3, 9, 0, 0)', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.CharField', [], {'default': "'w'", 'max_length': '1'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'seedsto': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'seeds_to_winner'", 'null': 'True', 'blank': 'True', 'to': "orm['tournament.Matchup']"}),
            'seedsto_loser': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'seeds_to_loser'", 'null': 'True', 'blank': 'True', 'to': "orm['tournament.Matchup']"}),
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