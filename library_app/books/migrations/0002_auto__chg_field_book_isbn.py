# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Book.isbn'
        db.alter_column('books_book', 'isbn', self.gf('django.db.models.fields.CharField')(max_length=13, default=''))

    def backwards(self, orm):

        # Changing field 'Book.isbn'
        db.alter_column('books_book', 'isbn', self.gf('django.db.models.fields.IntegerField')(null=True))

    models = {
        'books.book': {
            'Meta': {'object_name': 'Book'},
            'added_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'dewey_decimal': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'dewey_description': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'ebook': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_ebook_only': ('django.db.models.fields.BooleanField', [], {}),
            'isbn': ('django.db.models.fields.CharField', [], {'max_length': '13', 'blank': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'owner': ('django.db.models.fields.CharField', [], {'max_length': '200', 'default': "'xfghj'", 'blank': 'True'}),
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
            'parent': ('mptt.fields.TreeForeignKey', [], {'to': "orm['books.Category']", 'blank': 'True', 'related_name': "'children'", 'null': 'True'}),
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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'unique': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100', 'unique': 'True'})
        }
    }

    complete_apps = ['books']