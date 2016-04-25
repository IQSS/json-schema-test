import json
import collections
from rest_framework import serializers, viewsets
#  from rest_framework import routers, serializers, viewsets

from metadata_organizer.models import MetadataSchema#, LANGUAGE_CHOICES, STYLE_CHOICES


#
class MetadataSchemaSerializer(serializers.HyperlinkedModelSerializer):

    def validate_schema(self, value):
        """
        The schema is a string, make sure it can be converted to JSON
        """
        try:
            schema_dict = json.loads(value,\
                object_pairs_hook=collections.OrderedDict)
        except:
            message = 'This field is not valid JSON'
            raise serializers.ValidationError(message)

        if not hasattr(schema_dict, 'keys'):
            message = 'Please enter a valid JSON schema'
            raise serializers.ValidationError(message)
        elif len(schema_dict) == 0:
            message = 'The JSON schema is empty'
            raise serializers.ValidationError(message)

        return schema_dict


    class Meta:
        model = MetadataSchema
        fields = ('title', 'published', 'version', 'schema', 'description',)


# ViewSets define the view behavior.
class MetadataSchemaViewSet(viewsets.ModelViewSet):
    queryset = MetadataSchema.objects.all()
    serializer_class = MetadataSchemaSerializer
