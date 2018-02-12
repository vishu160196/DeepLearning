import numpy as np
import pandas as pd


def convert(label_encoding=None):
    data_file = pd.read_csv('combined_features.txt')
    data_file = data_file.as_matrix()[:, 1:]
    data = data_file[:, :153]
    labels = np.array(data_file[:, 153:],dtype=float)

    if label_encoding == 'one-hot-encoded':
        one_hot_encoded = []
        for label in labels:
            if label[0] == 0.:
                one_hot_encoded.append([1.0, 0.0])
            else:
                one_hot_encoded.append([0.0, 1.0])
        labels = np.array(one_hot_encoded,dtype=float)

    combined = np.concatenate((data, labels), axis=1)
    np.random.shuffle(combined)
    data = combined[:, :153]
    labels = combined[:, 153:]

    return data, labels
