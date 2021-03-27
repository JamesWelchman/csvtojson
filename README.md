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
{'properties': {'petal_length': {'maximum': 6.9,
                                 'minimum': 1.0,
                                 'type': 'number'},
                'petal_width': {'maximum': 2.5,
                                'minimum': 0.1,
                                'type': 'number'},
                'sepal_length': {'maximum': 7.9,
                                 'minimum': 4.3,
                                 'type': 'number'},
                'sepal_width': {'maximum': 4.4,
                                'minimum': 2.0,
                                'type': 'number'},
                'species': {'enum': ['setosa', 'versicolor', 'virginica'],
                            'type': 'string'}},
 'required': ['sepal_length',
              'sepal_width',
              'petal_length',
              'petal_width',
              'species'],
 'type': 'object'}
```

### Example Titanic Dataset

We not for this example:

	- if the number of strings is large then we don't treat it as an enum
	- if there are missing values in the columns we don't add it
	to our set of required keys

```python
>>> from csv import DictReader
>>> from csvtojson import jsonschema
>>> from pprint import pprint as pp
>>> d = DictReader(open("titanic.csv"))
>>> pp(jsonschema(d))
{'properties': {'age': {'maximum': 80.0, 'minimum': 0.1667, 'type': 'number'},
                'boat': {'maxLength': 7, 'minLength': 1, 'type': 'string'},
                'body': {'maximum': 328.0, 'minimum': 4.0, 'type': 'number'},
                'cabin': {'maxLength': 15, 'minLength': 1, 'type': 'string'},
                'embarked': {'enum': ['C', 'S', 'Q'], 'type': 'string'},
                'fare': {'maximum': 512.3292, 'minimum': 0.0, 'type': 'number'},
                'home.dest': {'maxLength': 50,
                              'minLength': 5,
                              'type': 'string'},
                'name': {'maxLength': 82, 'minLength': 12, 'type': 'string'},
                'parch': {'maximum': 9.0, 'minimum': 0.0, 'type': 'number'},
                'passenger_id': {'maximum': 1307.0,
                                 'minimum': 1.0,
                                 'type': 'number'},
                'pclass': {'maximum': 3.0, 'minimum': 1.0, 'type': 'number'},
                'sex': {'enum': ['male', 'female'], 'type': 'string'},
                'sibsp': {'maximum': 8.0, 'minimum': 0.0, 'type': 'number'},
                'survived': {'enum': [0.0, 1.0], 'type': 'number'},
                'ticket': {'maxLength': 18, 'minLength': 3, 'type': 'string'}},
 'required': ['passenger_id',
              'pclass',
              'name',
              'sex',
              'sibsp',
              'parch',
              'ticket',
              'survived'],
 'type': 'object'}
```