'''强化学习框架'''

import numpy
import time

class frame():
    def __init__(self, client):
        self.client = client

    def take_action(self, action):
        #根据不同动作采取不同的行动
        if action == "forward":
            self.client.MoveByDroneSpeed(1, 0, 0, 1)
        if action == "backward":
            self.client.MoveByDroneSpeed(-1, 0, 0, 1)
        if action == "left":
            self.client.MoveByDroneSpeed(0, -1, 0, 1)
        if action == "right":
            self.client.MoveByDroneSpeed(0, 1, 0, 1)
        if action == "up":
            self.client.MoveByDroneSpeed(0, 0, -1, 0.5)
        if action == "down":
            self.client.MoveByDroneSpeed(0, 0, 1, 0.5)
        if action == "yaw_Right":
            x, y, z, roll, pitch, yaw = self.client.get_position()
            target_yaw = yaw - numpy.pi/18
            self.client.change_Yaw(0, 0, -target_yaw, 0.5, 1)
        if action == "yaw_left":
            x, y, z, roll, pitch, yaw = self.client.get_position()
            target_yaw = yaw + numpy.pi/18
            self.client.change_Yaw(0, 0, -target_yaw, 0.5, 1)

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
        
        #执行完一步保存一张图片
        # self.client.save_img("Depth")
        # self.client.img_count -= 1
        # self.client.save_img("RGB")

        self.client.hover() #悬停
        next_state = self.client.get_img("RGB")
        x, y, z, roll, pitch, yaw = self.client.get_position()
        done = False
        if (x<-2) or (x>2) or (z<-3) or (z>0.2) or (y<-2) or (y>12):    #限制无人机的位置范围，一个长方体   第一个圈
            done = True
        # if (x<-1) or (x>3) or (z<-3) or (z>0.2) or (y<9) or (y>20):    #限制无人机的位置范围，一个长方体   第2个圈
        #     done = True
        # reward = 0.3*(1-((x+1)/3)) + 0.3*(1-((z+2.6)/2.8)) + 0.4*(1-((y-10)/12))    #奖励函数的设置 第一个版本
        L = numpy.sqrt((x+0.5)**2 + (y-9)**2 + (z+2.5)**2)  #目标位置 （-0.5, 9, -2.5）
        reward = 1-(L/5)
        return next_state, reward, done
        
