from django.contrib import admin
from lists.models import Item, List


class ItemAdmin(admin.ModelAdmin):
    fieldsets = [(None, {'fields': ['text']}),
                 ('Choose List', {'fields': ['list']})]

admin.site.register(List)
admin.site.register(Item, ItemAdmin)
