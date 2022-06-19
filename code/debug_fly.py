import Drone_control
import time

if __name__ == "__main__":
    MyDrone = Drone_control.DroneControler()    #创建无人机对象

    MyDrone.rest()
    MyDrone.initFly()   #初始化飞行
    MyDrone.Move2position(-0.5, 3, -2.5, 2)     #可以作为第一个圈的初始检测位置，在这里可以比较近的看完全整个圈
    MyDrone.hover() #悬停
    MyDrone.get_position()
    time.sleep(1)
    MyDrone.Move2position(-0.5, 9, -2.5, 2)
    MyDrone.hover() #悬停
    MyDrone.get_position()

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