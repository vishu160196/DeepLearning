import numpy as np
import mlp

class mlp_two_hidden_layers:

    def __init__(self, inputs, targets, nhidden1, nhidden2, beta=1, momentum=0.9, outtype='logistic'):
        """ Constructor """
        # Set up network size
        self.nin = np.shape(inputs)[1]
        self.nout = np.shape(targets)[1]
        self.ndata = np.shape(inputs)[0]
        self.nhidden1 = nhidden1
        self.nhidden2 = nhidden2

        self.beta = beta
        self.momentum = momentum
        self.outtype = outtype

        # Initialise network
        self.weights1 = (np.random.rand(self.nin + 1, self.nhidden1) - 0.5) * 2 / np.sqrt(self.nin + 1)
        self.weights2 = (np.random.rand(self.nhidden1 + 1, self.nhidden2) - 0.5) * 2 / np.sqrt(self.nhidden1 + 1)
        self.weights3 = (np.random.rand(self.nhidden2 + 1, self.nout) - 0.5) * 2 / np.sqrt(self.nhidden2 + 1)

    def mlptrain(self, inputs, targets, eta, niterations):
        """ Train the thing """
        # Add the inputs that match the bias node
        inputs = np.concatenate((inputs, -np.ones((self.ndata, 1))), axis=1)

        updatew1 = np.zeros((np.shape(self.weights1)))
        updatew2 = np.zeros((np.shape(self.weights2)))
        updatew3 = np.zeros((np.shape(self.weights3)))

        for n in range(niterations):

            self.outputs = self.mlpfwd(inputs)

            error = 0.5 * np.sum((self.outputs - targets) ** 2)
            if (np.mod(n, 100) == 0):
                print("Iteration: ", n, " error: ", error)


                # Different types of output neurons
            if self.outtype == 'linear':
                deltao = (self.outputs - targets) / self.ndata
            elif self.outtype == 'logistic':
                deltao = self.beta * (self.outputs - targets) * self.outputs * (1.0 - self.outputs)
            elif self.outtype == 'softmax':
                deltao = (self.outputs - targets) * (self.outputs * (-self.outputs) + self.outputs) / self.ndata
            else:
                print("error")

            deltah2 = self.hidden2 * self.beta * (1.0 - self.hidden2) * (np.dot(deltao, np.transpose(self.weights3)))
            deltah1 = self.hidden1 * self.beta * (1.0 - self.hidden1) * (np.dot(deltah2, np.transpose(self.weights2)))

            updatew1 = eta * (np.dot(np.transpose(inputs), deltah1[:, :-1])) + self.momentum * updatew1
            updatew2 = eta * (np.dot(np.transpose(self.hidden1), deltah2[:, :-1])) + self.momentum * updatew2
            updatew3 = eta * (np.dot(np.transpose(self.hidden2), deltao)) + self.momentum * updatew3

            self.weights1 -= updatew1
            self.weights2 -= updatew2
            self.weights3 -= updatew3

    def mlpfwd(self, inputs):

        self.hidden1 = np.dot(inputs, self.weights1)
        self.hidden1 = 1.0 / (1.0 + np.exp(-self.beta * self.hidden1))
        self.hidden1 = np.concatenate((self.hidden1, -np.ones((np.shape(inputs)[0], 1))), axis=1)

        self.hidden2 = np.dot(self.hidden1, self.weights2)
        self.hidden2 = 1.0 / (1.0 + np.exp(-self.beta * self.hidden2))
        self.hidden2 = np.concatenate((self.hidden2, -np.ones((np.shape(inputs)[0], 1))), axis=1)

        outputs = np.dot(self.hidden2, self.weights3)

        # Different types of output neurons
        if self.outtype == 'linear':
            return outputs
        elif self.outtype == 'logistic':
            return 1.0 / (1.0 + np.exp(-self.beta * outputs))
        elif self.outtype == 'softmax':
            normalisers = np.sum(np.exp(outputs), axis=1) * np.ones((1, np.shape(outputs)[0]))
            return np.transpose(np.transpose(np.exp(outputs)) / normalisers)
        else:
            print("error")

    def early_stop(self, train_inputs, train_targets, validation_set, validation_set_targets, eta):
        """ initialise first error """
        validation_set = np.concatenate((validation_set, -np.ones((np.shape(validation_set)[0], 1))), axis=1)
        self.mlptrain(train_inputs, train_targets, eta, 100)
        validation_out = self.mlpfwd(validation_set)
        error1 = 0.5 * (np.sum(validation_out - validation_set_targets) ** 2)

        """ initialise second error """
        self.mlptrain(train_inputs, train_targets, eta, 100)
        validation_out = self.mlpfwd(validation_set)
        error2 = 0.5 * (np.sum(validation_out - validation_set_targets) ** 2)

        while error2 < error1:
            self.mlptrain(train_inputs, train_targets, eta, 100)
            error1 = error2
            validation_out = self.mlpfwd(validation_set)
            error2 = 0.5 * (np.sum(validation_out - validation_set_targets) ** 2)

    def confmat(self, inputs, targets):
        """Confusion matrix"""

        # Add the inputs that match the bias node
        inputs = np.concatenate((inputs, -np.ones((np.shape(inputs)[0], 1))), axis=1)
        outputs = self.mlpfwd(inputs)

        nclasses = np.shape(targets)[1]

        if nclasses == 1:
            nclasses = 2
            outputs = np.where(outputs > 0.5, 1, 0)
        else:
            # 1-of-N encoding
            outputs = np.argmax(outputs, 1)
            targets = np.argmax(targets, 1)

        cm = np.zeros((nclasses, nclasses))
        for i in range(nclasses):
            for j in range(nclasses):
                cm[i, j] = np.sum(np.where(outputs == j, 1, 0) * np.where(targets == i, 1, 0))

        print("Confusion matrix is:")
        print(cm)
        print("Percentage Correct: ", np.trace(cm) / np.sum(cm) * 100)