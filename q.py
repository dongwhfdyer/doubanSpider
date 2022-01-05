import numpy as np
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.utils import np_utils
import warnings

warnings.filterwarnings("ignore")
text = (open("story.txt", encoding='UTF-8').read())
text = text.lower()

characters = sorted(list(set(text)))

n_to_char = {n: char for n, char in enumerate(characters)}
char_to_n = {char: n for n, char in enumerate(characters)}

X = []
Y = []
length = len(text)
seq_length = 100
for i in range(0, length - seq_length, 1):
    # seq_length 长度的序列 作为输入
    sequence = text[i:i + seq_length]
    # label为序列后的一个字符 作为输出
    label = text[i + seq_length]
    # 将字典序列转换为数字
    X.append([char_to_n[char] for char in sequence])
    Y.append(char_to_n[label])
checkpoint()

X_modified = np.reshape(X, (len(X), seq_length, 1))
X_modified = X_modified / float(len(characters))
Y_modified = np_utils.to_categorical(Y)

model = Sequential()
model.add(LSTM(400, input_shape=(X_modified.shape[1], X_modified.shape[2]), return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(400))
model.add(Dropout(0.2))
model.add(Dense(Y_modified.shape[1], activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam')

model.fit(X_modified, Y_modified, epochs=1, batch_size=100)
model.save('./weights/chinese_text_generator.h5')
