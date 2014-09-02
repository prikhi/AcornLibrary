# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'SubjectTag'
        db.delete_table('books_subjecttag')

        # Deleting model 'SubjectTaggedItem'
        db.delete_table('books_subjecttaggeditem')

        # Adding model 'TaggedSubject'
        db.create_table('books_taggedsubject', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tag', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['taggit.Tag'], related_name='books_taggedsubject_items')),
            ('content_object', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['books.Book'])),
        ))
        db.send_create_signal('books', ['TaggedSubject'])


    def backwards(self, orm):
        # Adding model 'SubjectTag'
        db.create_table('books_subjecttag', (
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=100, unique=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, unique=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('books', ['SubjectTag'])

        # Adding model 'SubjectTaggedItem'
        db.create_table('books_subjecttaggeditem', (
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'], related_name='books_subjecttaggeditem_tagged_items')),
            ('object_id', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
            ('tag', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['books.SubjectTag'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('books', ['SubjectTaggedItem'])

        # Deleting model 'TaggedSubject'
        db.delete_table('books_taggedsubject')


    models = {
        'books.book': {
            'Meta': {'object_name': 'Book'},
            'added_on': ('django.db.models.fields.DateField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'dewey_decimal': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '20'}),
            'dewey_description': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isbn': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '200'}),
            'owner': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '200'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'books.taggedsubject': {
            'Meta': {'object_name': 'TaggedSubject'},
            'content_object': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['books.Book']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['taggit.Tag']", 'related_name': "'books_taggedsubject_items'"})
        },
        'taggit.tag': {
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'unique': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100', 'unique': 'True'})
        }
    }

    complete_apps = ['books']