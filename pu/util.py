import json


def get_base_columns():
    # select the columns you want to keep
    return [
        # Common case-identification variables
        'SSUID', 'PNUM', 'MONTHCODE', 'ERESIDENCEID', 'ERELRPE', 'SPANEL', 'SWAVE',
        # The base weight and monthly in-survey-universe indicator
        'WPFINWGT', 'RIN_UNIV',
        # Common demographics variables, including age at time of interview (TAGE)
        # and monthly age during the reference period (TAGE_EHC)
        'ESEX', 'TAGE', 'TAGE_EHC', 'ERACE', 'EORIGIN', 'EEDUC',
        # Additional variables for analysis
        'TPTOTINC', 'RTANF_MNYN']


def read_schema():
    return json.load(open('data/pu2019_schema.json', 'r'))


def get_translator():
    schema = read_schema()
    lookup = {item['name']: (item['name'], item['label'], item['dtype']) for item in schema}

    def translate(field):
        return lookup[field]

    return translate


def translate_record(translator, record):
    return {translator(k): v for k, v in record.items()}
