import pandas as pd
from sklearn.preprocessing import StandardScaler
from pca import pca

def main():

    df = pd.read_csv(r'europe.csv')
    features = ['Area', 'GDP', 'Inflation','Life.expect','Military','Pop.growth','Unemployment']
    x = df.loc[:, features].values
    countries = df.loc[:, ['Country'][0]].values

    scaler = StandardScaler()
    scaler.fit(x)
    x = scaler.transform(x)

    # Or reduce the data towards 2 PCs
    model = pca(n_components=5)

    # Fit transform
    results = model.fit_transform(x,col_labels=features,row_labels=countries)

    # Make biplot with the number of features
    fig, ax = model.biplot()



if __name__ == '__main__':
    main()
