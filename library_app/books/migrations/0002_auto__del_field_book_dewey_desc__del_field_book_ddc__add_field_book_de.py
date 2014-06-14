# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Book.dewey_desc'
        db.delete_column('books_book', 'dewey_desc')

        # Deleting field 'Book.ddc'
        db.delete_column('books_book', 'ddc')

        # Adding field 'Book.dewey_decimal'
        db.add_column('books_book', 'dewey_decimal',
                      self.gf('django.db.models.fields.CharField')(max_length=20, default='', blank=True),
                      keep_default=False)

        # Adding field 'Book.dewey_description'
        db.add_column('books_book', 'dewey_description',
                      self.gf('django.db.models.fields.CharField')(max_length=200, default='', blank=True),
                      keep_default=False)

        # Adding field 'Book.added_on'
        db.add_column('books_book', 'added_on',
                      self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2014, 6, 14, 0, 0), blank=True, auto_now_add=True),
                      keep_default=False)


        # Changing field 'Book.description'
        db.alter_column('books_book', 'description', self.gf('django.db.models.fields.TextField')())

        # Changing field 'Book.isbn'
        db.alter_column('books_book', 'isbn', self.gf('django.db.models.fields.IntegerField')(null=True))

    def backwards(self, orm):
        # Adding field 'Book.dewey_desc'
        db.add_column('books_book', 'dewey_desc',
                      self.gf('django.db.models.fields.CharField')(max_length=200, default=12),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'Book.ddc'
        raise RuntimeError("Cannot reverse this migration. 'Book.ddc' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Book.ddc'
        db.add_column('books_book', 'ddc',
                      self.gf('django.db.models.fields.CharField')(max_length=20),
                      keep_default=False)

        # Deleting field 'Book.dewey_decimal'
        db.delete_column('books_book', 'dewey_decimal')

        # Deleting field 'Book.dewey_description'
        db.delete_column('books_book', 'dewey_description')

        # Deleting field 'Book.added_on'
        db.delete_column('books_book', 'added_on')


        # Changing field 'Book.description'
        db.alter_column('books_book', 'description', self.gf('django.db.models.fields.CharField')(max_length=4000))

        # User chose to not deal with backwards NULL issues for 'Book.isbn'
        raise RuntimeError("Cannot reverse this migration. 'Book.isbn' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'Book.isbn'
        db.alter_column('books_book', 'isbn', self.gf('django.db.models.fields.IntegerField')())

    models = {
        'books.book': {
            'Meta': {'object_name': 'Book'},
            'added_on': ('django.db.models.fields.DateField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'author': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'dewey_decimal': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'dewey_description': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isbn': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'owner': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['books']