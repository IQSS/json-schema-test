"""
Some scratch work...
http://guides.dataverse.org/en/4.2/api/native-api.html#datasets
"""
from os.path import isdir, isfile, join
import os
import json
import requests
import time
from collections import OrderedDict
from msg_util import *
from dataverse_creds import DATAVERSE_API_KEY
from metadata_transformer import MetadataTransformer

NATIVE_JSON_FOLDER = 'dataset_native_json'

DOI_PREFIX = 'doi:'
HDL_PREFIX = 'hdl:'

class DataverseClientTest(object):
    """
    Basic look at the the DV API
    """
    def __init__(self, dataverse_server='https://dataverse.harvard.edu'):
        assert dataverse_server is not None, "dataverse_server cannot be None"
        if dataverse_server.endswith('/'):
            dataverse_server = dataverse_server[:-1]

        self.dataverse_server = dataverse_server

    def format_persisent_id(self, persisent_id):
        """
        Make sure the id has a doi: or hdl: prefix
        """
        assert persisent_id is not None, "persisent_id cannot be None"
        if persisent_id.startswith(DOI_PREFIX):
            return persisent_id
        if persisent_id.startswith(HDL_PREFIX):
            return persisent_id

        if persisent_id.count('/') == 2:
            # assume DOI as in doi:10.7910/DVN/26230 (w/o the "doi:")
            return DOI_PREFIX + persisent_id
        elif persisent_id.count('/') == 1:
            # Assume HDL as in hdl:10904/10065 (w/o the "hdl")
            return HDL_PREFIX + persisent_id

        return persisent_id # Try our luck

    def get_metadata_blocks(self, dataset_id, version_id):
        """
        Lists all the metadata blocks and their content, for the given dataset and version:

        GET http://$SERVER/api/datasets/$id/versions/$versionId/metadata?key=$apiKey
        """
        assert dataset_id is not None, "dataset_id cannot be None"
        assert version_id is not None, "version_id cannot be None"

        api_url = '%s/api/datasets/%s/versions/%s/metadata' %\
                    (self.dataverse_server,\
                    dataset_id,\
                    version_id)

        return self.make_get_request(api_url)


    def get_versions_by_id(self, dataset_id):
        """
        GET http://$SERVER/api/datasets/$id/versions?key=$apiKey
        """
        assert dataset_id is not None, "dataset_id cannot be None"

        api_url = '%s/api/datasets/%s/versions' %\
                    (self.dataverse_server,\
                        dataset_id)

        return self.make_get_request(api_url)

    def get_dataset_by_persisent_id(self, persisent_id):
        """
        GET http://$SERVER/api/datasets/:persistentId/?persistentId=doi:10.5072/FK2/J8SJZB
        """
        persisent_id = self.format_persisent_id(persisent_id)

        api_url = '%s/api/datasets/:persistentId?persistentId=%s' %\
                    (self.dataverse_server,\
                        persisent_id)

        return self.make_get_request(api_url)

    def get_dataset_by_id(self, dataset_id):
        """
        Show the dataset whose id is passed:

        GET http://$SERVER/api/datasets/$id
        """
        assert dataset_id is not None, "dataset_id cannot be None"

        api_url = '%s/api/datasets/%s' %\
                    (self.dataverse_server,\
                    dataset_id)

        return self.make_get_request(api_url)

    def make_get_request(self, api_url):
        """
        That key can be passed either via an extra query parameter,
        key, as in ENPOINT?key=API_KEY, or via the HTTP header X-Dataverse-key
        """
        msgt('api_url: %s' % api_url)
        headers = {'X-Dataverse-key' : DATAVERSE_API_KEY}
        r  = requests.get(api_url, headers=headers)

        if r.status_code != 200:
            return 'FAILED: %s' % r.text

        rjson = r.json(object_pairs_hook=OrderedDict)

        return rjson.get('data', None)

def show_info(persisent_id):
    dc = DataverseClientTest()

    dataset_json = dc.get_dataset_by_persisent_id(persisent_id)
    #print dataset_json.keys()
    #return
    print json.dumps(dataset_json, indent=4)
    fname = '%s.json' % str(dataset_json['id']).zfill(7)
    full_fname = join(NATIVE_JSON_FOLDER, fname)
    open(full_fname, 'w').write(json.dumps(dataset_json, indent=4))
    msgt('file written: %s' % full_fname)
    print json.dumps(dataset_json, indent=4)
    return
    #metadata_info_dict = json.loads(citation_test_block,\
    #        object_pairs_hook=OrderedDict)
    metadata_dict = dataset_json.get('latestVersion', {}).get('metadataBlocks')
    mt = MetadataTransformer(metadata_dict)
    print json.dumps(mt.updated_blocks, indent=4)


    return
    """
    ds_id = dataset_json['id']
    ds_version_id = 1#dataset_json['latestVersion']['id']

    print 'ds_id', ds_id
    print 'ds_version_id', ds_version_id
    #print json.dumps(dc.get_versions_by_id(ds_id), indent=4)

    print json.dumps(dc.get_metadata_blocks(ds_id, ds_version_id), indent=4)
    """

def pull_and_save_file(ds_id):

    fname = '%s.json' % str(ds_id).zfill(7)
    full_fname = join(NATIVE_JSON_FOLDER, fname)
    if isfile(full_fname):
        msg('already exists')
        return

    dc = DataverseClientTest()

    dataset_json = dc.get_dataset_by_id(ds_id)
    #print dataset_json.keys()
    #return
    print json.dumps(dataset_json, indent=4)
    open(full_fname, 'w').write(json.dumps(dataset_json, indent=4))
    msgt('file written: %s' % full_fname)

def simplify_metadata_blocks():

    fnames = os.listdir(NATIVE_JSON_FOLDER)
    fnames = [x for x in fnames if x.endswith('.json') and x[:-5].isdigit()]

    for fname in fnames:
        content = open( join(NATIVE_JSON_FOLDER, fname), 'r').read()
        dataset_json = json.loads(content, object_pairs_hook=OrderedDict)
        metadata_dict = dataset_json.get('latestVersion', {}).get('metadataBlocks')
        mt = MetadataTransformer(metadata_dict)
        fname_compact = fname.replace('.json', '_compact.json')
        full_compact_fname = join(NATIVE_JSON_FOLDER, fname_compact)
        open(full_compact_fname, 'w').write(\
                json.dumps(mt.updated_blocks, indent=4))
        msg('file written: %s' % full_compact_fname)


def pull_down_native_json():
    from published_ds_ids import ds_id_list
    cnt = 0
    for ds_id in ds_id_list:
        cnt += 1
        if cnt < 7800:
            continue
        msgt('(%s) Pull published dataset id: %s' % (cnt, ds_id))
        pull_and_save_file(ds_id)
        if cnt % 100 == 0:
            msg('Sleeping')
            time.sleep(2)

"""
# https://pypi.python.org/pypi/jsonschema
from jsonschema import validate

schema = json.loads(s, object_pairs_hook=OrderedDict)
d = json.loads(data, object_pairs_hook=OrderedDict)

validate(d, schema)
"""

if __name__ == '__main__':
    #simplify_metadata_blocks()
    #pull_down_native_json()

    doi = 'doi:10.7910/DVN/TAG25E'
    doi = '10.7910/DVN/28977'
    hdl = 'hdl:10904/10065'
    xdoi = 'doi:10.7910/DVN/26230'
    xdoi = 'doi:10.7910/DVN/IHQAWE'
    doi = 'doi:10.7910/DVN/VB5KKA'
    show_info(doi)
