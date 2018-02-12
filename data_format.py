import numpy as np
from sklearn.preprocessing import StandardScaler
import RBF_networks
import matplotlib.pyplot as plt

dataset = []
with open('iris.txt', 'r') as f:
    for line in f:
        line = line.replace("\n", "")
        line = line.split(',')
        l=len(line)
        flower=line[l-1]
        line=line[:l-1]
        if flower=='Iris-setosa':
            line.append(1)
            line.append(0)
            line.append(0)
        elif flower=='Iris-versicolor':
            line.append(0)
            line.append(1)
            line.append(0)
        else:
            line.append(0)
            line.append(0)
            line.append(1)

        vector = list(map(float, line[:len(line)]))

        dataset.append(vector)

dataset = np.array(dataset, dtype=float)
#
scaler = StandardScaler().fit(dataset[:, :4])
dataset[:, :4] = scaler.transform(dataset[:, :4])
#
#
# test = dataset[2799:, :7]
# dataset = dataset[:2799, :]
#
network=RBF_networks.RBF_Network()
#
# benign_dataset=[]
# malign_dataset=[]
# for vector in dataset:
#     if vector[7]==0:
#         benign_dataset.append(vector[:7])
#     else:
#         malign_dataset.append(vector[:7])
#
# benign_dataset=np.array(benign_dataset)
# malign_dataset=np.array(malign_dataset)
# print(benign_dataset.shape)
# print(malign_dataset.shape)
# plt.plot(benign_dataset[2], benign_dataset[6], 'g.')
# plt.plot(malign_dataset[2], malign_dataset[6], 'r.')
# plt.show()
#
#
# malign_centroids=network.k_means(malign_dataset, 2)
# benign_centroids=network.k_means(benign_dataset, 2)
#
#
# for input in dataset[2695:,:]:
#     if input[7]==1:
#         malign_test=input
#         break
#
# for input in dataset[2695:,:]:
#     if input[7] == 0:
#         benign_test = input
#         break
#
# print(malign_test)
# print(benign_test)
# benign_distance=[]
# malign_distance=[]
#
# for centre in benign_centroids:
#     benign_distance.append(np.linalg.norm(benign_test[0]-centre))
#
# for centre in malign_centroids:
#     malign_distance.append(np.linalg.norm(benign_test[0] - centre))
#
# print(np.sum(benign_distance))
# print(np.sum(malign_distance))
#
# benign_distance=[]
# malign_distance=[]
#
# for centre in benign_centroids:
#     benign_distance.append(np.linalg.norm(malign_test[0] - centre))
#
# for centre in malign_centroids:
#     malign_distance.append(np.linalg.norm(malign_test[0] - centre))
#
# print(np.sum(malign_distance))
# print(np.sum(benign_distance))