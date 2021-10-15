import json
from brunodb import DBase
from pu.util import get_base_columns, read_schema
from pu.read_file import read as stream_all


def get_db():
    config = {'db_type': 'sqlite', 'filename': 'data/database.db'}
    dbase = DBase(config)
    return dbase


def get_columns():
    base_columns = get_base_columns()
    extra_columns = []
    return base_columns + extra_columns


def get_schema():
    raw_schema = read_schema()
    schema = {}
    assert len(raw_schema) > 0

    columns = get_columns()

    for item in raw_schema:
        field_name = item['name']
        field_type = item['dtype']

        if field_type == 'string':
            schema_type = 'TEXT'
        elif field_type == 'float':
            schema_type = 'REAL'
        elif field_type == 'integer':
            schema_type = 'REAL'
        else:
            raise ValueError('Unknown field type: %d' % field_type)

        if field_name in columns:
            schema[field_name] = schema_type

    return schema


def get_structure():
    indices = get_base_columns()
    # add any more indices?

    extra_indices = []
    indices += extra_indices

    return {'table_name': 'pu',
            'schema': get_schema(),
            'indices': indices}


def stream_data(n_max=1000):
    columns = get_columns()
    for row_num, row in enumerate(stream_all()):
        if n_max and row_num >= n_max:
            return

        new_row = {k: v for k, v in row.items() if k in columns}

        yield new_row


def load_table(block=False, n_max=1000):
    dbase = get_db()
    stream = stream_data(n_max=n_max)
    structure = get_structure()
    dbase.create_and_load_table(stream, structure, block=block)
    dbase.close()
