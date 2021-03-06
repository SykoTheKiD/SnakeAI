import os

import tensorflow as tf

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


class NeuralNetwork:
    def __init__(self):
        num_nodes_hl1 = 100
        num_nodes_hl2 = 400
        num_nodes_hl3 = 200
        self.input_size = 6
        self.num_classes = 4
        self.hl_1 = {'weights': tf.Variable(tf.random_normal([self.input_size, num_nodes_hl1])),
                     'biases': tf.Variable(tf.random_normal([num_nodes_hl1]))}

        self.hl_2 = {'weights': tf.Variable(tf.random_normal([num_nodes_hl1, num_nodes_hl2])),
                     'biases': tf.Variable(tf.random_normal([num_nodes_hl2]))}

        self.hl_3 = {'weights': tf.Variable(tf.random_normal([num_nodes_hl2, num_nodes_hl3])),
                     'biases': tf.Variable(tf.random_normal([num_nodes_hl3]))}

        self.output_layer = {'weights': tf.Variable(tf.random_normal([num_nodes_hl3, self.num_classes])),
                             'biases': tf.Variable(tf.random_normal([self.num_classes]))}
        self.layers = [self.hl_1, self.hl_2, self.hl_3, self.output_layer]
        self.x_input_placeholder = tf.placeholder(shape=[None, self.input_size], dtype=tf.float32)
        l1 = tf.add(tf.matmul(self.x_input_placeholder, self.hl_1['weights']), self.hl_1['biases'])
        l1 = tf.nn.relu(l1)
        l2 = tf.add(tf.matmul(l1, self.hl_2['weights']), self.hl_2['biases'])
        l2 = tf.nn.relu(l2)
        l3 = tf.add(tf.matmul(l2, self.hl_3['weights']), self.hl_3['biases'])
        l3 = tf.nn.relu(l3)
        self.output_layer_final = tf.add(tf.matmul(l3, self.output_layer['weights']), self.output_layer['biases'])

    def predict(self, input_vector):
        with tf.Session() as sess:
            sess.run(tf.global_variables_initializer())
            layer_eval = self.output_layer_final.eval(feed_dict={self.x_input_placeholder: [input_vector]})
            result = sess.run(tf.argmax(layer_eval, 1))
        return result[0]
