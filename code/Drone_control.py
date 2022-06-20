import airsim
import numpy
import cv2
import time

class DroneControler():
    def __init__(self):
        self.client = airsim.MultirotorClient()

    def initFly(self):
        self.client.confirmConnection() # 查询是否建立连接
        self.client.enableApiControl(True)   # 打开API控制权
        self.client.armDisarm(True)    # 解锁
        # self.get_position()
        self.client.takeoffAsync().join()     # 起飞
        self.client.moveToZAsync(-2, 1).join()   # 上升到1.5米高度 0.5m/s速度

    def landing(self):
        # self.client.moveToZAsync(-1, 5).join()
        self.client.landAsync().join()

    def hover(self):
        self.client.hoverAsync()
    
    def Move2position(self, x, y, z, speed):
        self.client.moveToPositionAsync(x, y, z, speed).join()

    def end_fly(self):
        self.client.armDisarm(False)     # 上锁
        self.client.enableApiControl(False)   # 关闭API控制权

    def get_position(self):
        state = self.client.getMultirotorState()
        # print(state)
        x = state.kinematics_estimated.position.x_val
        y = state.kinematics_estimated.position.y_val
        z = state.kinematics_estimated.position.z_val
        (pitch, roll, yaw) = airsim.to_eularian_angles(state.kinematics_estimated.orientation)
        print("x:", x, "y:", y, "z:", z, "roll:", roll, "pitch:", pitch, "yaw:", yaw)
        return x, y, z, roll, pitch, yaw

    def MoveByDroneSpeed(self, x, y, z, time):
        self.client.moveByVelocityBodyFrameAsync(vx=x, vy=y, vz=z, duration=time).join()

    def change_Yaw(self, input_roll, input_pitch, input_yaw, input_throttle, input_duration):
        self.client.moveByRollPitchYawThrottleAsync(roll=input_roll, pitch=input_pitch, yaw=input_yaw, throttle=input_throttle, duration=input_duration).join()

    def MoveByWorldSpeed(self):
        pass

    def get_img(self, img_type):
        self.client.hoverAsync()
        # time.sleep(0.5)
        responses = self.client.simGetImages([
                airsim.ImageRequest("0", airsim.ImageType.Scene, False, False),
                airsim.ImageRequest("0", airsim.ImageType.DepthPerspective, True, False)
                ])

        if img_type == "RGB":
            response = responses[0]
            buffer = numpy.frombuffer(response.image_data_uint8, dtype=numpy.uint8) 
            img_rgb = buffer.reshape(response.height, response.width, -1)
            return img_rgb
            # cv2.imwrite('./img/RGB/0.jpg', img_rgb)
        
        elif img_type == "Grayscale":
            response = responses[0]
            buffer = numpy.frombuffer(response.image_data_uint8, dtype=numpy.uint8) 
            img_rgb = buffer.reshape(response.height, response.width, -1)
            img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
            cv2.imwrite('./img/Grayscale/0.jpg', img_gray)
            return img_gray

        if img_type == "Depth":
            response = responses[1]
            Depth_Img = airsim.get_pfm_array(response)
            print(Depth_Img)
            cv2.imwrite('./img/Depth/0.jpg', Depth_Img)
            return Depth_Img
        
        else:
            return responses

    def rest(self):
        self.client.reset()