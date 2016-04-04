"""
quick scratch work
"""
import json
from msg_util import *
from collections import OrderedDict

MULTIPLE_KEY = 'multiple'
TYPE_NAME_KEY = 'typeName'
TYPE_CLASS_KEY = 'typeClass'
VALUE_KEY = 'value'
COMPOUND_VAL = 'compound'

class MetadataTransformer(object):
    """
    Flatten out Dataverse Metadata returned from the native API
    """
    def __init__(self, dv_metadata_block):
        assert dv_metadata_block is not None, "dv_metadata_block cannot be None"
        self.orig_blocks = dv_metadata_block
        self.updated_blocks = OrderedDict()

        self.format_block()

    def format_block(self):

        block_names = self.orig_blocks.keys()
        for bname in block_names:
            print 'bname', bname
            block_fields = self.orig_blocks[bname].get('fields', [])
            self.updated_blocks[bname] = self.build_fields(block_fields)

    def build_fields(self, block_fields):
        assert block_fields is not None, "block_fields cannot be None"
        # 'block_fields', block_fields
        formatted_fields = OrderedDict()

        for finfo in block_fields:
            msgt('finfo: %s' % json.dumps(finfo, indent=4))
            is_multiple = finfo.get(MULTIPLE_KEY)
            data_type = finfo.get(TYPE_CLASS_KEY)
            #continue
            if is_multiple:
                if data_type == COMPOUND_VAL:
                    formatted_fields.update(self.format_multi_compound_field(finfo))
                elif data_type in ('controlledVocabulary', 'primitive'):
                    """
                    e.g. {"typeName": "subject", "multiple": true, "value": ["Earth and Environmental Sciences", "Demographics"], "typeClass": "controlledVocabulary"}
                    """
                    formatted_fields.update(self.format_single_field(finfo,\
                        force_multiple=True))
            else:
                if data_type in ('primitive',):
                    """
                    e.g. {"typeName": "title", "multiple": false, "value": "shapefile trial", "typeClass": "primitive"}
                    """
                    formatted_fields.update(self.format_single_field(finfo))


        return formatted_fields


    def format_single_field(self, field_dict, force_multiple=True):
        """
        IN: {
                "typeName": "title",
                "multiple": false,
                "value": "shapefile trial",
                "typeClass": "primitive"
            }

        OUT:{
                "title" : "shapefile trial"
            }

            e.g. { typeName val : value val }
        """
        msg('field_dict: %s' % json.dumps(field_dict, indent=4))
        assert field_dict is not None, "field_dict cannot be None"
        if not force_multiple:
            assert field_dict.get(MULTIPLE_KEY, None) is False,\
                "field_dict['%s'] must be False" % MULTIPLE_KEY

        return {field_dict[TYPE_NAME_KEY] : field_dict[VALUE_KEY]}

    def format_multi_compound_field(self, field_dict):
        """
        IN: {
            "typeName": "author",
            "multiple": true,
            "value": [
                {
                    "authorAffiliation": {
                        "typeName": "authorAffiliation",
                        "multiple": false,
                        "value": "Harvard University",
                        "typeClass": "primitive"
                    },
                    "authorName": {
                        "typeName": "authorName",
                        "multiple": false,
                        "value": "Del Ray, Martha",
                        "typeClass": "primitive"
                    }
                }
            ],
            "typeClass": "compound"
        },

        OUT:{
                "authors" : [
                    {
                        "authorName" : "Del Ray, Martha",
                        "authorAffiliation" : "Harvard University"
                    }
                    (etc)
                ]
            }
        """
        assert field_dict is not None, "field_dict cannot be None"
        assert field_dict.get(MULTIPLE_KEY, None) is True,\
            "field_dict['%s'] must be True" % MULTIPLE_KEY
        assert self.is_compound_val(field_dict),\
            'field_dict must contain {"typeClass": "compound"}'

        field_list = []

        # Iterate through the {}'s under the value key
        #
        for single_field in field_dict[VALUE_KEY]:
            # e.g. iterate through each dict with an
            # attribriute for a single author
            single_field_dict = OrderedDict()
            for key, val_dict in single_field.items():
                if self.is_compound_val(val_dict):
                    pass
                else:
                    single_field_dict.update(self.format_single_field(val_dict))
            field_list.append(single_field_dict)

        ordered_dict = OrderedDict()
        ordered_dict[field_dict[TYPE_NAME_KEY]] = field_list
        return ordered_dict
        #return {field_dict[TYPE_NAME_KEY] : field_dict["value"]}


    def is_compound_val(self, field_dict):
        """
        Does this exist in the dict?
            "typeClass": "compound"
        """
        assert field_dict is not None, "field_dict cannot be None"
        if field_dict.get(TYPE_CLASS_KEY, '') == COMPOUND_VAL:
            return True
        return False



def show_test():
    from test_block import citation_test_block

    metadata_info_dict = json.loads(citation_test_block,\
                object_pairs_hook=OrderedDict)
    mt = MetadataTransformer(metadata_info_dict)

    print json.dumps(mt.updated_blocks, indent=4)

if __name__ == '__main__':
    show_test()
