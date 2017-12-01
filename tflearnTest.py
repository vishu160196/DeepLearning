import mlp
import numpy as np
from sklearn.preprocessing import StandardScaler

apk_train_data = []
with open('features.txt', 'r') as f:
    for line in f:
        line = line.replace("\n", "")
        line=line.split(',')
        vector = list(map(int, line[:len(line)-1]))
        apk_train_data.append(vector)


apk_test_data = apk_train_data[800:]
apk_train_data = apk_train_data[:800]

apk_train_data = np.array(apk_train_data, dtype=float)
apk_test_data = np.array(apk_test_data, dtype=float)
#
# apk_train_data = np.array([
#     [4, 1, 6, 29, 0, 3711, 1423906, 0],
#     [20, 1, 5, 24, 0, 4082, 501440, 0],
#     [3, 0, 1, 6, 0, 5961, 2426358, 0],
#     [0, 0, 2, 27, 0, 6074, 28762, 0],
#     [12, 1, 3, 17, 0, 4066, 505, 0],
#     [1, 0, 2, 5, 0, 1284, 38504, 0],
#     [2, 0, 2, 10, 0, 2421, 5827165, 0],
#     [5, 0, 17, 97, 0, 25095, 7429, 0],
#     [1, 1, 3, 22, 6, 4539, 9100705, 0],
#     [2, 0, 4, 15, 0, 2054, 264563, 0],
#     [3, 1, 6, 19, 0, 3562, 978171, 0],
#     [8, 0, 5, 12, 3, 1741, 1351990, 0],
#     [9, 0, 5, 12, 2, 1660, 2022743, 0],
#     [9, 0, 5, 12, 2, 1664, 2022743, 0],
#     [10, 4, 11, 70, 8, 43944, 51488321, 1],
#     [6, 0, 3, 18, 0, 8511, 19984102, 1],
#     [11, 2, 6, 44, 0, 61398, 32139, 1],
#     [0, 0, 0, 0, 0, 1008, 23872, 1],
#     [7, 1, 1, 16, 3, 46792, 94818, 1],
#     [3, 2, 1, 13, 2, 8263, 208820, 1],
#     [0, 0, 0, 2, 0, 2749, 3926, 1],
#     [10, 0, 1, 9, 0, 5220, 2275848, 1],
#     [1, 1, 3, 34, 6, 50030, 814322, 1],
#     [2, 2, 4, 48, 7, 86406, 12895, 1],
#     [0, 1, 5, 45, 2, 63060, 803121, 1],
#     [1, 0, 2, 11, 7, 7602, 1557, 1],
#     [3, 0, 1, 15, 3, 20813, 218352, 1]
# ])
# apk_test_data = np.array([
#     [0, 0, 1, 9, 0, 4317, 118082, 0],
#     [8, 0, 5, 12, 3, 1742, 1351990, 0],
#     [8, 0, 5, 12, 3, 1744, 1351990, 0],
#     [0, 0, 1, 11, 2, 17630, 326164, 1],
#     [10, 2, 6, 45, 7, 22668, 30257520, 1],
#     [1, 0, 1, 8, 0, 9317, 33000349, 1],
#     [3, 0, 1, 15, 3, 20813, 218352, 1]
# ])

train_target=apk_train_data[:,7:]
test_target=apk_test_data[:,7:]
merged_data=np.concatenate((apk_train_data,apk_test_data));
# merged_data=(merged_data-np.mean(merged_data))/np.var(merged_data);
# apk_train_data=merged_data[:800]
# apk_test_data=merged_data[800:]

scaler = StandardScaler().fit(merged_data[:,:8])
merged_data=scaler.transform(merged_data)[:,:8]
apk_train_data = merged_data[:800]
apk_test_data = merged_data[800:]

p = mlp.mlp(apk_train_data[:, 0:7], train_target, 19)
p.mlptrain(apk_train_data[:, 0:7], train_target, 0.0001, 100000)
p.confmat(apk_test_data[:, 0:7], test_target)

# anddata = np.array([[0, 0, 0, 0],
#                     [0, 1, 0, 0],
#                     [0, 0, 1, 0],
#                     [0, 1, 1, 0],
#
#                     [1, 0, 1, 0],
#                     [1, 1, 0, 0],
#                     [1, 1, 1, 1]], dtype=float)
# anddata_test = np.array([
#     [1, 0, 0, 0]], dtype=float)
# # xordata = np.array([[0,0,0],[0,1,1],[1,0,1],[1,1,0]])
#
# p = mlp.mlp(anddata[:, 0:3], anddata[:, 3:], 3)
# p.mlptrain(anddata[:, 0:3], anddata[:, 3:], 0.25, 1001)
# p.confmat(anddata_test[:, 0:3], anddata_test[:, 3:])
