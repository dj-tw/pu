"""
The following code is an example of reading the pipe-delimited Survey of Income and Program Participation (SIPP)
data into an Pandas dataframe in preparation for analysis. Specifically, this code loads in both the primary data file
and the calendar-year replicate weights file (as opposed to the longitudinal replicate weights). These files are
separate downloads on the SIPP website.
SIPP data are in person-month format, meaning each record represents one month for a specific person.
Unique persons are identified using SSUID+PNUM. Unique households are identified using SSUID+ERESIDENCEID. For
additional guidance on using SIPP data, please see the SIPP Users'
Guide at <https://www.census.gov/programs-surveys/sipp/guidance/users-guide.html>
This code was written in Python 3, and requires version 0.24 or higher of the Pandas module.
Note the use of 'usecols' in the first pd.read_csv statement. Most machines do not have enough memory to read
the entire SIPP file into memory. Use 'usecols' to read in only the columns you are interested in. If you
still encounter an out-of-memory error, either select less columns, or consider using the Dask module.
Run this code in the same directory as the data.
This code was written by Adam Smith. Please contact census.sipp@census.gov if you have any questions.
Refactored by David Johnston, dajohnst@thoughtworks.com
"""

# Import the pandas module. This code requires version 0.24 or higher
# in order to use the Int64 and Float64 data types, which allow for
# missing values

from pu.util import get_base_columns
import pandas as pd


def get_dtype(dtype):
    if dtype == 'integer':
        return 'Int64'
    elif dtype == 'string':
        return 'object'
    elif dtype == 'float':
        return 'Float64'
    else:
        raise ValueError('Unknown dtype: %s' % dtype)


def get_rd_schema():
    # Read in the primary data file schema to get data-type information for
    # each variable.
    rd_schema = pd.read_json('data/pu2019_schema.json')
    rd_schema['dtype'] = [get_dtype(s) for s in rd_schema['dtype']]
    return rd_schema


def get_rw_schema():
    # Read in the replicate weight data file schema to get data-type information
    # for each variable.
    rw_schema = pd.read_json('data/rw2019_schema.json')
    rw_schema['dtype'] = [get_dtype(s) for s in rw_schema['dtype']]
    return rw_schema


def get_extra_columns():
    # get the extra columns, beyond base columns
    return []


def get_columns():
    columns = get_base_columns()
    extra = get_extra_columns()
    return columns + extra


def read_data(small=False, write_csv=False):
    rd_schema = get_rd_schema()
    rw_schema = get_rw_schema()
    filename_whole = 'data/pu2019.csv'
    filename_small = 'data/pu2019_small.csv'
    if small:
        filename = filename_small
    else:
        filename = filename_whole

    print('reading file: %s' % filename)

    columns = get_columns()

    print('reading data')
    df_data = pd.read_csv(filename, names=rd_schema['name'],
                          dtype=dict([(i, v) for i, v in zip(rd_schema['name'], rd_schema['dtype'])]),
                          sep='|',
                          header=0,
                          usecols=columns)
    # preview the data
    print(df_data.head())

    print("N_rows total: %s" % len(df_data))

    # check some means against the validation xls file to help ensure that the data
    # were read in correctly. Note that the validation xls files do not include all variables
    print('TPTOTINC mean:' + str(df_data.TPTOTINC.mean()))

    # Read in the replicate-weight data. This dataset is small enough that most machines
    # can read the whole file into memory
    print('reading weights')
    rw_file = 'data/rw2019.csv'
    df_rw = pd.read_csv(rw_file,
                        dtype=dict([(i, v) for i, v in zip(rw_schema['name'], rw_schema['dtype'])]),
                        sep='|',
                        header=0,
                        names=rw_schema['name'])
    # preview the data
    print(df_rw.head())

    # check these estimates against the validation xls file to help ensure that the data
    # were read in correctly. Note that the validation xls files do not include all variables
    print('REPWT100 mean:' + str(df_rw.REPWGT100.mean()))

    # Merge data and replicate weights on SSUID, PNUM, MONTHCODE
    df = df_data.merge(df_rw, left_on=['SSUID', 'PNUM', 'MONTHCODE'],
                       right_on=['SSUID', 'PNUM', 'MONTHCODE'])

    # preview the merged data
    print(df.head())

    if write_csv:
        csv_filename = 'data/merged.csv'
        write_csv_file(df, csv_filename)
    return df


def write_csv_file(df, filename):
    df.to_csv(filename, index=False)
