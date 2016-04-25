from os.path import isfile
import json
from jsonschema import validate
from jsonschema import Draft3Validator, Draft4Validator

def open_json_file(fname):
    assert isfile(fname), 'file not found: %s' % fname

    json_file =  open(fname, 'r').read()
    return json.loads(json_file)

def show_pretty_json(dict_info):
    print json.dumps(dict_info, indent=4)

def validate_json(schema_fname, json_data_fname, show_schema=False):
    schema = open_json_file(schema_fname)
    json_data = open_json_file(json_data_fname)

    if show_schema:
        show_pretty_json(schema)

    try:
        #d4 = Draft3Validator(schema)
        #d4.validate(json_data)
        validate(json_data, schema)
        print 'looks good'
    except Exception as e:
        print 'Exception', type(e), e


if __name__=='__main__':
    num = str(3).zfill(2)
    schema_file = 'schema_%s.json' % num
    data_file = 'data_%s.json' % num
    validate_json(schema_file, data_file, show_schema=False)
