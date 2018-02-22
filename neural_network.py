import os
import numpy as np
import tensorflow as tf

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

num_nodes_hl1 = 3
num_nodes_hl2 = 4
num_nodes_hl3 = 5
input_size = 6
num_classes = 4

x_input_placeholder = tf.placeholder(shape=[None, input_size], dtype=tf.float32)
output_y = tf.placeholder(dtype=tf.uint8)


def network_model(input_vector):
    hl_1 = {'weights': tf.Variable(tf.random_normal([input_size, num_nodes_hl1])),
            'biases': tf.Variable(tf.random_normal([num_nodes_hl1]))}

    hl_2 = {'weights': tf.Variable(tf.random_normal([num_nodes_hl1, num_nodes_hl2])),
            'biases': tf.Variable(tf.random_normal([num_nodes_hl2]))}

    hl_3 = {'weights': tf.Variable(tf.random_normal([num_nodes_hl2, num_nodes_hl3])),
            'biases': tf.Variable(tf.random_normal([num_nodes_hl3]))}

    output_layer = {'weights': tf.Variable(tf.random_normal([num_nodes_hl3, num_classes])),
                    'biases': tf.Variable(tf.random_normal([num_classes]))}

    l1 = tf.add(tf.matmul(input_vector, hl_1['weights']), hl_1['biases'])
    l1 = tf.nn.relu(l1)
    l2 = tf.add(tf.matmul(l1, hl_2['weights']), hl_2['biases'])
    l2 = tf.nn.relu(l2)
    l3 = tf.add(tf.matmul(l2, hl_3['weights']), hl_3['biases'])
    l3 = tf.nn.relu(l3)
    output = tf.add(tf.matmul(l3, output_layer['weights']), output_layer['biases'])
    return output


def train_model():
    model = network_model(x_input_placeholder)
    cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(model, y))
    optimizer = tf.train.AdamOptimizer().minimize(cost)

    num_runs = 10
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        for i in range(num_runs):
            loss = 0
            for _ in range(len(dataset)):
                run_x, run_y = dataset
                _, c = sess.run([optimizer, cost], feed_dict={x_input_placeholder: run_x, output_y: run_y})
                loss += c


if __name__ == '__main__':
    x = np.genfromtxt('data/data.csv', delimiter=',')
    print(x[1])
