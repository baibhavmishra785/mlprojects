# -*- coding: utf-8 -*-
"""Parkinson's Disease Prediction.ipynb

"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# %matplotlib inline

import seaborn as sns
import tensorflow as tf

import logging
logging.basicConfig(filename='P-disease logs', level = logging.INFO, format = '%(asctime)s, %(name)s, %(message)s')
logging.info('Logs started.')

df = pd.read_csv('Parkinsson dataset.csv')

df.head()

df.isnull().sum()

df.info()

df.describe()

df.corr()['status'][:-1].sort_values().plot(kind='bar')

df = df.drop('name', axis = 1)

plt.figure(figsize=(30,30))
sns.heatmap(df.corr(), annot = True, cmap= "coolwarm")

X = df.drop('status', axis = 1)
Y = df['status']

try:
  from sklearn.model_selection import train_test_split
  X_train, X_test, Y_train, Y_test = train_test_split(X,Y,test_size=0.25,random_state=101)
  
  from sklearn.preprocessing import MinMaxScaler
  scaler = MinMaxScaler()

  X_train_scaled = scaler.fit_transform(X_train)
  X_test_scaled = scaler.transform(X_test)

  X_train_scaled.shape

  from tensorflow.keras.models import Sequential
  from tensorflow.keras.layers import Dense, Activation,Dropout

  model = Sequential()
  model.add(Dense(units=30,activation='relu'))
  model.add(Dropout(0.2))
  model.add(Dense(units=25,activation='relu'))
  model.add(Dropout(0.2))
  model.add(Dense(units=10,activation='relu'))
  model.add(Dropout(0.2))
  model.add(Dense(units=1,activation='sigmoid'))

  model.compile(loss='binary_crossentropy', optimizer='adam')
  print('Model is working fine')

except Exception as e:
  print('There is an exception')

from tensorflow.keras.callbacks import EarlyStopping
cb = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=10)

model.fit(x=X_train_scaled,y=Y_train, validation_data=(X_test_scaled, Y_test), batch_size=450, epochs=600, callbacks=[cb])

losses = pd.DataFrame(model.history.history)

losses.plot()

predictions = (model.predict(X_test_scaled) > 0.5).astype("int32")

from sklearn.metrics import classification_report,confusion_matrix, accuracy_score

print(confusion_matrix(Y_test,predictions))

print(classification_report(Y_test,predictions))

print(accuracy_score(Y_test,predictions))

logging.info('Project successful.')
