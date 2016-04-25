#from django.shortcuts import render
import json
from decimal import Decimal
from django.http import HttpResponse, Http404
from django.views.decorators.http import require_POST, require_GET
from .models import MetadataSchema

@require_GET
def view_schema_list(request, with_indent=False):

    l = [m.as_dict() for m in MetadataSchema.objects.filter(published=True).all()]

    if with_indent:
        indent=4
    else:
        indent=None

    return HttpResponse(json.dumps(l, indent=indent), content_type='application/json')


@require_GET
def view_schema(request, schema_name_slug=None, version=None):
    schema_qs = MetadataSchema.objects.filter(slug=schema_name_slug)
    if version:
        version_num = Decimal(version)
        print 'version_num', version_num
        schema_qs = schema_qs.filter(version=version_num)

    schema_info = schema_qs.first()
    if schema_info is None:
        raise Http404('Does not exist')

    if 'pretty' in request.GET:
        indent=4
    else:
        indent=None

    #return render(schema_info.as_json(), mimetype='json'
    return HttpResponse(schema_info.as_json(indent=indent), content_type='application/json')



#@require_POST
#def add_schema(request):
