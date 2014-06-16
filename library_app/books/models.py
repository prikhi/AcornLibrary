from django.db import models
from django.forms import ModelForm

# Create your models here.


class Book(models.Model):
    isbn = models.IntegerField(null=True, blank=True)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    dewey_decimal = models.CharField(max_length=20, blank=True)
    dewey_description = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=200, blank=True)
    owner = models.CharField(max_length=200, blank=True)
    added_on = models.DateField(auto_now_add=True)

    def __unicode__(self):
        return self.title


class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ['isbn', 'title', 'author', 'dewey_decimal', 'dewey_description', 'location', 'owner']
        labels = {
            'isbn': 'ISBN',
            'dewey_decimal': 'Dewey Decimal #',
            'dewey_description': 'Dewey Description',
        }
