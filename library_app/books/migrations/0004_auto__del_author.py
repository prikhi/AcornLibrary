# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Author'
        db.delete_table('books_author')

        # Removing M2M table for field author on 'Book'
        db.delete_table(db.shorten_name('books_book_author'))


    def backwards(self, orm):
        # Adding model 'Author'
        db.create_table('books_author', (
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('books', ['Author'])

        # Adding M2M table for field author on 'Book'
        m2m_table_name = db.shorten_name('books_book_author')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('book', models.ForeignKey(orm['books.book'], null=False)),
            ('author', models.ForeignKey(orm['books.author'], null=False))
        ))
        db.create_unique(m2m_table_name, ['book_id', 'author_id'])


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
        }
    }

    complete_apps = ['books']