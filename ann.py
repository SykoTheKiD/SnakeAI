import tensorflow as tf
import numpy as np


# hyperparameters
num_nodes_hl1 = 100
num_nodes_hl2 = 400
num_nodes_hl3 = 200

num_classes = 4

# input placeholders
x_input = tf.placeholder(tf.float32, [5, 1])
y_output = tf.placeholder(tf.float32)

def ann_model(input_vector):
	layer_1 = tf.layers.dense(input_vector, num_nodes_hl1)
	layer_2 = tf.layers.dense(layer_1, num_nodes_hl2)
	layer_3 = tf.layers.dense(layer_2, num_nodes_hl3)
	output_layer = tf.layers.dense(layer_3, num_classes)
	return output_layer

def model_estimator(features, labels, mode):
	ann = ann_model(features)

	prediction_classes = tf.argmax(ann, axis=1)
	prediction_probabilities = tf.nn.softmax(ann)

	if mode == tf.estimator.ModeKeys.PRECICT:
		return tf.estimator.EstimatorSpec(mode, predictions=prediction_classes)

	loss = tf.reduce_mean(tf.nn.sparse_softmax_cross_entropy_with_logits(
		logits=ann, labels=tf.cast(labels, dtype=tf.int32)))
	optimizer = tf.train.GradientDescentOptimizer(learning_rate=learning_rate)
	train_op = optimizer.minimize(loss, global_step=tf.train.get_global_step())

	accuracy = tf.metrics.accuracy(labels=labels, predictions=pred_classes)



# create session and run

# close
sess.close()