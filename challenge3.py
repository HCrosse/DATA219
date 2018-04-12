import datetime
import numpy as np
import pandas as pd
import sqlite3
from keras import callbacks
from keras.layers import Activation, Dense
from keras.models import Sequential
from livelossplot import PlotLossesKeras
from sklearn.metrics import accuracy_score
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier

con = sqlite3.connect("Data/Fires/Data/FPA_FOD_20170508.sqlite")
df = pd.read_sql('select LATITUDE, LONGITUDE, OWNER_DESCR, DISCOVERY_TIME, CONT_TIME, DISCOVERY_DATE, CONT_DATE,'
                 'FIRE_SIZE, FIRE_YEAR, STATE, STAT_CAUSE_DESCR from Fires', con)

df = df.dropna()

own_hot = pd.get_dummies(df.OWNER_DESCR)
year_hot = pd.get_dummies(df.FIRE_YEAR)
state_hot = pd.get_dummies(df.STATE)

df['DISC_DATETIME'] = pd.to_datetime(df.DISCOVERY_DATE - pd.Timestamp(0).to_julian_date(), unit='D')
df['CONT_DATETIME'] = pd.to_datetime(df.CONT_DATE - pd.Timestamp(0).to_julian_date(), unit='D')

df.DISCOVERY_TIME = pd.to_datetime(df.DISCOVERY_TIME, format='%H%M') - datetime.datetime(1900, 1, 1)
df.CONT_TIME = pd.to_datetime(df.CONT_TIME, format='%H%M') - datetime.datetime(1900, 1, 1)
df['DURATION'] = ((df.CONT_DATETIME + df.CONT_TIME) - (df.DISC_DATETIME + df.DISCOVERY_TIME)) / np.timedelta64(1, 'm')
df.DURATION = df.DURATION.astype('int')

df = df[['LATITUDE', 'LONGITUDE', 'DURATION', 'FIRE_SIZE', 'STAT_CAUSE_DESCR']]

df2 = df.join(own_hot).join(year_hot).join(state_hot)

train = df2.sample(frac=.7)
test = df2.drop(train.index)
train_target = train.STAT_CAUSE_DESCR
train = train.drop('STAT_CAUSE_DESCR', axis=1)
test_target = test.STAT_CAUSE_DESCR
test = test.drop('STAT_CAUSE_DESCR', axis=1)

gnb = GaussianNB()
gnb.fit(train, train_target)

pred = gnb.predict(test)
gnb_accuracy = accuracy_score(test_target, pred)

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% #
# Super simple MLP

df = df.join(own_hot).join(year_hot)
train = df.sample(frac=.7)
test = df.drop(train.index)
train_target = pd.get_dummies(train.STAT_CAUSE_DESCR)
train = train.drop('STAT_CAUSE_DESCR', axis=1)
test_target = pd.get_dummies(test.STAT_CAUSE_DESCR)
test = test.drop('STAT_CAUSE_DESCR', axis=1)

n_input = len(train.columns)
n_classes = len(train_target.columns)

model = Sequential([
    Dense(32, input_shape=(n_input,)),
    Activation('relu'),
    Dense(n_classes),
    Activation('softmax'),
])

model.compile(optimizer='rmsprop',
              loss='categorical_crossentropy',
              metrics=['accuracy'],)

tbCallBack = callbacks.TensorBoard(log_dir='./TensorBoard', histogram_freq=0, write_graph=True, write_images=True)

model.fit(train, train_target, epochs=10, batch_size=100, validation_data=(test, test_target),
          callbacks=[tbCallBack, PlotLossesKeras()])
score = model.evaluate(test, test_target, batch_size=100)

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% #
# Super simple k-NN

neigh = KNeighborsClassifier()  # default K of 5 turned out to be good
neigh.fit(train, train_target)

k_pred = neigh.predict(test)
k_accuracy = accuracy_score(test_target, k_pred)

print(gnb_accuracy)  # 23.95% (+/- 10.6%)
print(score)     # 46.61 (+/- 1.94%)
print(k_accuracy)  # 40.43 (+/- 0.04%)
