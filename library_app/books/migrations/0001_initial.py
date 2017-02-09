# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TaggedSubject'
        db.create_table('books_taggedsubject', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tag', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['taggit.Tag'], related_name='books_taggedsubject_items')),
            ('content_object', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['books.Book'])),
        ))
        db.send_create_signal('books', ['TaggedSubject'])

        # Adding model 'Category'
        db.create_table('books_category', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('number', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('link_number', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('parent', self.gf('mptt.fields.TreeForeignKey')(blank=True, null=True, to=orm['books.Category'], related_name='children')),
            ('book_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('is_leaf', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal('books', ['Category'])

        # Adding model 'Book'
        db.create_table('books_book', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('isbn', self.gf('django.db.models.fields.IntegerField')(blank=True, null=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('dewey_decimal', self.gf('django.db.models.fields.CharField')(blank=True, max_length=20)),
            ('dewey_description', self.gf('django.db.models.fields.CharField')(blank=True, max_length=200)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('location', self.gf('django.db.models.fields.CharField')(blank=True, max_length=200)),
            ('owner', self.gf('django.db.models.fields.CharField')(blank=True, default='xfghj', max_length=200)),
            ('added_on', self.gf('django.db.models.fields.DateTimeField')(blank=True, auto_now_add=True)),
            ('ebook', self.gf('django.db.models.fields.files.FileField')(blank=True, null=True, max_length=100)),
            ('is_ebook_only', self.gf('django.db.models.fields.BooleanField')()),
        ))
        db.send_create_signal('books', ['Book'])


    def backwards(self, orm):
        # Deleting model 'TaggedSubject'
        db.delete_table('books_taggedsubject')

        # Deleting model 'Category'
        db.delete_table('books_category')

        # Deleting model 'Book'
        db.delete_table('books_book')


    models = {
        'books.book': {
            'Meta': {'object_name': 'Book'},
            'added_on': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'dewey_decimal': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '20'}),
            'dewey_description': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '200'}),
            'ebook': ('django.db.models.fields.files.FileField', [], {'blank': 'True', 'null': 'True', 'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_ebook_only': ('django.db.models.fields.BooleanField', [], {}),
            'isbn': ('django.db.models.fields.IntegerField', [], {'blank': 'True', 'null': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '200'}),
            'owner': ('django.db.models.fields.CharField', [], {'blank': 'True', 'default': "'xfghj'", 'max_length': '200'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'books.category': {
            'Meta': {'object_name': 'Category'},
            'book_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_leaf': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'link_number': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['books.Category']", 'related_name': "'children'"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
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
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'})
        }
    }

    complete_apps = ['books']