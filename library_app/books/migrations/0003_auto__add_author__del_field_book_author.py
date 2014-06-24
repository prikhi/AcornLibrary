# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Author'
        db.create_table('books_author', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('books', ['Author'])

        # Deleting field 'Book.author'
        db.delete_column('books_book', 'author')

        # Adding M2M table for field author on 'Book'
        m2m_table_name = db.shorten_name('books_book_author')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('book', models.ForeignKey(orm['books.book'], null=False)),
            ('author', models.ForeignKey(orm['books.author'], null=False))
        ))
        db.create_unique(m2m_table_name, ['book_id', 'author_id'])


    def backwards(self, orm):
        # Deleting model 'Author'
        db.delete_table('books_author')


        # User chose to not deal with backwards NULL issues for 'Book.author'
        raise RuntimeError("Cannot reverse this migration. 'Book.author' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Book.author'
        db.add_column('books_book', 'author',
                      self.gf('django.db.models.fields.CharField')(max_length=200),
                      keep_default=False)

        # Removing M2M table for field author on 'Book'
        db.delete_table(db.shorten_name('books_book_author'))


    models = {
        'books.author': {
            'Meta': {'object_name': 'Author'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'books.book': {
            'Meta': {'object_name': 'Book'},
            'added_on': ('django.db.models.fields.DateField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'author': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['books.Author']"}),
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