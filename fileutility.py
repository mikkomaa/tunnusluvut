"""Module reads data from a file and cleans it"""

import sys

import pandas as pd


def prepare_data():
    """Return the cleaned data and the units of the variables"""
    df = read_csv('tunnusluvut.csv')
    units = get_units(df)
    df = transpose(df)
    df = change_company_names(df)
    df = split_date(df)
    df = set_column_types(df)
    convert_thousands(df, units)
    df = round_data(df, units)
    return df, units


def read_csv(filename):
    """Read data from a csv file and return it as a dataframe"""
    try:
        return pd.read_csv(filename, sep=',')
    except OSError as e:
        print(e, file=sys.stderr)
        raise SystemExit


def get_units(df):
    """Return the units of the variables in the dataframe as a dictionary"""
    units = {}
    for i, name in enumerate(df['Tunnusluku']):
        units[name] = df.loc[i, 'Yksikkö']
    return units


def transpose(df):
    """Transpose the data for more natural handling"""
    df = df.drop(columns=['Yksikkö'])
    df = df.T
    df.columns = df.iloc[0]
    df = df.drop('Tunnusluku', axis=0)
    return df


def change_company_names(df):
    """Change LähiTapiola and Tapiola into Elo"""
    m = (df['Yhtiö'] == 'LähiTapiola') | (df['Yhtiö'] == 'Tapiola')
    df.loc[m, 'Yhtiö'] = 'Elo'
    return df


def split_date(df):
    """Split the date column into month, day, and year columns"""
    d = df['Päivämäärä'].str.split(pat='/', expand=True)
    d.columns = ['Kuukausi', 'Päivä', 'Vuosi']
    d = d.astype({'Kuukausi': int, 'Päivä': int, 'Vuosi': int})
    d['Vuosi'] += 2000
    df = pd.concat([d, df], axis=1)
    df = df.drop('Päivämäärä', axis=1)
    return df


def set_column_types(df):
    """Set the index and column types"""
    df.index = df.index.astype(int)
    df = df.apply(pd.to_numeric, errors='ignore')
    return df


def convert_thousands(df, units):
    """Convert the variables with the unit 'teur'"""
    for col_name, unit in units.items():
        if unit == 'teur':
            df[col_name] *= 1000
            units[col_name] = 'euroa'


def round_data(df, units):
    """Round the data for graphs"""
    for col_name, unit in units.items():
        if unit == 'euroa':
            df[col_name] = df[col_name].round(0)
        elif unit == '%':
            df[col_name] = df[col_name].round(2)
    return df


# For testing and debugging
def main():
    df, units = prepare_data()
    for i, luku in enumerate(df.columns):
        print(i, luku)


if __name__ == "__main__":
    main()
