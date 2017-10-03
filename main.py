import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf

dataframe = pd.read_csv('data.csv')
dataframe = dataframe.drop(['index', 'price', 'sq_price'], axis=1)[:10]
dataframe.loc[:, ("y1")] = [1, 1, 1, 0, 0, 1, 0, 1, 1, 1]

dataframe.loc[:, ("y2")] = dataframe["y1"] == 0
dataframe.loc[:, ("y2")] = dataframe["y2"].astype(int)

inputX = dataframe.loc[:, ['area', 'bathrooms']].as_matrix()
inputY = dataframe.loc[:, ["y1", "y2"]].as_matrix()


learning_rate = 0.000001
training_epochs = 2000
display_step = 50
n_samples = inputY.size

x = tf.placeholder(tf.float32, [None, 2])   # Okay TensorFlow, we'll feed you an array of examples. Each example will
                                            # be an array of two float values (area, and number of bathrooms).
                                            # "None" means we can feed you any number of examples
                                            # Notice we haven't fed it the values yet

W1 = tf.Variable(tf.zeros([2, 3]))           # Maintain a 2 x 2 float matrix for the weights that we'll keep updating
                                            # through the training process (make them all zero to begin with)

B1 = tf.Variable(tf.zeros([3]))              # Also maintain three bias values

v1_values = tf.add(tf.matmul(x, W1), B1)       # The first step in calculating the prediction would be to multiply
                                            # the inputs matrix by the weights matrix then add the biases

W2 = tf.Variable(tf.zeros([3, 2]))
B2 = tf.Variable(tf.zeros([2]))

y_values = tf.add(tf.matmul(v1_values, W2), B2)                 # Then we use softmax as an "activation function" that translates the
                                            # numbers outputted by the previous layer into probability form
y = tf.nn.softmax(y_values)

y_ = tf.placeholder(tf.float32, [None, 2])   # For training purposes, we'll also feed you a matrix of labels

# Cost function: Mean squared error
cost = tf.reduce_sum(tf.pow(y_ - y, 2))/(2*n_samples)
# Gradient descent
optimizer = tf.train.GradientDescentOptimizer(learning_rate).minimize(cost)

# Initialize variabls and tensorflow session
init = tf.initialize_all_variables()
sess = tf.Session()
sess.run(init)

for i in range(training_epochs):
    sess.run(x, feed_dict={x: inputX, y: inputY}) # Take a gradient descent step using our inputs and labels


    # That's all! The rest of the cell just outputs debug messages.
    # Display logs per epoch step
    if (i) % display_step == 0:
        cc = sess.run(cost, feed_dict={x: inputX, y_:inputY})
        print ("Training step:", '%04d' % (i), "cost=", "{:.9f}".format(cc)) #, \"W=", sess.run(W), "b=", sess.run(b)

print ("Optimization Finished!")
training_cost = sess.run(cost, feed_dict={x: inputX, y_: inputY})
print ("Training cost=", training_cost, "W1, W2=", sess.run(W1), sess.run(W2), "B1, B2=", sess.run(B1), sess.run(B2), '\n')

sess.run(y, feed_dict={x: inputX })
sess.close()
