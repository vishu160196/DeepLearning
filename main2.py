import pandas as pd              # A beautiful library to help us work with data as tables
import numpy as np               # So we can use number matrices. Both pandas and TensorFlow need it.
import matplotlib.pyplot as plt  # Visualize the things
import tensorflow as tf          # Fire from the gods


dataframe = pd.read_csv("data.csv") # Let's have Pandas load our dataset as a dataframe
dataframe = dataframe.drop(["index", "price", "sq_price"], axis=1) # Remove columns we don't care about
dataframe = dataframe[0:10] # We'll only use the first 10 rows of the dataset in this example

dataframe.loc[:, ("y1")] = [1, 1, 1, 0, 0, 1, 0, 1, 1, 1] # This is our friend's list of which houses she liked
                                                          # 1 = good, 0 = bad
dataframe.loc[:, ("y2")] = dataframe["y1"] == 0           # y2 is the negation of y1
dataframe.loc[:, ("y2")] = dataframe["y2"].astype(int)    # Turn TRUE/FALSE values into 1/0

inputX = dataframe.loc[:, ['area', 'bathrooms']].as_matrix()
inputY = dataframe.loc[:, ["y1", "y2"]].as_matrix()

# Parameters
learning_rate = 0.000001
training_epochs = 2000
display_step = 50
n_samples = inputY.size

x = tf.placeholder(tf.float32, [None, 2])   # Okay TensorFlow, we'll feed you an array of examples. Each example will
                                            # be an array of two float values (area, and number of bathrooms).
                                            # "None" means we can feed you any number of examples
                                            # Notice we haven't fed it the values yet

W = tf.Variable(tf.zeros([2, 2]))           # Maintain a 2 x 2 float matrix for the weights that we'll keep updating
                                            # through the training process (make them all zero to begin with)

b = tf.Variable(tf.zeros([2]))              # Also maintain two bias values

y_values = tf.add(tf.matmul(x, W), b)       # The first step in calculating the prediction would be to multiply
                                            # the inputs matrix by the weights matrix then add the biases

y = tf.nn.softmax(y_values)                 # Then we use softmax as an "activation function" that translates the
                                            # numbers outputted by the previous layer into probability form

y_ = tf.placeholder(tf.float32, [None,2])   # For training purposes, we'll also feed you a matrix of labels

# Cost function: Mean squared error
cost = tf.reduce_sum(tf.pow(y_ - y, 2))/(2*n_samples)
# Gradient descent
optimizer = tf.train.GradientDescentOptimizer(learning_rate).minimize(cost)

# Initialize variabls and tensorflow session
init = tf.initialize_all_variables()
sess = tf.Session()
sess.run(init)

for i in range(training_epochs):
    sess.run(optimizer, feed_dict={x: inputX, y_: inputY}) # Take a gradient descent step using our inputs and labels

    # That's all! The rest of the cell just outputs debug messages.
    # Display logs per epoch step
    if (i) % display_step == 0:
        cc = sess.run(cost, feed_dict={x: inputX, y_:inputY})
        print ("Training step:", '%04d' % (i), "cost=", "{:.9f}".format(cc)) #, \"W=", sess.run(W), "b=", sess.run(b)

print ("Optimization Finished!")
print(sess.run(x, feed_dict={x: inputX, y_: inputY}))
training_cost = sess.run(cost, feed_dict={x: inputX, y_: inputY})
print ("Training cost=", training_cost, "W=", sess.run(W), "b=", sess.run(b), '\n')

sess.run(y, feed_dict={x: inputX })
