from django.contrib import admin

from polls.models import Choice, Poll


class ChoiceInline(admin.TabularInline):

    model = Choice
    extra = 3


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):

    fieldsets = [
        (None, {'fields': ['question', 'author'], }),
        ('Date information', {'fields': ['pub_date'], }),
    ]
    inlines = [ChoiceInline]
    list_display = ('question', 'pub_date',)
    list_filter = ['pub_date']
    search_fields = ['question']
    date_hierarchy = 'pub_date'
