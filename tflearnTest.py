import mlp
import numpy as np
from sklearn.preprocessing import StandardScaler

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

apk_validation_set = apk_train_data[3::4, :]
apk_test_data = apk_train_data[1::4, :]
apk_train_data = apk_train_data[0::2, :]

train_target = apk_train_data[:, 7:]
validation_target = apk_validation_set[:, 7:]
test_target = apk_test_data[:, 7:]

p = mlp.mlp(apk_train_data[:, 0:7], train_target, 19)
p.early_stop(apk_train_data[:, 0:7], train_target, apk_validation_set[:, 0:7], validation_target, 0.0001)
p.confmat(apk_test_data[:, 0:7], test_target)
