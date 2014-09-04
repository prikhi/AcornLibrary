import datetime
from haystack import indexes
from books.models import Book


class BookIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    authors = indexes.MultiValueField()
    subjects = indexes.MultiValueField()
    description = indexes.CharField()

    def get_model(self):
        return Book

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects  #.filter(pub_date__lte=datetime.datetime.now())
        
    def prepare_tags(self, obj):
        return [author.name for author in obj.authors.all()] + [subject.name for subject in obj.subjects.all()]
