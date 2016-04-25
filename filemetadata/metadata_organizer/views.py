#from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_POST, require_GET
from .models import MetadataSchema

@require_GET
def view_schema(request, slug, version=None):

    schema_qs = MetadataSchema.objects.filter(slug=slug)
    if version:
        schema_qs.filter(version=version)

    schema_info = schema_qs.first()
    if schema_info is None:
        raise Http404('Does not exist')

    #return render(schema_info.as_json(), mimetype='json'
    return HttpResponse(schema_info.as_json(), content_type='application/json')

#@require_POST
#def add_schema(request):
