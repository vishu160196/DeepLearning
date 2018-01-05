import tensorflow as tf


class LenetClassifier:

    def __init__(self):

        self.train_data=None
        self.train_labels=None
        self.test_data=None
        self.test_labels=None

        self.x_image = tf.placeholder(dtype=tf.float32, shape=(None, 12, 12, 1))
        self.y_true = tf.placeholder(dtype=tf.float32, shape=(None, 2))
        self.prob = tf.placeholder(dtype=tf.float32)

        self.convo_1 = self.convolutional_layer(self.x_image, shape=[2, 2, 1, 32])
        self.convo_1_pooling = self.max_pool_2by2(self.convo_1)
        self.convo_2 = self.convolutional_layer(self.convo_1_pooling, shape=[2, 2, 32, 64])
        self.convo_2_pooling = self.max_pool_2by2(self.convo_2)
        self.convo_2_flat = tf.reshape(self.convo_2_pooling, [-1, 3 * 3 * 64])
        self.full_layer_one = tf.nn.relu(self.normal_full_layer(self.convo_2_flat, 1024))
        self.full_one_dropout = tf.nn.dropout(self.full_layer_one, keep_prob=self.prob)
        self.y_pred = self.normal_full_layer(self.full_one_dropout, 2)

        self.cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=self.y_pred, labels=self.y_true))

        self.optimiser = tf.train.AdamOptimizer()

        self.train = self.optimiser.minimize(self.cross_entropy)

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

    def convolution(self, x, w):
        return tf.nn.conv2d(input=x, filter=w, strides=[1, 1, 1, 1], padding='SAME')

    def max_pool_2by2(self, x):
        return tf.nn.max_pool(x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')

    def convolutional_layer(self, input_x, shape):
        W = self.init_weights(shape)
        b = self.init_bias([shape[3]])
        return tf.nn.relu(self.convolution(input_x, W) + b)

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
                    print(accuracy)

                i += 1
        return max(prev_accuracy, accuracy)*100
