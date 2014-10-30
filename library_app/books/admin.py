from django.contrib import admin
from books.models import Book
from django import forms
from django.template.response import TemplateResponse
from django.contrib import messages
from django.contrib.admin import helpers

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


def change_location(modeladmin, request, queryset):
    #print('something')
    # The user has already confirmed the deletion.
    # Do the deletion and return a None to display the change list view again.
    opts = modeladmin.model._meta
    app_label = opts.app_label
    
    if request.POST.get('post'):
        n = queryset.count()
        if n:
            queryset.update(location=request.POST.get('location'))
            modeladmin.message_user(request, "Successfully updated location on %s books" % n, messages.SUCCESS)
        # Return None to display the change list page again.
        return None

    context = {
        'queryset': queryset,
        'opts': opts,
        'app_label': app_label,
        'action_checkbox_name': helpers.ACTION_CHECKBOX_NAME,
    }

    # Display the confirmation page
    return TemplateResponse(request, "books/change_location.html", context, current_app=modeladmin.admin_site.name)
change_location.short_description = 'Change Location'        

class BookAdmin(admin.ModelAdmin):
    list_filter = (('dewey_decimal', RangeFilter), 'owner', 'location')
    actions = [change_location]
    list_display = ('title', 'dewey_decimal', 'owner', 'location',)

admin.site.register(Book, BookAdmin)
admin.filters.FieldListFilter.register(
    lambda f: isinstance(f, models.CharField), RangeFilter)
