import pandas as pd

config = {
    'encoding': 'utf-8', # CP1252, iso-8859-1
    'separator': ';',
}


def get_dataframe(filepath, converter, config=config):
    return pd.read_csv(filepath, sep=config['separator'], converters=converter, encoding=config['encoding'])
