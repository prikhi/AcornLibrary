from django.db import models
from django.forms import ModelForm
from django.db.models import F

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
        
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        if is_new:
            dewey_num = self.dewey_decimal[:3]
            category = Category.objects.filter(number=dewey_num, is_leaf=True)[:1].get()
            while category:
                category.book_count = F('book_count') + 1
                category.save()
                category = category.parent
        # TODO: handle case when book is being updated
        super(Book, self).save(*args, **kwargs)


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
    link_number = models.CharField(max_length=3)
    title = models.CharField(max_length=100)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    book_count = models.IntegerField(default=0, blank=False, null=False)
    is_leaf = models.BooleanField(default=False)

    class MPTTMeta:
        order_insertion_by = ['number']
