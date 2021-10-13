from pu.read_pandas import get_dtype

def test_get_dtype():
    assert get_dtype('integer') == 'Int64'
    assert get_dtype('float') == 'Float64'
    assert get_dtype('string') == 'object'
