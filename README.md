# CSVTOJSON

csvtojson will generate [jsonschema][1] from a python
[DictReader][2] instance.


[1]: https://json-schema.org/
[2]: https://docs.python.org/3/library/csv.html#csv.DictReader

## Examples

The schema of the famous Iris dataset.

```python
>>> from csv import DictReader
>>> from pprint import pprint as pp
>>> from csvtojson import jsonschema
>>> d = DictReader(open("iris.csv"))
>>> pp(jsonschema(d))
{'properties': {'petal_length': {'maximum': '1.1',
                                 'minimum': '1.0',
                                 'type': 'number'},
                'petal_width': {'maximum': '0.2',
                                'minimum': '0.1',
                                'type': 'number'},
                'sepal_length': {'maximum': '4.4',
                                 'minimum': '4.3',
                                 'type': 'number'},
                'sepal_width': {'maximum': '2.2',
                                'minimum': '2.0',
                                'type': 'number'},
                'species': {'enum': ['setosa', 'virginica', 'versicolor'],
                            'type': 'string'}},
 'required': ['sepal_length',
              'sepal_width',
              'petal_length',
              'petal_width',
              'species'],
 'type': 'object'}
```
