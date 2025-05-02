import os
import pandas as pd
import logging as log

__logger = log.getLogger('app.utils.file_functions')

def read_csv(path: str):
    try:
        assert(os.path.isfile(path) and str(os.path.basename(path)).endswith('.csv'))
        return pd.read_csv(path, sep=';', index_col=None, encoding='latin-1')
    
    except AssertionError as error:
        __logger.error(f"The path: {path} is not a valid csv to load: {error}")
    except Exception as error:
        __logger.error(f"There was an error trying to load {path}: {error}")
