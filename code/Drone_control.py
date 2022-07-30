'''该文件是为了创建一个类，别的文件调用之后可以通过写好的方法来控制无人机以及获取图片'''

import airsim
import numpy
import cv2
import time

class DroneControler():
    def __init__(self):
        self.client = airsim.MultirotorClient()
        self.img_count = 0

    # 初始化无人机通常需要调用，调用完后无人机会起飞一定高度。
    def initFly(self):
        self.client.confirmConnection() # 查询是否建立连接
        self.client.enableApiControl(True)   # 打开API控制权
        self.client.armDisarm(True)    # 解锁
        self.client.takeoffAsync().join()     # 起飞

    # 降落
    def landing(self):
        self.client.landAsync().join()

    # 悬停
    def hover(self):
        self.client.hoverAsync()
    
    # 移动到世界坐标(GPS)
    def Move2position(self, x, y, z, speed):
        self.client.moveToPositionAsync(x, y, z, speed).join()

    # 结束飞行释放API控制权（若没有降落则无人机会突然降落）
    def end_fly(self):
        self.client.armDisarm(False)     # 上锁
        self.client.enableApiControl(False)   # 关闭API控制权

    # 获取无人机的世界坐标以及航向角
    def get_position(self):
        state = self.client.getMultirotorState()
        x = state.kinematics_estimated.position.x_val
        y = state.kinematics_estimated.position.y_val
        z = state.kinematics_estimated.position.z_val
        (pitch, roll, yaw) = airsim.to_eularian_angles(state.kinematics_estimated.orientation)
        print("x:", x, "y:", y, "z:", z, "roll:", roll, "pitch:", pitch, "yaw:", yaw)
        return x, y, z, roll, pitch, yaw

    #获取IMU信息
    def get_IMU_data(self):
        imu_data = self.client.getImuData()
        return imu_data

    # 飞行通过机体坐标三轴速度及时间
    def MoveByDroneSpeed(self, x, y, z, time):
        self.client.moveByVelocityBodyFrameAsync(vx=x, vy=y, vz=z, duration=time)

    # 改变无人机Yaw角（偏航）
    def change_Yaw(self, input_roll, input_pitch, input_yaw, input_throttle, input_duration):
        self.client.moveByRollPitchYawThrottleAsync(roll=input_roll, pitch=input_pitch, yaw=input_yaw, throttle=input_throttle, duration=input_duration).join()

    # 通过世界坐标速度移动（未编写）
    def MoveByWorldSpeed(self):
        pass

    #读取图片
    def get_img(self, img_type):
        # self.client.hoverAsync()
        # time.sleep(0.5)
        responses = self.client.simGetImages([
                airsim.ImageRequest(0, airsim.ImageType.Scene, False, False),
                airsim.ImageRequest(0, airsim.ImageType.DepthPerspective, True, False),
                airsim.ImageRequest(3, airsim.ImageType.DepthPerspective, True, False),
                airsim.ImageRequest(3, airsim.ImageType.Scene, False, False)
                ])

        if img_type == "RGB":
            response = responses[0]
            buffer = numpy.frombuffer(response.image_data_uint8, dtype=numpy.uint8) 
            img_rgb = buffer.reshape(response.height, response.width, -1)
            return img_rgb
        
        elif img_type == "Grayscale":
            response = responses[0]
            buffer = numpy.frombuffer(response.image_data_uint8, dtype=numpy.uint8) 
            img_rgb = buffer.reshape(response.height, response.width, -1)
            img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
            return img_gray

        elif img_type == "Depth":
            response = responses[1]
            Depth_Img = numpy.uint8(airsim.get_pfm_array(response))
            return Depth_Img

        elif img_type == "Bottom":
            response = responses[3]
            # Depth_Bottom_Img = airsim.get_pfm_array(response)
            buffer = numpy.frombuffer(response.image_data_uint8, dtype=numpy.uint8) 
            Depth_Bottom_Img = buffer.reshape(response.height, response.width, -1)
            return Depth_Bottom_Img
        
        else:
            return responses

    def rest(self):
        self.client.reset()

    # 保存图片
    def save_img(self, img_type):
        if img_type == "RGB":
            img_rgb = self.get_img("RGB")
            cv2.imwrite('./img/RGB/{}.jpg'.format(self.img_count), img_rgb)
        elif img_type == "Grayscale":
            img_gray = self.get_img("Grayscale")
            cv2.imwrite('./img/Grayscale/{}.jpg'.format(self.img_count), img_gray)
        elif img_type == "Depth":
            Depth_Img = self.get_img("Depth")
            cv2.imwrite('./img/Depth/{}.jpg'.format(self.img_count), Depth_Img)
        elif img_type == "Bottom":
            Depth_Left_Img = self.get_img("Bottom")
            cv2.imwrite('./img/Bottom/{}.jpg'.format(self.img_count), Depth_Left_Img)

        self.img_count += 1