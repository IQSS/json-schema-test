from django.contrib import admin

from metadata_organizer.models import MetadataSchema


class MetadataSchemaAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ['title', 'slug', 'version', 'published',  'description','modified', 'created']
    search_fields = ['title',]
    list_filter = ['published', 'version', 'title']
    readonly_fields = ['modified', 'created']
admin.site.register(MetadataSchema, MetadataSchemaAdmin)
