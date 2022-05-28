import pandas as pd
from sklearn.preprocessing import StandardScaler
import numpy as np


def parse_csv(file: str):
    df = pd.read_csv(file)
    df.index = df.Country.values
    df.drop('Country',axis = 1, inplace=True)
    return StandardScaler().fit_transform(df.values),df.index.values

def parse_letters(file: str):
    set: np.ndarray = pd.read_csv(file, delim_whitespace=True, header=None).values
    elem_size = len(set[0]) * 5
    set = np.reshape(set, (np.size(set) // elem_size, elem_size))
    return set
