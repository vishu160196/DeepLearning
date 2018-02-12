import apk_image as converter
from sklearn.preprocessing import StandardScaler
import numpy as np
from tabulate import tabulate
import tensorflow as tf

data, labels = converter.convert()

total_apps = labels.shape[0]
start = 100
step = 200
number_of_apps_taken_list = list(range(start, 1701, step))

feature_columns = [str(i) for i in range(153)]
feature_cols = [tf.feature_column.numeric_column(k) for k in feature_columns]

graph = []
scaler_model = StandardScaler()
for index, apps_taken in enumerate(number_of_apps_taken_list):

    fold_size = int(apps_taken / 5)

    acc_sum = 0.0
    model = tf.estimator.DNNClassifier([20,25,20], feature_columns=feature_cols)
    print('number of apps taken {}'.format([apps_taken]))
    for i in range(5):
        train_set = {
            'data': np.concatenate((data[0:i * fold_size, :], data[i * fold_size + fold_size:, :]), axis=0),
            'labels': np.concatenate((labels[0:i * fold_size, :], labels[i * fold_size + fold_size:, :]), axis=0)
        }
        test_set = {
            'data': data[i * fold_size:i * fold_size + fold_size, :],
            'labels': labels[i * fold_size:i * fold_size + fold_size:, :]
        }

        train_images = np.array(train_set['data'], copy=True)
        test_images = np.array(test_set['data'], copy=True)

        scaler_model.fit(train_images)
        scaler_model.transform(train_images)
        scaler_model.transform(test_images)

        feature_dict_train = {str(i): train_images[:, i:i + 1] for i in range(153)}
        feature_dict_test = {str(i): test_images[:, i:i + 1] for i in range(153)}
        train_input_func = tf.estimator.inputs.numpy_input_fn(x=feature_dict_train, y=train_set['labels'],
                                                              num_epochs=None, shuffle=True,
                                                              batch_size=train_images.shape[0])
        eval_input_func = tf.estimator.inputs.numpy_input_fn(x=feature_dict_test, y=test_set['labels'], num_epochs=1,
                                                             shuffle=False, batch_size=test_images.shape[0])
        print('fold number {}'.format(i))
        acc = 0
        # prev_acc = -1
        # while acc >= prev_acc:
        model.train(train_input_func, steps=600)
        results = model.evaluate(eval_input_func)
        # prev_acc = acc
        acc = results['accuracy']
        acc_sum += acc
        print('accuracy is {}'.format(acc))

    average_accuracy = acc_sum / 5
    graph.append([apps_taken, average_accuracy])
    print(graph[index])

graph = np.array(graph)
x = graph[:, :1]
y = graph[:, 1:]
table = tabulate(np.concatenate((x, y), axis=1),
                 headers=['apps_taken', 'average_accuracy'], floatfmt='.3f')
with open('dnn_observations.txt', 'w') as f:
    f.write(table)
