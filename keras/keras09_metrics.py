from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import numpy as np
import matplotlib.pyplot as plt
import time 

# 1. 데이터
x = np.array([[1,2,3,4,5,6,7,8,9,10], [1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.5, 1.4, 1.3], [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]])
x1 = np.transpose(x)
# print(x1.shape) #( 10,3)
y = np.array([[11,12,13,14,15,16,17,18,19,20]])
y1 = np.transpose(y)
# print(y.shape) # (10, ) <-> (10, 1)

# 2. 모델 구성
model = Sequential()
model.add(Dense(5, input_dim=3))
model.add(Dense(5))
model.add(Dense(5))
model.add(Dense(5))
model.add(Dense(5))
model.add(Dense(5))
model.add(Dense(5))
model.add(Dense(1))

# 3. 컴파일, 훈련
# metrics = 반영은 없으나 지표 표현
# loss :  [0.014884325675666332, 0.0939272865653038]
# 두개 이상은 list로 표현
# mse = Mean Square error
# mae = Mean Absolute error
# rmse = Root mse 
model.compile(loss='mse', optimizer='adam', metrics=['mae'])
start = time.time()
model.fit(x1, y1, epochs=100, batch_size=1, verbose=1)
end = time.time() - start
print("걸린 시간 : ", end)

# verbose / 출력 양 설정
# 0 -> hide
# 1 -> show
# 2 -> hide progress bar
# 3 -> epo only

# 4. 평가 예측
loss = model.evaluate(x1, y1)
print('loss : ', loss)
y_pred = model.predict(x1)
print('[10, 1.3, 1]의 예측값 : ', y_pred)

# 5. 시각화
# y_predict = model.predict(x1)
# plt.scatter(x1[:,0],y1)
# plt.scatter(x1[:,1],y1)
# plt.scatter(x1[:,2],y1)

# plt.plot(x1,y_predict, color='red')
# plt.show()
