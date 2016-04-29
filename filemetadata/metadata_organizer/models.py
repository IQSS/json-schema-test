from __future__ import unicode_literals

from collections import OrderedDict
import json
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.text import slugify
#from django.contrib.postgres.fields import JSONField
from jsonfield import JSONField
from model_utils.models import TimeStampedModel
from decimal import Decimal
from proj_utils.decimal_encoder import DecimalEncoder
from proj_utils.msg_util import msgt

class MetadataSchema(TimeStampedModel):

    title = models.CharField(max_length=100)
    published = models.BooleanField(default=True)
    slug = models.SlugField(max_length=120, blank=True)
    version = models.DecimalField(default=1.0, decimal_places=2, max_digits=5)
    schema = JSONField(load_kwargs={'object_pairs_hook': OrderedDict})
    description = models.TextField(blank=True)
    contributor = models.CharField(max_length=255, default='Dataverse core')

    def __str__(self):
        return '%s (%s)' % (self.title, self.version)

    class Meta:
        unique_together = ('title', 'version')
        ordering = ('title', '-version',)

    @staticmethod
    def get_next_version(title, minor_version=False):

        qs = MetadataSchema.objects.filter(title=title).order_by('-version').first()
        if qs is None:
            return Decimal('1.0')

        if minor_version:
            # e.g. 1.5 -> 1.6
            return qs.version + Decimal('.1')
        else:
            # e.g.  1.6 -> 2.0
            return Decimal(int(qs.version)) + Decimal('1.0')


    def get_schema_dict(self):
        return self.schema

    def as_json(self, indent=None):
        """
        Dump the schema as JSON
        """
        if indent is not None:
            indent=4

        schema_copy = self.as_json_dict()

        return json.dumps(schema_copy, indent=indent)

    def as_json_dict(self):
        """
        Format the schema for JSON dump.
        - Change the version from a Decimal to a float
        """
        schema_copy = self.schema.copy()
        schema_copy['self']['version'] = float(schema_copy['self']['version'])

        return schema_copy


    def get_api_url(self):
        """
        Format the url so the schema may be retrieved via API
        """
        if not self.id:
            return 'n/a'
        api_dict = dict(schema_name_slug=self.slug,\
                    version=self.version)
        url = reverse('view_schema_with_identifier', kwargs=api_dict)

        return url

    def add_version_to_schema(self):


        self_dict = { 'self' : dict(version=self.version,\
                                url=self.get_api_url(),\
                                modified=str(self.modified),\
                                description=self.description,\
                                contributor=self.contributor)\
                    }
        updated_schema = OrderedDict(self_dict)
        for k, v in self.schema.items():
            if k == 'self': continue
            updated_schema[k] = v
        self.schema = updated_schema

    def as_dict(self):
        return self.schema

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        self.add_version_to_schema()
        super(MetadataSchema, self).save(*args, **kwargs)


class FileMetadata(TimeStampedModel):

    schema = models.ForeignKey(MetadataSchema)
    datafile_id = models.IntegerField(default=1)
    metadata = JSONField(load_kwargs={'object_pairs_hook': OrderedDict})
    published = models.BooleanField(default=True)
    # How does this version relate to DatasetVersion?
    version = models.IntegerField(default=1, help_text='Placeholder')

    class Meta:
        unique_together = ('schema', 'datafile_id', 'version')
        ordering = ('schema', '-version',)

    def __str__(self):
        return '%s, file id: %s (%s)' % (self.schema, self.datafile_id, self.version)

    def as_json(self, indent=None):

        if indent is not None:
            indent=4
        return json.dumps(self.schema, indent=indent)

    def save(self, *args, **kwargs):
        super(FileMetadata, self).save(*args, **kwargs)

"""
from metadata_organizer.models import MetadataSchema
for m in MetadataSchema.objects.all(): m.as_json()
"""
