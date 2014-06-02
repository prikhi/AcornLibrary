from django.db import models

# Create your models here.
class Book(models.Model):
    isbn = models.IntegerField()
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    ddc = models.CharField(max_length=20)
    dewey_desc = models.CharField(max_length=200)
    description = models.CharField(max_length=4000)
    location = models.CharField(max_length=200)
    owner = models.CharField(max_length=200)

    def __unicode__(self):
        return self.title
