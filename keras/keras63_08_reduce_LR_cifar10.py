import numpy as np

x_train = np.load('./_save/_NPY/k55_x_data_cifar10_train.npy')
x_test = np.load('./_save/_NPY/k55_x_data_cifar10_test.npy')
y_train = np.load('./_save/_NPY/k55_y_data_cifar10_train.npy')
y_test = np.load('./_save/_NPY/k55_y_data_cifar10_test.npy')

x_train = x_train.reshape(50000, 32*32*3)
x_test = x_test.reshape(10000, 32*32*3)

from sklearn.preprocessing import MinMaxScaler, StandardScaler, RobustScaler, MaxAbsScaler, QuantileTransformer, PowerTransformer
scaler = QuantileTransformer()
# scaler.fit(x_train) 
# x_train = scaler.transform(x_train) 
x_train = scaler.fit_transform(x_train)
x_test = scaler.transform(x_test) 

x_train = x_train.reshape(50000, 32*32, 3)
x_test = x_test.reshape(10000, 32*32, 3)

from sklearn.preprocessing import OneHotEncoder
one = OneHotEncoder()
y_train = y_train.reshape(-1,1)
y_test = y_test.reshape(-1,1)
one.fit(y_train)
y_train = one.transform(y_train).toarray() # (50000, 10)
y_test = one.transform(y_test).toarray() # (10000, 10)

# 2. model
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv1D, Flatten, MaxPool1D, GlobalAveragePooling1D, Dropout

model = Sequential()
model.add(Conv1D(filters=32, kernel_size=2, padding='same',                        
                        activation='relu' ,input_shape=(32*32, 3))) 
model.add(Conv1D(32, 2, padding='same', activation='relu'))                   
model.add(MaxPool1D())                                         
model.add(Conv1D(64, 2, padding='same', activation='relu'))                   
model.add(Conv1D(64, 2, padding='same', activation='relu'))    
model.add(Flatten())                                              
model.add(Dense(256, activation='relu'))
model.add(Dense(124, activation='relu'))
model.add(Dense(84, activation='relu'))
model.add(Dense(10, activation='softmax'))

# 3. comple fit // metrics 'acc'
from tensorflow.keras.optimizers import Adam

op = Adam(lr = 0.001)

# model.compile(loss='categorical_crossentropy', 
#                 optimizer='adam', metrics='acc')
model.compile(loss='categorical_crossentropy', 
                optimizer=op, metrics='acc')

from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
es = EarlyStopping(monitor='val_loss', patience=15, 
                mode='min', verbose=1)
lr = ReduceLROnPlateau(monitor='val_loss', patience=5, 
                mode='auto', verbose=1, factor=0.5)

import time 
start_time = time.time()
hist = model.fit(x_train, y_train, epochs=100, batch_size=1024, verbose=2,
    validation_split=0.05, callbacks=[es, lr])
end_time = time.time() - start_time

# 4. predict eval 

loss = model.evaluate(x_test, y_test, batch_size=256)
print("======================================")

acc = hist.history['acc']
val_acc = hist.history['val_acc']
loss = hist.history['loss']
val_loss = hist.history['val_loss']

print("total time : ", end_time)
print('acc : ',acc[-15])
print('val_acc : ',val_acc[-15])
print('loss : ',loss[-15])
print('val_loss : ',val_loss[-15])

'''
time :  90.459463596344
loss :  2.8855037689208984
acc :  0.6269000172615051

with lr
total time :  70.02825927734375
acc :  0.7510315775871277
val_acc :  0.642799973487854
loss :  0.7203593850135803
val_loss :  1.073926329612732
'''