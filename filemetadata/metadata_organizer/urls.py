from django.conf.urls import url

from metadata_organizer.views import view_schema, view_schema_list

urlpatterns = [


    url(r'^schema/(?P<schema_name_slug>\w{4,150})/(?P<version>\d+(\.\d{0,2}|))/?$', view_schema, name='view_schema'),
    url(r'^schema/(?P<schema_name_slug>\w{4,150})/?$', view_schema, name='view_schema'),
    url(r'^schema/list$', view_schema_list, name='view_schema_list'),
    #url(r'^tsv-json-form/$', view_json_form, name='view_json_form'),
    #url(r'^make-json-schema/$', view_make_json_schema, name='view_make_json_schema'),
    #url(r'^make-all-json-schemas/$', view_make_all_json_schemas, name='view_make_all_json_schemas'),
    #url(r'^delete-all-json-schemas/$', view_delete_all_json_schemas, name='view_delete_all_json_schemas')
]
