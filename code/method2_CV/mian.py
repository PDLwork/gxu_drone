'''传统CV方法过圆'''
import sys
sys.path.append(sys.argv[0].rstrip('/main.py').rstrip('ethod2_CV').rstrip('/m'))  #这一系列的操作是为了能导入上一级的包
import Drone_control
import detect_circle

if __name__ == "__main__":
    MyDrone = Drone_control.DroneControler()    #创建无人机对象

    MyDrone.initFly()   #初始化飞行
    MyDrone.Move2position(-0.5, 3, -2.5, 2)     #可以作为第1个圈的初始检测位置，在这里可以比较近的看完全整个圈 第1个圈起点
    for i in range(40):
        A = MyDrone.get_IMU_data()
        print(A)
        # img_buffer = MyDrone.get_img("Depth")
        # MyDrone.save_img("Depth")
        # MyDrone.img_count -= 1
        # MyDrone.save_img("RGB")
        # center_A, center_B = detect_circle.circle_center(img_buffer)
        # flag_begin = False
        # if center_A != False:

        #     if abs(center_B-72) + abs(center_A-128) > 20:
        #         speed_x = 0
        #         speed_y = 0 
        #         if (center_B-72) > 10:
        #             speed_x = 1
        #         if (center_B-72) < -10:
        #             speed_x = -1
        #         if (center_A-128) > 10:
        #             speed_y = 1
        #         if (center_A-128) < -10:
        #             speed_y = -1
        #         MyDrone.MoveByDroneSpeed(0.5, speed_x, speed_y, 1)
        #         print("改变位姿")
        #         print(i, speed_x, speed_y)
        # else:
        #     MyDrone.MoveByDroneSpeed(1, 0, 0, 1)
        