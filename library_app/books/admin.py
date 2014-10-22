from django.contrib import admin
from books.models import Book
from django import forms

class RangeForm(forms.Form):

    def __init__(self, *args, **kwargs):
        field_name = kwargs.pop('field_name')
        super(RangeForm, self).__init__(*args, **kwargs)

        self.fields['%s__gte' % field_name] = forms.DecimalField(required=False)

        self.fields['%s__lte' % field_name] = forms.DecimalField(required=False)
        
        
class RangeFilter(admin.filters.FieldListFilter):
    template = 'books/filter.html'

    def __init__(self, field, request, params, model, model_admin, field_path):
        self.lookup_kwarg_since = '%s__gte' % field_path
        self.lookup_kwarg_upto = '%s__lte' % field_path
        super(RangeFilter, self).__init__(
            field, request, params, model, model_admin, field_path)
        self.form = self.get_form(request)

    def choices(self, cl):
        return []

    def expected_parameters(self):
        return [self.lookup_kwarg_since, self.lookup_kwarg_upto]

    def get_form(self, request):
        return RangeForm(data=self.used_parameters,
                             field_name=self.field_path)

    def queryset(self, request, queryset):
        if self.form.is_valid():
            # get no null params
            filter_params = dict(filter(lambda x: bool(x[1]),
                                        self.form.cleaned_data.items()))
            return queryset.filter(**filter_params)
        else:
            return queryset
            

class BookAdmin(admin.ModelAdmin):
    list_filter = ('owner', 'location', ('dewey_decimal', RangeFilter))

admin.site.register(Book, BookAdmin)
admin.filters.FieldListFilter.register(
    lambda f: isinstance(f, models.CharField), RangeFilter)
