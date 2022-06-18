import numpy
import time

class frame():
    def __init__(self, client):
        self.client = client

    def take_action(self, action):
        if action == "forward":
            self.client.MoveByDroneSpeed(1, 0, 0, 1)
        if action == "backward":
            self.client.MoveByDroneSpeed(-1, 0, 0, 1)
        if action == "left":
            self.client.MoveByDroneSpeed(0, -1, 0, 1)
        if action == "right":
            self.client.MoveByDroneSpeed(0, 1, 0, 1)
        if action == "up":
            self.client.MoveByDroneSpeed(0, 0, -1, 1)
        if action == "down":
            self.client.MoveByDroneSpeed(0, 0, 1, 1)
        if action == "yaw_Right":
            yaw = self.client.get_position()
            yaw -= numpy.pi/18
            self.client.change_Yaw(0, 0, yaw, 0.5, 4)
        if action == "yaw_left":
            yaw = self.client.get_position()
            yaw += numpy.pi/18
            self.client.change_Yaw(0, 0, yaw, 0.5, 4)

        if action == 0:
            self.client.MoveByDroneSpeed(1, 0, 0, 0.5)
        if action == 1:
            self.client.MoveByDroneSpeed(-1, 0, 0, 0.5)
        if action == 2:
            self.client.MoveByDroneSpeed(0, -1, 0, 0.5)
        if action == 3:
            self.client.MoveByDroneSpeed(0, 1, 0, 0.5)
        if action == 4:
            self.client.MoveByDroneSpeed(0, 0, -1, 0.5)
        if action == 5:
            self.client.MoveByDroneSpeed(0, 0, 1, 0.5)
        if action == 6:
            # x, y, z, roll, pitch, yaw = self.client.get_position()
            # yaw -= numpy.pi/18
            # self.client.change_Yaw(0, 0, yaw, 0.5, 4)
            pass
        if action == 7:
            # x, y, z, roll, pitch, yaw = self.client.get_position()
            # yaw += numpy.pi/18
            # self.client.change_Yaw(0, 0, yaw, 0.5, 4)
            pass
        
        self.client.hover() #悬停
        next_state = self.client.get_img("RGB")
        x, y, z, roll, pitch, yaw = self.client.get_position()
        done = False
        if (x<-2) or (x>2) or (z<-3) or (z>0.2) or (y<-2) or (y>12):
            done = True
        reward = 0.3*(1-((x+1)/3)) + 0.3*(1-((z+2.6)/2.8)) + 0.4*(1-((y-10)/12))    #奖励函数的设置
        return next_state, reward, done
        
