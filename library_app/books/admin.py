from django.contrib import admin
from books.models import Book

class BookAdmin(admin.ModelAdmin):
    list_filter = ('owner', 'location')

admin.site.register(Book, BookAdmin)
