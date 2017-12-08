import mlp
import numpy as np
import matplotlib.pyplot as plt
from tabulate import tabulate

class mlp_k_fold:

    def k_fold_cross_validation(self, inputs, targets, early_stop_test, early_stop_test_target, step_size, eta):
        n = np.shape(inputs)[0]
        size_list = range(step_size, int(n/2), step_size)
        average_accuracy_list = []

        for size in size_list:
            indices = []
            k = int(n / size)
            for i in range(k):
                indices.append(i * size)
            accuracy_list = []

            mlp_helper = mlp.mlp(7, size*(k-1), 1, 19)
            for i in indices:
                test_set = inputs[i:i + size, :]
                test_targets = targets[i:i + size, :]

                train_set = np.concatenate((inputs[:i, :], inputs[i + size:k*size, :]))
                train_targets = np.concatenate((targets[:i, :], targets[i + size:k*size, :]))

                accuracy_list.append(float(self.early_stop(train_set, train_targets, test_set, test_targets, eta, mlp_helper, early_stop_test, early_stop_test_target)))


            average_accuracy_list.append(np.mean(accuracy_list))
            print(average_accuracy_list)

        plt.plot(size_list, average_accuracy_list, 'g^')
        plt.axis([size_list[0], int(n/2), 0, 100])
        plt.show()

        size_list = np.transpose(np.array(list([size_list])))
        average_accuracy_list=np.transpose(np.array(list([average_accuracy_list])))

        table=tabulate(np.concatenate((size_list, average_accuracy_list), axis=1), headers=['batch_size', 'average accuracy(%)'], floatfmt='.3f')

        with open('k_fold_X_validation_observations.txt', 'w') as f:
            f.write(table)


    def early_stop(self, train_set, train_target, test_set, test_target, eta, mlp_helper, early_stop_test, early_stop_test_target):

        """ initialise first error """
        test_set = np.concatenate((test_set, -np.ones((np.shape(test_set)[0], 1))), axis=1)
        mlp_helper.mlptrain(train_set, train_target, eta, 100)
        test_out = mlp_helper.mlpfwd(test_set)
        error1 = 0.5 * (np.sum(test_out - test_target) ** 2)

        """ initialise second error """
        mlp_helper.mlptrain(train_set, train_target, eta, 100)
        test_out = mlp_helper.mlpfwd(test_set)
        error2 = 0.5 * (np.sum(test_out - test_target) ** 2)

        while error2 < error1:
            mlp_helper.mlptrain(train_set, train_target, eta, 100)
            error1 = error2
            test_out = mlp_helper.mlpfwd(test_set)
            error2 = 0.5 * (np.sum(test_out - test_target) ** 2)

        # Add the inputs that match the bias node
        #test_set = np.concatenate((test_set, -np.ones((np.shape(test_set)[0], 1))), axis=1)
        early_stop_test = np.concatenate((early_stop_test, -np.ones((np.shape(early_stop_test)[0], 1))), axis=1)
        test_out = mlp_helper.mlpfwd(early_stop_test)
        nclasses = np.shape(early_stop_test_target)[1]

        if nclasses == 1:
            nclasses = 2
            test_out = np.where(test_out > 0.5, 1, 0)
        else:
            # 1-of-N encoding
            outputs = np.argmax(test_out, 1)
            targets = np.argmax(test_target, 1)

        cm = np.zeros((nclasses, nclasses))
        for i in range(nclasses):
            for j in range(nclasses):
                cm[i, j] = np.sum(np.where(test_out == j, 1, 0) * np.where(early_stop_test_target == i, 1, 0))

        print(cm)
        return np.trace(cm) / np.sum(cm) * 100
