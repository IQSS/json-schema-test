
from django.test import TestCase
from metadata_organizer.utils import validate_schema,\
    validate_schema_string,\
    validate_filemetadata,\
    ERR_MSG_SCHEMA_NONE
import json
import collections
from os.path import isfile, isdir, join, realpath, dirname
from utils.msg_util import msg, msgt

TEST_FILE_DIR = join(dirname(realpath(__file__)), 'test_files')

class JoinTargetTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        msg('\n>>> setUpClass SchemaValidationTestCase')
        super(SchemaValidationTestCase, cls).setUpClass()

        # Verify test directory exists
        assert isdir(TEST_FILE_DIR),\
            "Test file directory not found: %s" % TEST_FILE_DIR

    def load_json_test_file(self, filename):

        full_filename = join(TEST_FILE_DIR, filename)
        assert isfile(full_filename), "Test file not found: %s" % full_filename

        try:
            return json.loads(open(full_filename, 'r').read(),\
                object_pairs_hook=collections.OrderedDict)
        except ValueError as e:
            msg('JSON load error: %s' % e.message)
            msgx('This file is not valid JSON: %s' % full_filename)

        cls.layer_attribute_info = 'boohoo layer_attribute_info'

    def setUp(self):
        pass


    def test_01_schema_valid(self):
        msgt('1 - Test a valid schema')
        schema = self.load_json_test_file('astro_schema_good_01.json')
        self.assertTrue(validate_schema(schema))

        # Test it as a string
        msg('1a - Test it as a string')
        schema_string = json.dumps(schema)
        self.assertTrue(validate_schema_string(schema_string))

    def test_02_schema_null(self):
        msgt('2- Test sending "None" for validation')
        success, error_list = validate_schema(None)
        self.assertEqual(success, False)
        self.assertEqual(error_list[0], ERR_MSG_SCHEMA_NONE)

        # Test it as a string
        msg('2a - Test it as a string')
        success, error_list = validate_schema_string(None)
        self.assertEqual(success, False)
        self.assertEqual(error_list[0], ERR_MSG_SCHEMA_NONE)

    def test_03_schema_dupe_enum_value(self):
        msgt('3 - Schema with duplicate enum value')
        success, error_list = validate_schema(schema)
        self.assertEqual(success, False)
        self.assertEqual(error_list[0], u'Error Location: properties->astroType->items')
        self.assertTrue(error_list[1].endswith(\
            'is not valid under any of the given schemas'))



    def test_04_schema_invalid_required_field(self):
        msgt('4 - Schema with invalid required field')
        success, error_list = validate_schema(schema)
        self.assertEqual(success, False)
        self.assertEqual(error_list[0], u'Error Location: properties->astroFacility->items')
        self.assertTrue(error_list[1].endswith(\
            'is not valid under any of the given schemas'))







