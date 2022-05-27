import pandas as pd
from sklearn.preprocessing import StandardScaler


def parse_csv(file: str):
    df = pd.read_csv(file)
    df.index = df.Country.values
    df.drop('Country',axis = 1, inplace=True)
    return StandardScaler().fit_transform(df.values)