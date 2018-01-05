import apk_image as converter
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from image_classifier import LenetClassifier
from tabulate import tabulate


data, labels = converter.convert()

total_apps=labels.shape[0]
start=50
step=100
number_of_apps_taken_list=list(range(start, 1701, step))

graph=[]
for index,apps_taken in enumerate(number_of_apps_taken_list):

    fold_size=int(apps_taken/5)

    acc_sum=0.0
    classifier = LenetClassifier()
    for i in range(5):
        train_set = {
            'data': np.concatenate((data[0:i,:], data[i+fold_size:, :]), axis=0),
            'labels': np.concatenate((labels[0:i,:], labels[i+fold_size:, :]), axis=0)
        }
        test_set = {
            'data': data[i:i+fold_size, :],
            'labels': labels[i:i+fold_size:, :]
        }
        train_images=np.array(train_set['data'], copy=True)
        test_images=np.array(test_set['data'], copy=True)
        scaler_model = MinMaxScaler()
        scaler_model.fit(train_images)
        scaler_model.transform(train_images)
        scaler_model.transform(test_images)
        train_images=np.reshape(train_images, newshape=(-1,12,12,1))
        test_images=np.reshape(test_images, newshape=(-1,12,12,1))
        classifier.set_data(train_images, train_set['labels'], test_images, test_set['labels'])
        acc_sum+=classifier.train_model()

    average_accuracy=acc_sum/5
    graph.append([apps_taken, average_accuracy])
    print(graph[index])

graph=np.array(graph)
x=graph[:,:1]
y=graph[:,1:]
table = tabulate(np.concatenate((x, y), axis=1),
                         headers=['apps_taken', 'average_accuracy'], floatfmt='.3f')
with open('lenet_observations.txt', 'w') as f:
    f.write(table)