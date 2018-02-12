import mlp
import numpy as np
import matplotlib.pyplot as plt
from tabulate import tabulate


class mlp_k_fold:
    def k_fold_cross_validation(self, inputs, targets, early_stop_test, early_stop_test_target, num_folds, eta):
        n = np.shape(inputs)[0]
        size_list = range(100, n, num_folds)
        average_accuracy_list = []

        for size in size_list:
            indices = range(0, size, int(size / num_folds))
            accuracy_list = []

            mlp_helper = mlp.mlp(7, int(size / num_folds) * (num_folds - 1), 1, 19)
            for i in indices:
                validation_set = inputs[i:i + int(size / num_folds), :]
                validation_targets = targets[i:i + int(size / num_folds), :]

                train_set = np.concatenate((inputs[:i, :], inputs[i + int(size / num_folds):size, :]))
                train_targets = np.concatenate((targets[:i, :], targets[i + int(size / num_folds):size, :]))

                accuracy_list.append(float(
                    self.early_stop(train_set, train_targets, validation_set, validation_targets, eta, mlp_helper,
                                    early_stop_test, early_stop_test_target)))

            average_accuracy_list.append(np.mean(accuracy_list))
            print(average_accuracy_list)

        plt.plot(size_list, average_accuracy_list, 'g^')
        plt.axis([size_list[0], size_list[len(size_list) - 1], 0, 100])
        plt.show()

        size_list = np.transpose(np.array(list([size_list])))
        average_accuracy_list = np.transpose(np.array(list([average_accuracy_list])))

        table = tabulate(np.concatenate((size_list, average_accuracy_list), axis=1),
                         headers=['apps taken', 'average accuracy(%)'], floatfmt='.3f')

        with open('k_fold_X_validation_observations.txt', 'w') as f:
            f.write(table)

    def early_stop(self, train_set, train_target, validation_set, validation_target, eta, mlp_helper, early_stop_test,
                   early_stop_test_target):

        """ initialise first error """
        validation_set = np.concatenate((validation_set, -np.ones((np.shape(validation_set)[0], 1))), axis=1)
        mlp_helper.mlptrain(train_set, train_target, eta, 100)
        test_out = mlp_helper.mlpfwd(validation_set)
        error1 = 0.5 * (np.sum(test_out - validation_target) ** 2)

        """ initialise second error """
        mlp_helper.mlptrain(train_set, train_target, eta, 100)
        test_out = mlp_helper.mlpfwd(validation_set)
        error2 = 0.5 * (np.sum(test_out - validation_target) ** 2)

        while error2 < error1:
            mlp_helper.mlptrain(train_set, train_target, eta, 100)
            error1 = error2
            test_out = mlp_helper.mlpfwd(validation_set)
            error2 = 0.5 * (np.sum(test_out - validation_target) ** 2)

        # Add the inputs that match the bias node
        early_stop_test = np.concatenate((early_stop_test, -np.ones((np.shape(early_stop_test)[0], 1))), axis=1)
        test_out = mlp_helper.mlpfwd(early_stop_test)
        nclasses = 2

        test_out = np.where(test_out > 0.5, 1, 0)

        cm = np.zeros((nclasses, nclasses))
        for i in range(nclasses):
            for j in range(nclasses):
                cm[i, j] = np.sum(np.where(test_out == j, 1, 0) * np.where(early_stop_test_target == i, 1, 0))

        print(cm)
        return np.trace(cm) / np.sum(cm) * 100
