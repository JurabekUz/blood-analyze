from django.contrib import admin

from .models import Disease, Media


class MediaAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


class DiseaseAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at', 'is_active']


admin.site.register(Media, MediaAdmin)
admin.site.register(Disease, DiseaseAdmin)

