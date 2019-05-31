import numpy as np
import pandas as pd
import datetime as dt

def to_categorical(df, cols):
    '''
    Converts specified columns to categorical type
    
    ARGS:
        df - dataframe
        cols = list of column names
    RETURN
        df
    ''' 
    for c in cols:
        df[c] = df[c].astype("category")
    return df
    
    
def to_numeric(df, cols):
    '''
    Converts specified columns to numeric type
    
    ARGS:
        df - dataframe
        cols = list of column names
    RETURN
        df
    '''
    for c in cols:
        df[c] = df[c].apply(lambda x: pd.to_numeric(x, errors='coerce'))
    return df

def to_datetime(df,col, start, end):
    '''
    Converts 'col' to datetime within range start<->end
    Adds new new columns for 'hour','day'(of month), 'day'(of week), and month.
    
    ARGS:
        df - dataframe
        cols = str
        start = str (formate "YYYY-MM-DD")
        end = str (formate "YYYY-MM-DD")
    RETURN
        df
    '''
    df[col] = pd.to_datetime(df[col])
    time_range_filter = (df['DATE'] > start) & (df['DATE'] < end)
    df = df[time_range_filter].copy()
    df['month'] = df['DATE'].apply(lambda x: x.month)
    df['day'] = df['DATE'].apply(lambda x: x.day)
    df['hour'] = df['DATE'].apply(lambda x: x.hour)
    df['w_day'] = df['DATE'].apply(lambda x: int(x.strftime('%w')))
    return df

def select_cols(df, cols):
    '''
    Returns df with specified columns
    
    ARGS:
        df - pd.dataFrame
        cols - list of columns
    '''
    columns_to_drop = []
    for x in df.columns:
        if x not in columns_to_keep:
            columns_to_drop.append(x)
    df.drop(columns_to_drop, inplace=True, axis=1)
    return df

def save(df):
    df.to_pickle('data/pickled_df')
    
if __name__ == '__main__':
    df = pd.read_csv('data/dentraffic_accidents.csv',dtype=str)
    df['DATE'] = df['FIRST_OCCURRENCE_DATE']

    start, end = '2013-01-01', '2019-01-01'
    numeric_cols=['GEO_LON','GEO_LAT','BICYCLE_IND','PEDESTRIAN_IND',
                  'SERIOUSLY_INJURED','FATALITIES']
    cat_cols = ['ROAD_CONDITION', 'TU1_DRIVER_ACTION','TU1_DRIVER_HUMANCONTRIBFACTOR']
    columns_to_keep = ['DATE', 'GEO_LON', 'GEO_LAT','INCIDENT_ADDRESS', 'BICYCLE_IND',
        'PEDESTRIAN_IND','ROAD_LOCATION', 'ROAD_DESCRIPTION', 'ROAD_CONDITION',
        'LIGHT_CONDITION', 'SERIOUSLY_INJURED', 'FATALITIES','FATALITY_MODE_1',
        'FATALITY_MODE_2', 'SERIOUSLY_INJURED_MODE_1','SERIOUSLY_INJURED_MODE_2',
        'TU1_DRIVER_ACTION','TU1_DRIVER_HUMANCONTRIBFACTOR']
    
    df = select_cols(df, columns_to_keep)
    df = to_numeric(df,numeric_cols)
    df = to_datetime(df, 'DATE', start, end)
    df = to_categorical(df,cat_cols)
    save(df)
    print(df.columns)
    

 
