import vrep
import numpy as np
import time

class Simple2WheelsRobot:

    def __init__(self):
        vrep.simxFinish(-1)
        self.clientID = vrep.simxStart('127.0.0.1', 19997, True, True, 5000, 5)
        self.sonics = ["Ultrasonic1", "Ultrasonic2", "Ultrasonic3"]
        self.time_delay = 0.05
        self.forward_koef = 5
        self.rotate_koef = 3
        self.sonic_range = 1
        self.delta_min = 0.01
        self.delta_max = 1.01
        self.speed = 0.5

        _, self.motor_left = vrep.simxGetObjectHandle(self.clientID, "MotorLeft",
                                                                 vrep.simx_opmode_blocking)
        _, self.motor_right = vrep.simxGetObjectHandle(self.clientID, "MotorRight",
                                                                      vrep.simx_opmode_blocking)
        if self.clientID != -1 :
            print("Connected!")
            # self.init_sensors()

    def _config_motor(self, motor, velocity):

        error_code = vrep.simxSetJointTargetVelocity(self.clientID, motor, velocity, vrep.simx_opmode_streaming)
        return error_code

    def move_forward(self):
        koef = self.forward_koef
        error_code_l = self._config_motor(self.motor_left, koef * self.speed)
        error_code_r = self._config_motor(self.motor_right, koef * self.speed)
        return error_code_l, error_code_r

    def rotate_left(self):
        koef = self.rotate_koef
        error_code_l = self._config_motor(self.motor_left, koef * -self.speed)
        error_code_r = self._config_motor(self.motor_right, koef * self.speed)
        return error_code_l, error_code_r

    def rotate_right(self):
        koef = self.rotate_koef
        error_code_l = self._config_motor(self.motor_left, koef * self.speed)
        error_code_r = self._config_motor(self.motor_right, koef * -self.speed)
        return error_code_l, error_code_r

    def stop(self):
        error_code_l = self._config_motor(self.motor_left, 0)
        error_code_r = self._config_motor(self.motor_right, 0)
        return error_code_l, error_code_r

    def move(self, signal):
        if signal == 0:
            self.rotate_left()
        elif signal == 1:
            self.move_forward()
        elif signal == 2:
            self.rotate_right()

    def _read(self, name):
        _, sonic = vrep.simxGetObjectHandle(self.clientID, name, vrep.simx_opmode_blocking)
        time.sleep(self.time_delay)
        _, detectionState, detectedPoint, detectedObjectHandle, detectedSurfaceNormalVector = vrep.simxReadProximitySensor(
            self.clientID, sonic , vrep.simx_opmode_streaming)
        time.sleep(self.time_delay)
        _, detectionState, detectedPoint, detectedObjectHandle, detectedSurfaceNormalVector = vrep.simxReadProximitySensor(
            self.clientID, sonic, vrep.simx_opmode_blocking)
        return detectedPoint

    def readDataFromSensors(self):
        data_array = []
        for s in self.sonics:
            data = self._read(s)[2]
            if data < self.delta_min and data >= 0:
                data = 0
            elif data > self.delta_max or data < 0:
                data = self.sonic_range
            data_array.append(data)
        return np.array([data_array])