from __future__ import unicode_literals

from collections import OrderedDict
import json

from django.db import models
from django.utils.text import slugify
#from django.contrib.postgres.fields import JSONField
from jsonfield import JSONField
from model_utils.models import TimeStampedModel

class MetadataSchema(TimeStampedModel):

    title = models.CharField(max_length=100)
    published = models.BooleanField(default=False)
    slug = models.SlugField(max_length=120, blank=True)
    version = models.DecimalField(default=1.0, decimal_places=2, max_digits=5)
    schema = JSONField(load_kwargs={'object_pairs_hook': OrderedDict})
    description = models.TextField(blank=True)

    def __str__(self):
        return '%s' % (self.title)

    def as_json(self, indent=None):

        if indent is not None:
            indent=4
        return json.dumps(self.schema, indent=indent)


    def add_version_to_schema(self):


        self_dict = { 'self' : dict(version=self.version,\
                                modified=str(self.modified),\
                                description=self.description)}
        updated_schema = OrderedDict(self_dict)
        for k, v in self.schema.items():
            updated_schema[k] = v
        self.schema = updated_schema

    def as_dict(self):
        return self.schema


    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        self.add_version_to_schema()
        super(MetadataSchema, self).save(*args, **kwargs)

    class Meta:
        unique_together = ('title', 'version')
        ordering = ('title', '-version',)

"""
from metadata_organizer.models import MetadataSchema
for m in MetadataSchema.objects.all(): m.as_json()
"""
