import numpy as np
from sklearn.preprocessing import StandardScaler
import mlp_two_hidden_layer

apk_train_data = []
with open('features.txt', 'r') as f:
    for line in f:
        line = line.replace("\n", "")
        line = line.split(',')
        vector = list(map(int, line[:len(line) - 1]))
        apk_train_data.append(vector)

apk_train_data = np.array(apk_train_data, dtype=float)

scaler = StandardScaler().fit(apk_train_data[:, :7])
apk_train_data[:, :7] = scaler.transform(apk_train_data[:, :7])

apk_targets = apk_train_data[:, 7:]
apk_train_data = apk_train_data[:, :7]

order = np.arange(np.shape(apk_train_data)[0])
np.random.shuffle(order)

apk_train_data = apk_train_data[order, :]
apk_targets = apk_targets[order, :7]

apk_validation_set = apk_train_data[3::4, :]
apk_test_data = apk_train_data[1::4, :]
apk_train_data = apk_train_data[0::2, :]

train_target = apk_targets[0::2, :]
validation_target = apk_targets[3::4, :]
test_target = apk_targets[1::4, :]

mlp = mlp_two_hidden_layer.mlp_two_hidden_layers(7, np.shape(apk_train_data)[0], 1)
mlp.early_stop(apk_train_data, train_target, apk_validation_set, validation_target, 0.0001)
mlp.confmat(apk_test_data, test_target)
