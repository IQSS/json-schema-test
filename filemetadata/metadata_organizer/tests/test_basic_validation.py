
from django.test import TestCase
from metadata_organizer.utils import validate_schema, validate_filemetadata,\
    ERR_MSG_SCHEMA_NONE
import json
import collections
from os.path import isfile, isdir, join, realpath, dirname
from utils.msg_util import msg, msgt

TEST_FILE_DIR = join(dirname(realpath(__file__)), 'test_files')

class JoinTargetTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        msg('\n>>> setUpClass')
        super(JoinTargetTestCase, cls).setUpClass()

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
        schema = self.load_json_test_file('astro_good_01.json')
        self.assertTrue(validate_schema(schema))

    def test_0201__schema_null(self):
        msgt('2- Test sending "None" for validation')
        success, error_list = validate_schema(None)
        self.assertEqual(success, False)
        self.assertEqual(error_list[0], ERR_MSG_SCHEMA_NONE)

    def test_03_schema_dupe_enum_value(self):
        msgt('3 - Schema with duplicate enum value')
        schema = self.load_json_test_file('astro_bad_01_enum.json')
        success, error_list = validate_schema(schema)
        print error_list
        self.assertEqual(success, False)
        self.assertEqual(error_list[0], u'Error Location: properties->astroType->items')
        self.assertTrue(error_list[1].endswith(\
            'is not valid under any of the given schemas'))

    def test_04_schema_invalid_required_field(self):
        msgt('4 - Schema with invalid required field')
        schema = self.load_json_test_file('astro_bad_02_enum.json')
        success, error_list = validate_schema(schema)
        print error_list
        self.assertEqual(success, False)
        self.assertEqual(error_list[0], u'Error Location: properties->astroFacility->items')
        self.assertTrue(error_list[1].endswith(\
            'is not valid under any of the given schemas'))



    """
    def test_name_is_slugified(self):

        tname = standardize_table_name('hello" there-table')
        self.assertEqual(tname, 'hello_there')

        tname = standardize_table_name('1-2-button-+shoe')
        self.assertEqual(tname, 't_1_2_butto')

    def test_random_chars(self):

        tname = 'mytable'
        for x in range(1, 11):
            random_chars = get_random_chars(x+1)
            new_name = '{0}_{1}'.format(tname, random_chars)
            self.assertEqual(len(new_name), len(tname) + x + 2)
    """
