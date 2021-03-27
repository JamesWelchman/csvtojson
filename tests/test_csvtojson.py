from csv import DictReader

from csvtojson import (
    jsonschema,
    gen_json_records,
)


def test_iris_schema():
    d1 = DictReader(open("iris.csv"))
    d2 = DictReader(open("iris.csv"))

    schema = jsonschema(d1)
    gen = gen_json_records(d2, schema)
    rec1 = {'sepal_length': 5.1,
            'sepal_width': 3.5,
            'petal_length': 1.4,
            'petal_width': 0.2,
            'species': 'setosa',
            }

    assert next(gen) == rec1, "matching first json record"
