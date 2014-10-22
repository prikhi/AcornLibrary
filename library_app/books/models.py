from django.db import models
from django.forms import ModelForm
from django.db.models import F
from django import forms

from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase
from mptt.models import MPTTModel, TreeForeignKey

# Create your models here.
def last_location():
    latest = Book.objects.latest('added_on')
    return latest.location

def last_owner():
    latest = Book.objects.latest('added_on')
    return latest.owner

class TaggedSubject(TaggedItemBase):
    content_object = models.ForeignKey('Book')
    
    
class Category(MPTTModel):
    number = models.CharField(max_length=3)
    link_number = models.CharField(max_length=3)
    title = models.CharField(max_length=100)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    book_count = models.IntegerField(default=0, blank=False, null=False)
    is_leaf = models.BooleanField(default=False)

    class MPTTMeta:
        order_insertion_by = ['number']
    

class Book(models.Model):
    isbn = models.IntegerField(null=True, blank=True)
    title = models.CharField(max_length=200)
    authors = TaggableManager(verbose_name="Author(s)", help_text="")
    subjects = TaggableManager(verbose_name='FAST subject heading(s)', through=TaggedSubject, help_text="")
    subjects.rel.related_name = "+"
    dewey_decimal = models.CharField(max_length=20, blank=True)
    dewey_description = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=200, blank=True)#, default=last_location)
    owner = models.CharField(max_length=200, blank=True)#, default=last_owner)
    added_on = models.DateTimeField(auto_now_add=True)
    
    #reindex_related=('authors','subjects',)

    def __unicode__(self):
        return self.title
        
    def object(self):
        return self
        
    def save(self, *args, **kwargs):
    # TODO: This could probably be better handled by having an explicit relationship between categories and books. Need to uhderstand the capabilities of MPTT better.
        is_new = self.pk is None
        if is_new:
            dewey_num = self.dewey_decimal[:3]
            category = Category.objects.filter(number=dewey_num, is_leaf=True)[:1].get()
            while category:
                category.book_count = F('book_count') + 1
                category.save()
                category = category.parent
        else:
            new_dewey_num = self.dewey_decimal[:3]
            old_object = Book.objects.filter(pk=self.pk)[:1].get()
            old_dewey_num = old_object.dewey_decimal[:3]
            if old_dewey_num != new_dewey_num:
                category = Category.objects.filter(number=old_dewey_num, is_leaf=True)[:1].get()
                while category:
                    category.book_count = F('book_count') - 1
                    category.save()
                    category = category.parent
                category = Category.objects.filter(number=new_dewey_num, is_leaf=True)[:1].get()
                while category:
                    category.book_count = F('book_count') + 1
                    category.save()
                    category = category.parent
            
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
        widgets = {
            'description': forms.Textarea(attrs={'rows':7, 'cols':70}),
            'title': forms.TextInput(attrs={'size':'70'}),
        }
        
