from django.contrib import admin
from .models import Place


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'org_name', 'category', 'lat', 'lng')
    list_filter = ('category', 'org_name')
    search_fields = ('name', 'org_name', 'address')