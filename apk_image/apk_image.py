import numpy as np


def convert():
    b = []

    with open('new_feature_benign.txt') as f:
        a = f.readlines()

    for line in a:
        b.append(line.split(',')[:147])

    with open('new_feature_malign.txt') as f:
        a = f.readlines()

    for line in a:
        b.append(line.split(',')[:147])

    images = np.array(b, dtype=float)
    x = images[:, :144] # data
    y = images[:, 146:] # label
    one_hot_encoded = np.ndarray(shape=(y.shape[0], 2))
    y=np.reshape(y, newshape=-1)


    for i,label in enumerate(y):
        if label == 0.:
            one_hot_encoded[i,0]=1
            one_hot_encoded[i, 1] = 0
        else:
            one_hot_encoded[i,0]= 0
            one_hot_encoded[i, 1] = 1


    images = np.concatenate((x, one_hot_encoded), axis=1)
    np.random.shuffle(images)
    data=images[:1700, :144]
    labels=images[:1700, 144:]

    return data, labels