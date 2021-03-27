from csv import DictReader


__all__ = ["jsonschema"]


class SchemaReader:
    def __init__(self, column_labels):
        self.column_labels = column_labels

        # We need one set per column_labels
        # to determine how many values we have
        self._unique_value_sets = {
            k: set() for k in column_labels
        }

        # We need to check if we found any empty values
        self._empty_value_counts = {
            k: 0 for k in column_labels
        }

        # We need to check if every non-empty value
        # is a valid float
        self._is_valid_float = {
            k: True for k in column_labels
        }

    def process_row(self, row):
        for k in self.column_labels:
            val = row[k]
            # Is it empty?
            if val is None or val == "":
                self._empty_value_counts[k] += 1
                continue

            # Is it a valid float?
            try:
                float(val)
            except ValueError:
                # It's not valid
                self._is_valid_float[k] = False

            self._unique_value_sets[k].add(val)

    def _add_numeric_data(self, column_schema, k):
        # If we only have two valid values
        # then we'll call it an enum
        if len(self._unique_value_sets[k]) <= 2:
            enum = list(map(float, self._unique_value_sets[k]))
            column_schema['enum'] = enum
            return

        # Okay we're not calling it an enum
        # We instead compute maximum and minimum values
        values = list(self._unique_value_sets[k])
        values.sort()
        column_schema["minimum"] = values[0]
        column_schema['maximum'] = values[1]

    def _add_string_data(self, column_schema, k):
        # If we have fewer than 8 strings
        # then we'll call it an enum, otherwise
        # it's an arbitary string. We also want
        # minimum and maximum length information.
        if len(self._unique_value_sets[k]) <= 8:
            enum = list(self._unique_value_sets[k])
            column_schema['enum'] = enum
            return

        # It's an arbitary string
        min_length = -1
        max_length = -1
        for s in self._unique_value_sets[k]:
            if len(s) > max_length:
                max_length = len(s)
            if min_length == -1 or len(s) < min_length:
                min_length = len(s)

        column_schema["minLength"] = min_length
        column_schema["maxLength"] = max_length

    def jsonschema(self):
        schema = {
            "type": "object",
            "properties": {},
        }

        for k in self.column_labels:
            column_schema = {}
            # Is it a valid number?
            if self._is_valid_float[k]:
                column_schema["type"] = "number"
                self._add_numeric_data(column_schema, k)
            else:
                column_schema["type"] = "string"
                self._add_string_data(column_schema, k)

            schema["properties"][k] = column_schema

        # fields are required if they are not empty
        required = []
        for k in self.column_labels:
            if self._empty_value_counts[k] == 0:
                required.append(k)

        schema['required'] = required

        return schema


def jsonschema(dict_reader):
    """
    dict_reader is a python
    """

    if not isinstance(dict_reader, DictReader):
        s = "jsonschema must be passed a DictReader instance"
        raise TypeError(s)

    iterator = iter(dict_reader)
    try:
        row1 = next(iterator)
    except StopIteration:
        # There is no data - it is empty
        # can't generate schema data
        raise ValueError("empty DictReader instance")

    column_labels = list(row1)
    reader = SchemaReader(column_labels)
    reader.process_row(row1)
    for row in iterator:
        reader.process_row(row)

    return reader.jsonschema()
