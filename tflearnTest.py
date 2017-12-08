import numpy as np
from sklearn.preprocessing import StandardScaler
import mlp_k_fold_X_validation

dataset = []
with open('features.txt', 'r') as f:
    for line in f:
        line = line.replace("\n", "")
        line = line.split(',')
        vector = list(map(int, line[:len(line) - 1]))
        dataset.append(vector)

dataset = np.array(dataset, dtype=float)

scaler = StandardScaler().fit(dataset[:, :7])
dataset[:, :7] = scaler.transform(dataset[:, :7])

targets = dataset[:, 7:]
dataset = dataset[:, :7]

order = np.arange(np.shape(dataset)[0])
np.random.shuffle(order)

dataset = dataset[order, :]
targets = targets[order, :]

early_stop_test = dataset[2799:,:]
early_stop_test_targets = targets[2799:,:]

dataset=dataset[:2799,:]
targets=targets[:2799,:]

mlp_k_fold = mlp_k_fold_X_validation.mlp_k_fold()
mlp_k_fold.k_fold_cross_validation(dataset, targets, early_stop_test, early_stop_test_targets, 50, 0.0001)

# apk_validation_set = apk_train_data[3::4, :]
# apk_test_data = apk_train_data[1::4, :]
# apk_train_data = apk_train_data[0::2, :]
#
# train_target = apk_train_data[:, 7:]
# validation_target = apk_validation_set[:, 7:]
# test_target = apk_test_data[:, 7:]
