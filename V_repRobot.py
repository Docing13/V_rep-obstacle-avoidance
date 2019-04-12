import Robot
import NN
import numpy as np
import time
class VrepRobot:
    def __init__(self):
        self.robot = Robot.Simple2WheelsRobot()
        self.brain = NN.NNRobotBrain()
        self.brain.loadModel()
    def starSimulation(self):
        print('Beginning Sim...')
        self.robot.stop()
        time.sleep(1)
        while 1:
            data = self.robot.readDataFromSensors()
            answer = self.brain.getAnswer(data)
            index = np.argmax(answer)
            self.robot.move(index)
            time.sleep(0.3)

def run():
    simulation = VrepRobot()
    simulation.starSimulation()
run()