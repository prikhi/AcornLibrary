from django.db import models
from django.forms import ModelForm

from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase
from mptt.models import MPTTModel, TreeForeignKey

# Create your models here.

class TaggedSubject(TaggedItemBase):
    content_object = models.ForeignKey('Book')

class Book(models.Model):
    isbn = models.IntegerField(null=True, blank=True)
    title = models.CharField(max_length=200)
    authors = TaggableManager(verbose_name="Author(s)", help_text="")
    subjects = TaggableManager(verbose_name='FAST subject heading(s)', through=TaggedSubject, help_text="")
    subjects.rel.related_name = "+"
    dewey_decimal = models.CharField(max_length=20, blank=True)
    dewey_description = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=200, blank=True)
    owner = models.CharField(max_length=200, blank=True)
    added_on = models.DateField(auto_now_add=True)

    def __unicode__(self):
        return self.title
        
    def object(self):
        return self


class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ['isbn', 'title', 'authors', 'subjects', 'dewey_decimal', 'description', 'location', 'owner']
        labels = {
            'isbn': 'ISBN',
            'dewey_decimal': 'Dewey Decimal #',
            'description': 'Description',
            'authors': 'Author(s)',
            'subjects': 'Subject(s)',
        }
        
        
class Category(MPTTModel):
    number = models.CharField(max_length=3)
    title = models.CharField(max_length=100)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['number']
