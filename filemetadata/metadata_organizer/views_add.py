#from django.shortcuts import render
from django.http import HttpResponse#, Http404
from django.views.decorators.http import require_POST#, require_GET
from django.views.decorators.csrf import csrf_exempt

from .forms import MetadataSchemaForm
#from .utils import validate_schema, validate_filemetadata
from proj_utils.message_helper_json import MessageHelperJSON

@require_POST
@csrf_exempt
def add_schema(request):

    f = MetadataSchemaForm(request.POST)
    if not f.is_valid():
        json_msg = MessageHelperJSON.get_json_fail_msg('Failed to add schema',\
                            data_dict=f.errors)
        return HttpResponse(json_msg, content_type="application/json", status=200)

    metadata_schema_obj = f.save_schema()
    json_msg = MessageHelperJSON.get_json_success_msg('success',\
                            data_dict=metadata_schema_obj.as_json_dict())

    return HttpResponse(json_msg, content_type="application/json", status=200)
