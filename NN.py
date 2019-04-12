from keras.models import Sequential
from keras.layers import Dense
from keras.models import load_model
import random
import numpy as np

class NNRobotBrain:
    def __init__(self):
        self.model = None
        self.epchs = 8
        self.batch = 20
        self.nn_name = 'nn.h5'
    def initNN(self):

        model = Sequential()
        model.add(Dense(40,activation='sigmoid',input_shape=(3,)))
        model.add(Dense(3,activation='sigmoid'))
        model.compile(optimizer='adam', loss='mse')
        return model

    def generateTrainData(self, examples_num = 300):
        # meters
        sensor_range = 1
        detect_range = 0.3
        detect_error = 0.05

        left_move = [1, 0, 0]
        right_move = [0, 0, 1]
        forward_move = [0, 1, 0]
        detect_lim = detect_range  # +- detect error
        x = []
        y = []
        for _ in range(examples_num):
            # left
            s1_data = random.uniform(0,sensor_range)
            # center
            s2_data = random.uniform(0,sensor_range)
            # right
            s3_data = random.uniform(0,sensor_range)
            sens_data = np.array([s1_data, s2_data, s3_data])
            x.append(sens_data)
            # turn left
            if s1_data <= detect_lim and s2_data > detect_lim and s3_data > detect_lim:
                y.append(left_move)
            # turn right
            elif s3_data <= detect_lim and s2_data > detect_lim and s1_data > detect_lim:
                y.append(right_move)
            # turn if all the obstcle on sensors data  - default rotation left
            elif s3_data <= detect_lim and s2_data <= detect_lim and s1_data <= detect_lim:
                y.append(left_move)
            # move straight if there is no obs onthe straight line
            elif s3_data <= detect_lim and s2_data > detect_lim and s1_data <= detect_lim:
                y.append(forward_move)
            # empty data from sensors
            elif s3_data > detect_lim and s2_data > detect_lim and s1_data > detect_lim:
                y.append(forward_move)
            # in any case just go
            else:
                y.append(forward_move)
        x = np.array(x)
        y = np.array(y)
        return x, y

    def learn(self):
        x = np.loadtxt('x_train.txt',delimiter=' ')
        y = np.loadtxt('y_train.txt', delimiter=' ')
        model = self.initNN()
        model.fit(x, y, epochs=self.epchs, batch_size=self.batch)
        self.model = model
        return model

    def saveModel(self,model):
        model.save(self.nn_name)

    def loadModel(self):
        model = load_model(self.nn_name)
        self.model = model

    def getAnswer(self,data):
        return self.model.predict(data)
