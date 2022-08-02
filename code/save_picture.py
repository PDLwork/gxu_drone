'''该文件用于双线程的时候作为另一个程序不断连续采集图片'''

import Drone_control


if __name__ == "__main__":
    IMG_Drone = Drone_control.DroneControler()
    IMG_Drone.init_getimg()

    for i in range(100):
        IMG_Drone.save_img("Depth")
        IMG_Drone.img_count -= 1
        IMG_Drone.save_img("RGB")

    print("图像采集结束！") 