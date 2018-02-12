import numpy as np


class RBF_Network:
    def __init__(self, n_in, n_hidden, n_out):
        self.n_in=n_in
        self.n_hidden=n_hidden
        self.n_out=n_out
        self.weights=np.ndarray((n_hidden+1,n_out))

    def train(self, inputs, targets):
        """set beta"""
        self.prototypes, cluster_info = self.k_means(inputs)
        self.set_beta(cluster_info, inputs)

        """first layer activations"""
        activations=self.first_layer_activations(inputs)

        activations=np.concatenate((activations,-np.ones((activations.shape[0], 1))), axis=1)

        """weights obtained by multiplying target matrix with pseudo inverse of activation matrix"""
        self.weights=np.dot(np.linalg.pinv(activations), targets)

    def first_layer_activations(self, inputs):
        activations=np.ndarray((inputs.shape[0], self.n_hidden))
        for i in range(len(activations)):
            activations[i, :] = [np.exp(-self.beta[j] * np.linalg.norm(inputs[i] - self.prototypes[j])) for j in
            range(self.prototypes.shape[1])]

        return activations

    def test(self, test_input, test_target):
        activations=self.first_layer_activations(test_input)
        activations = np.concatenate((activations, -np.ones((activations.shape[0], 1))), axis=1)
        outputs=np.dot(activations, self.weights)
        # outputs=np.where(outputs>0.5, 1, 0)
        self.performance_metrics(outputs, test_target)

    def performance_metrics(self, outputs, targets):
        pass

    def set_beta(self, cluster_info, inputs):
        a=np.concatenate((inputs,cluster_info), axis=1)
        self.beta=[]

        for i in range(self.n_hidden):
            self.beta.append(np.mean(np.linalg.norm(a[a[:,1]==i][:,:-1]-self.prototypes[i],axis=1)))

        self.beta=np.array(self.beta)
        self.beta=(float)(1/(2*self.beta**2))

    def k_means(self, dataset, eps=0):
        prototypes = dataset[np.random.randint(0, dataset.shape[0] - 1, size=self.n_hidden)]
        prototypes_old = np.zeros(prototypes.shape)

        norm = np.linalg.norm(prototypes-prototypes_old)

        belongs_to = np.zeros((dataset.shape[0], 1))

        while norm > eps:
            dist = np.zeros((dataset.shape[0], self.n_hidden))

            for index, vector in enumerate(dataset):
                for proto_num, prototype in enumerate(prototypes):
                    dist[index, proto_num] = np.linalg.norm(prototype - vector)


            for index, distances in enumerate(dist):
                min = np.amin(distances)

                for i, d in enumerate(distances):
                    if d == min:
                        belongs_to[index, 0] = i
                        break


            prototypes_old = prototypes

            for i in range(self.n_hidden):
                inputs_close = [j for j in range(len(belongs_to)) if belongs_to[j,0] == i]

                prototypes[i, :] = np.mean(dataset[inputs_close], axis=0)

            norm = np.linalg.norm(prototypes - prototypes_old)

        return prototypes, belongs_to


