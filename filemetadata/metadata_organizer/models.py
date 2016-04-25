from __future__ import unicode_literals

import collections
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
    schema = JSONField(load_kwargs={'object_pairs_hook': collections.OrderedDict})
    description = models.TextField(blank=True)

    def __str__(self):
        return '%s' % (self.title)

    def as_json(self, with_indent=False):
        if with_indent:
            return json.dumps(self.schema, indent=4)
        else:
            return json.dumps(self.schema)

        #   object_pairs_hook=collections.OrderedDict)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(MetadataSchema, self).save(*args, **kwargs)

    class Meta:
        unique_together = ('title', 'version')
        ordering = ('title', '-version',)

"""
from metadata_organizer.models import MetadataSchema
for m in MetadataSchema.objects.all(): m.as_json()
"""
