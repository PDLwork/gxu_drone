import Reinforcement_Learning
import Drone_control
import GUI
import time
import numpy

if __name__ == "__main__":

    MyDrone = Drone_control.DroneControler()    #创建无人机对象
    RL_frame = Reinforcement_Learning.frame(MyDrone)
    GUI_window = GUI.GUI_Design(RL_frame)

    # MyDrone.rest()
    MyDrone.initFly()   #初始化飞行
    # MyDrone.Move2position(-0.5, 3, -2.5, 2)     #可以作为第1个圈的初始检测位置，在这里可以比较近的看完全整个圈 第1个圈起点
    # MyDrone.Move2position(-0.5, 1, -2.5, 2)
    # MyDrone.Move2position(1.3, 10, -0.5, 2)     #第2个圈起点
    # MyDrone.hover() #悬停
    # MyDrone.get_position()
    # MyDrone.get_img("Depth")
    # time.sleep(1)
    # MyDrone.Move2position(-0.5, 9, -2.5, 2)         #第1个圈目标点
    # MyDrone.Move2position(1.3, 16, -0.5, 2)     #第2个圈目标点
    # MyDrone.hover() #悬停
    # MyDrone.get_position()

    #针对降落的调试
    MyDrone.change_Yaw(0, 0, -(numpy.pi), 0.6, 2)
    # MyDrone.Move2position(0, 0, -10, 5)
    # MyDrone.Move2position(-30, 20, -10, 5)
    # MyDrone.Move2position(-30, 20, -1, 5)
    # MyDrone.Move2position(-48, 20, -1, 5)

    GUI_window.keep()

    # MyDrone.Move2position(-1, 10, -3, 2)      #目标位置
# MyDrone.MoveByDroneSpeed(0, 1, 0, 1.5)
# MyDrone.Move2position(-1, 10, -3, 2)
# # MyDrone.change_Yaw(0, 0, -(numpy.pi/2), 0.5, 4)
# MyDrone.change_Yaw(0, 0, (numpy.pi/2), 0.5, 2)
# # MyDrone.MoveByDroneSpeed(0, 1, 0, 5)
# MyDrone.hover() #悬停
# # MyDrone.rest()
# # MyDrone.get_img("RGB")
# MyDrone.hover()
# time.sleep(5)
# MyDrone.get_position()
# time.sleep(5)
# MyDrone.Move2position(0, 0, -2, 2)
# time.sleep(5)
# MyDrone.Move2position(-1, 10, -3, 2)
# MyDrone.rest()
# MyDrone.landing()
# MyDrone.end_fly()