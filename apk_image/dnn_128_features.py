import tensorflow as tf


class DNNClassifier:
    def __init__(self):

        self.train_data=None
        self.train_labels=None
        self.test_data=None
        self.test_labels=None

        self.x_image = tf.placeholder(dtype=tf.float32, shape=(None, 153))
        self.y_true = tf.placeholder(dtype=tf.float32, shape=(None, 1))
        self.prob = tf.placeholder(dtype=tf.float32)
        
        self.full_layer_one = tf.nn.relu(self.normal_full_layer(self.x_image, 25))
        self.full_one_dropout = tf.nn.dropout(self.full_layer_one, keep_prob=self.prob)
        
        self.full_layer_two = tf.nn.relu(self.normal_full_layer(self.full_one_dropout, 25))
        self.full_two_dropout = tf.nn.dropout(self.full_layer_two, keep_prob=self.prob)
        
        self.full_layer_three = tf.nn.relu(self.normal_full_layer(self.self.full_layer_two, 25))
        self.full_three_dropout = tf.nn.dropout(self.full_layer_three, keep_prob=self.prob)
        
        self.y_pred = self.normal_full_layer(self.full_three_dropout, 1)

        self.squared_error = tf.reduce_mean((self.y_pred-self.y_true)**2)

        self.optimiser = tf.train.RMSPropOptimizer(learning_rate=0.01)

        self.train = self.optimiser.minimize(self.squared_error)

        self.init = tf.global_variables_initializer()

    def set_data(self, train_data, train_labels, test_data, test_labels):
        self.train_data = train_data
        self.train_labels = train_labels
        self.test_data = test_data
        self.test_labels = test_labels

    def init_weights(self, shape):
        a = tf.truncated_normal(shape=shape, stddev=0.1)
        return tf.Variable(a)

    def init_bias(self, shape):
        a = tf.constant(0.1, shape=shape)
        return tf.Variable(a)

    def normal_full_layer(self, input_layer, size):
        input_size = int(input_layer.get_shape()[1])
        W = self.init_weights([input_size, size])
        b = self.init_bias([size])
        return tf.matmul(input_layer, W) + b

    def train_model(self):
        accuracy = 0
        prev_accuracy = -1
        with tf.Session() as sess:
            sess.run(self.init)
            batch_data = self.train_data
            batch_labels = self.train_labels

            test_data=self.test_data
            test_labels=self.test_labels

            i = 0
            while prev_accuracy < accuracy < 1.0:
                sess.run(self.train, feed_dict={self.x_image: batch_data, self.y_true: batch_labels, self.prob: 0.5})

                if i % 100 == 0:
                    matches = tf.equal(tf.argmax(self.y_pred, 1), tf.argmax(self.y_true, 1))

                    acc = tf.reduce_mean(tf.cast(matches, tf.float32))
                    prev_accuracy = accuracy
                    accuracy = sess.run(acc, feed_dict={self.x_image: test_data, self.y_true: test_labels, self.prob: 1.0})


                i += 1
        
        return prev_accuracy*100
