#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 18:44:44 2019

@author: gioel
"""

import tensorflow as tf

mnist = tf.keras.datasets.mnist 
(x_train, y_train), (x_test, y_test) = mnist.load_data()

x_train = tf.keras.utils.normalize(x_train, axis = 1)
x_test = tf.keras.utils.normalize(x_test, axis = 1)


model = tf.keras.models.Sequential() 
model.add(tf.keras.layers.Flatten()) 

model.add(tf.keras.layers.Dense(128, activation=tf.nn.relu)) 
model.add(tf.keras.layers.Dense(128, activation=tf.nn.relu)) 
model.add(tf.keras.layers.Dense(10, activation=tf.nn.softmax)) 

model.compile(optimizer = 'adam',
             loss= 'sparse_categorical_crossentropy', 
             metrics = ['accuracy']) 

model.fit(x_train, y_train, epochs = 3)