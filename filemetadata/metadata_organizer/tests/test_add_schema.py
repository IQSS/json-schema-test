from django.test import TestCase
from metadata_organizer.views_add import add_schema
import json
import collections
from os.path import isfile, isdir, join, realpath, dirname
from proj_utils.msg_util import msg, msgt
from django.test import Client
from django.core.urlresolvers import reverse

TEST_FILE_DIR = join(dirname(realpath(__file__)), 'test_files')

class AddSchemaTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        msg('\n>>> setUpClass AddSchemaTestCase')
        super(AddSchemaTestCase, cls).setUpClass()

        # Verify test directory exists
        assert isdir(TEST_FILE_DIR),\
            "Test file directory not found: %s" % TEST_FILE_DIR

    def load_json_test_file(self, filename):
        """
        Load a file into a JSON object (python OrderedDict)
        """
        full_filename = join(TEST_FILE_DIR, filename)
        assert isfile(full_filename), "Test file not found: %s" % full_filename

        try:
            return json.loads(open(full_filename, 'r').read(),\
                object_pairs_hook=collections.OrderedDict)
        except ValueError as e:
            msg('JSON load error: %s' % e.message)
            msgx('This file is not valid JSON: %s' % full_filename)


    def test_add_good_schema(self):
        msgt('Add a good schema')

        add_schema_url = reverse('add_schema', kwargs={})

        test_client = Client()

        description = 'This is a great schema for testing all types of metadata'
        contributor = 'Dataverse core'

        # -------------------------------------------
        # Load schema
        # -------------------------------------------
        schema_dict = self.load_json_test_file('astro_schema_good_01.json')
        schema_string = json.dumps(schema_dict)

        data_dict = dict(description=description,\
                        contributor=contributor,\
                        schema=schema_string)

        # -------------------------------------------
        # Submit the schema
        # -------------------------------------------
        response = test_client.post(add_schema_url, data_dict)

        json_resp = json.loads(response.content)
        #print json.dumps(json_resp, indent=4)
        msg('status_code: %s' % response.status_code)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(json_resp['success'])
        self.assertEqual(json_resp['data']['self']['version'], 1.0)
        #.status_code, 200)
        #print ('version', json_resp['data']['self']['version'])

        # -------------------------------------------
        # Add the schema again, checking the version increment
        # -------------------------------------------
        msgt('Major version. Add the schema a 2nd time and check the version')
        response2 = test_client.post(add_schema_url, data_dict)
        json_resp2 = json.loads(response2.content)
        self.assertEqual(response2.status_code, 200)
        self.assertTrue(json_resp2['success'])
        self.assertEqual(json_resp2['data']['self']['version'], 2.0)

        # -------------------------------------------
        # Add the schema again, checking the version increment
        # -------------------------------------------
        msgt('Minor version. Add the schema a 3rd time and check the version.')
        data_dict['minor_version'] = True
        response3 = test_client.post(add_schema_url, data_dict)
        json_resp3 = json.loads(response3.content)

        #print ('version', json_resp3['data']['self']['version'])
        self.assertEqual(response3.status_code, 200)
        self.assertTrue(json_resp3['success'])
        self.assertEqual(json_resp3['data']['self']['version'], 2.1)
