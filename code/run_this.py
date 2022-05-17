import Drone_control
import time
import numpy

if __name__ == "__main__":
    MyDrone = Drone_control.DroneControler()    #创建对象
    MyDrone.initFly()   #初始化飞行
    # MyDrone.Move2position(0, 1, -1.5, 1)
    # MyDrone.change_Yaw(0, 0, -(numpy.pi/2), 0.5, 4)
    MyDrone.MoveByDroneSpeed(0, 0, -1, 5)
    MyDrone.hover() #悬停
    MyDrone.get_position()
    time.sleep(5)
    MyDrone.landing()
    MyDrone.end_fly()
    print("----------测试完成！----------")