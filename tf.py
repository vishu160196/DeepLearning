import mlp
import numpy as np

i=0
with open('A.txt') as f:
    apk_train_data = [list(map(int, line.split())) for line in f]

apk_train_data=np.array(apk_train_data)
apk_test_data=apk_train_data[800:]
apk_train_data=apk_train_data[:800]


p=mlp.mlp(apk_train_data[:, 0:8], apk_train_data[:, 7:8], 9)
p.mlptrain(apk_train_data[:, 0:8], apk_train_data[:, 7:8], 0.25, 10000)
p.confmat(apk_test_data[:, 0:8], apk_test_data[:, 7:8])
