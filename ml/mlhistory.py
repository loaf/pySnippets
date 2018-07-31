#coding=utf-8
#http://python.jobbole.com/88713/

#1.最小二乘法,可参考 https://www.cnblogs.com/armysheng/p/3422923.html

# y = mx + b
# m is slope, b is y-intercept

def compute_error_for_line_given_points(b, m, coordinates):
    totalError = 0
    for i in range(0, len(coordinates)):
        x = coordinates[i][0]
        y = coordinates[i][1]
        totalError += (y - (m * x + b)) ** 2
    return totalError / float(len(coordinates))


# example
#z=compute_error_for_line_given_points(1, 2, [[3, 6], [6, 9], [12, 18]])
#print(z)


#2.梯度下降
current_x = 0.5  # the algorithm starts at x=0.5
learning_rate = 0.01  # step size multiplier
num_iterations = 60  # the number of times to train the function

# the derivative of the error function (x**4 = the power of 4 or x^4)
def slope_at_given_x_value(x):
    return 5 * x ** 4 - 6 * x ** 2

# Move X to the right or left depending on the slope of the error function
for i in range(num_iterations):
    previous_x = current_x
    current_x += -learning_rate * slope_at_given_x_value(previous_x)
    print(previous_x)

print("The local minimum occurs at %f" % current_x)

#3.线性回归
# Price of wheat/kg and the average price of bread
wheat_and_bread = [[0.5, 5], [0.6, 5.5], [0.8, 6], [1.1, 6.8], [1.4, 7]]

def step_gradient(b_current, m_current, points, learningRate):
    b_gradient = 0
    m_gradient = 0
    N = float(len(points))
    for i in range(0, len(points)):
        x = points[i][0]
        y = points[i][1]
        b_gradient += -(2 / N) * (y - ((m_current * x) + b_current))
        m_gradient += -(2 / N) * x * (y - ((m_current * x) + b_current))
    new_b = b_current - (learningRate * b_gradient)
    new_m = m_current - (learningRate * m_gradient)
    return [new_b, new_m]


def gradient_descent_runner(points, starting_b, starting_m, learning_rate, num_iterations):
    b = starting_b
    m = starting_m
    for i in range(num_iterations):
        b, m = step_gradient(b, m, points, learning_rate)
    return [b, m]

gradient_descent_runner(wheat_and_bread, 1, 1, 0.01, 100)

#4.感知机
from random import choice
from numpy import array, dot, random

_1_or_0 = lambda x: 0 if x < 0 else 1
training_data = [(array([0, 0, 1]), 0),
                 (array([0, 1, 1]), 1),
                 (array([1, 0, 1]), 1),
                 (array([1, 1, 1]), 1), ]
weights = random.rand(3)
errors = []
learning_rate = 0.2
num_iterations = 100

for i in range(num_iterations):
    input, truth = choice(training_data)
    result = dot(weights, input)
    error = truth - _1_or_0(result)
    errors.append(error)
    weights += learning_rate * error * input

for x, _ in training_data:
    result = dot(x, weights)
    print("{}: {} -> {}".format(input[:2], result, _1_or_0(result)))


#5.人工神经网络
import numpy as np

X_XOR = np.array([[0, 0, 1], [0, 1, 1], [1, 0, 1], [1, 1, 1]])
y_truth = np.array([[0], [1], [1], [0]])

np.random.seed(1)
syn_0 = 2 * np.random.random((3, 4)) - 1
syn_1 = 2 * np.random.random((4, 1)) - 1


def sigmoid(x):
    output = 1 / (1 + np.exp(-x))
    return output


def sigmoid_output_to_derivative(output):
    return output * (1 - output)


for j in range(60000):
    layer_1 = sigmoid(np.dot(X_XOR, syn_0))
    layer_2 = sigmoid(np.dot(layer_1, syn_1))
    error = layer_2 - y_truth
    layer_2_delta = error * sigmoid_output_to_derivative(layer_2)
    layer_1_error = layer_2_delta.dot(syn_1.T)
    layer_1_delta = layer_1_error * sigmoid_output_to_derivative(layer_1)
    syn_1 -= layer_1.T.dot(layer_2_delta)
    syn_0 -= X_XOR.T.dot(layer_1_delta)

print("Output After Training: n", layer_2)

#6.深度神经网络
from __future__ import division, print_function, absolute_import
import tflearn
from tflearn.layers.core import dropout, fully_connected
from tensorflow.examples.tutorials.mnist import input_data
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.normalization import local_response_normalization
from tflearn.layers.estimator import regression

# Data loading and preprocessing
mnist = input_data.read_data_sets("/data/", one_hot=True)
X, Y, testX, testY = mnist.train.images, mnist.train.labels, mnist.test.images, mnist.test.labels
X = X.reshape([-1, 28, 28, 1])
testX = testX.reshape([-1, 28, 28, 1])

# Building convolutional network
network = tflearn.input_data(shape=[None, 28, 28, 1], name='input')
network = conv_2d(network, 32, 3, activation='relu', regularizer="L2")
network = max_pool_2d(network, 2)
network = local_response_normalization(network)
network = conv_2d(network, 64, 3, activation='relu', regularizer="L2")
network = max_pool_2d(network, 2)
network = local_response_normalization(network)
network = fully_connected(network, 128, activation='tanh')
network = dropout(network, 0.8)
network = fully_connected(network, 256, activation='tanh')
network = dropout(network, 0.8)
network = fully_connected(network, 10, activation='softmax')
network = regression(network, optimizer='adam', learning_rate=0.01,
                        loss='categorical_crossentropy', name='target')

# Training
model = tflearn.DNN(network, tensorboard_verbose=0)
model.fit({'input': X}, {'target': Y}, n_epoch=20,
            validation_set=({'input': testX}, {'target': testY}),
            snapshot_step=100, show_metric=True, run_id='convnet_mnist')