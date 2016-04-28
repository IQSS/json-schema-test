"""
Convenience method to validate a metadata against a JSON schema
"""
import json
import jsonschema
from jsonschema import Draft4Validator

CHOSEN_VALIDATOR_CLASS = Draft4Validator

def msgt(m1, m2):
    if m2 is None:
        return
    print '=' * 40
    print m1
    print '-' * 40
    print m2

ERR_MSG_SCHEMA_NONE = 'The schema was None (or null)'

def validate_schema(schema_dict):
    """
    Validate a schema using the Draft4Validator
    """
    if schema_dict is None:
        return False, [ERR_MSG_SCHEMA_NONE]
    try:
        CHOSEN_VALIDATOR_CLASS.check_schema(schema_dict)
        return True, None
    except jsonschema.exceptions.SchemaError as schema_err:
        err_msgs = []
        if schema_err.path:
            err_msg = 'Error Location: %s' % '->'.join(schema_err.path)
            err_msgs.append(err_msg)
        err_msgs.append('Error: %s' % schema_err.message)
        err_msgs.append('(Note: JSON schema Draft 4 validation was used)')

        return False, err_msgs



def validate_filemetadata(schema_dict, data_dict):
    """
    See jsonschema docs for error breakdown:
    https://python-jsonschema.readthedocs.org/en/latest/errors/#module-jsonschema
    """
    print 'validate_filemetadata'
    """
    try:
        jsonschema.validate(data_dict, schema_dict)
        return True, None
    except jsonschema.exceptions.ValidationError as errors:
        error_messages = '<br />'.join([err.message for err in errors])
        return (False, error_messages)
    except jsonschema.exceptions.SchemaError as schema_err:
        print schema_err
        print type(schema_err)
        #error_messages = '<br />'.join([err.message for err in errors])
        return (False, None)
    """
    print Draft4Validator.check_schema(schema_dict)

    validator = Draft4Validator(schema_dict)

    errors = sorted(validator.iter_errors(data_dict), key=lambda e: e.path)
    if errors:
        return False, str(errors)
    for error in errors:
        print error.message
        #for suberror in sorted(error.context, key=lambda e: e.schema_path):
        #    print suberror.schema_path, suberror.message

    #print errors

    return (True, None)
    """
    try:
        res = validate(data_dict, schema_dict)
        print type(res)
        return (True, None)
    except Exception as e:

        print 'unexpected error: ', type(e), e
        return (False, e)
    """
    #for suberror in sorted(error.context, key=lambda e: e.schema_path):
    #    print(list(suberror.schema_path), suberror.message, sep=", ")

if __name__ == '__main__':
    schema = {
                "items": {
                    "anyOf": [
                        {"type": "string", "maxLength": 2},
                        {"type": "integer", "minimum": 5}
                    ]
                },
                "hats" : {
                    "xtype" : "string",
                    "required" : False,
                    "Enum" : [1, 2, 3]
                }
            }
    content = open('tests/astro_good_01.json', 'rb').read()
    #content = open('tests/astro_bad_01.json', 'rb').read()
    #content = open('tests/identifier_01.json', 'rb').read()
    #content = open('tests/person_01.json', 'rb').read()
    #content = open('tests/repository.json', 'rb').read()
    schema = json.loads(content)
    success, err_list = validate_schema(schema)
    if not success:
        print '\n'.join(err_list)
    else:
        print 'success'
"""
import json
import jsonschema
from jsonschema import Draft4Validator
import os

def validate_schemas():
    json_fnames = [x for x in os.listdir('.') if x.endswith('.json')]
    for fname in json_fnames:
        #if not fname == 'customGSD.json': continue
        print '-' * 40
        print 'checking: %s', fname
        print '-' * 40
        content = open(fname, 'r').read()
        schema_dict = json.loads(content)
        try:
            Draft4Validator.check_schema(schema_dict)
            print 'yes'
        except jsonschema.exceptions.SchemaError as schema_err:
            print schema_err




def validate_schema(schema_dict):

    try:
        Draft4Validator.check_schema(schema_dict)
"""
