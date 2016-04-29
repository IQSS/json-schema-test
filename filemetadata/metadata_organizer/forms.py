from django import forms
from metadata_organizer.models import MetadataSchema#, FileMetadata
from metadata_organizer.utils import validate_schema,\
    validate_schema_string

class MetadataSchemaForm(forms.ModelForm):

    minor_version = forms.BooleanField(required=False)

    class Meta:
        model = MetadataSchema
        fields = ['schema', 'description', 'contributor']

    def save_schema(self):
        """
        Save a schema
        """
        assert hasattr(self, 'cleaned_data'),\
            "Make sure the form is valid before calling this method."

        contributor = self.cleaned_data['contributor']
        description = self.cleaned_data['description']

        # get title from schema
        #
        schema = self.cleaned_data['schema']
        title = schema['title']

        # Get the next version for this schema
        minor_version = self.cleaned_data['minor_version']
        version = MetadataSchema.get_next_version(title, minor_version)

        # Create a new object
        kwargs = dict(title=title,\
                    schema=schema,\
                    version=version,\
                    description=description,\
                    contributor=contributor)

        schema_obj = MetadataSchema(**kwargs)
        schema_obj.save()

        return schema_obj

    def clean_schema(self):
        schema = self.cleaned_data['schema']

        # Validate the schema using jsonschema
        #
        success, err_list = validate_schema(schema)
        if not success:
            error_msg = '\n'.join(err_list)
            raise forms.ValidationError(error_msg)

        # Make sure it has a title attribute
        #
        if not 'title' in schema:
            error_msg = 'The schema does not have a "title" attribute.'
            raise forms.ValidationError(error_msg)

        return schema
