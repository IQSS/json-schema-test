# schema-test

quick test. A mix of:
  - JSON schema editor from Jeremy Dorn
    - repository: https://github.com/jdorn/json-editor
    - example: http://jeremydorn.com/json-editor/
  - TSVs from Dataverse
    - https://github.com/IQSS/dataverse/tree/develop/scripts/api/data/metadatablocks

```
mkvirtualenv schema-test
pip install -r requirements.txt
cd filemetadata/    # should have the manage.py file inside
#
python manage.py check  # ignore deprecations for now
python manage.py runserver # to run a differnt port, e.g. 8070; python manage.py runserver 8070
```

- open http://127.0.0.1:8000/tsv-files/
- click the links to create JSON schemas and view them in editor

You should see something like:

![file listing](https://raw.githubusercontent.com/iqss/json-schema-test/master/screenshots/tsv-file-list.png)
![JSON schema editor J. Dorn](https://raw.githubusercontent.com/iqss/json-schema-test/master/screenshots/schema-editor.png)

### Caveat

Not all of the TSV features are translated over.
This is proof of concept and J. Dorn's editor has not been modified for these examples.
