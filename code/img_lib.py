import airsim
import os
import cv2
import numpy as np

class DroneController:
    def __init__(self,client,name):
        self.client = client
        self.name = name
        self.state = self.client.getMultirotorState()
    
    def initFly(self):
        self.client.confirmConnection()
        self.client.enableApiControl(True)
        self.client.armDisarm(True)              # 解锁
        self.client.takeoffAsync().join()        # 起飞
        self.client.moveToZAsync(-1.5, 0.2).join()   # 上升到1.5米高度
        return

class Filter():
    def __init__(self):
        self.hsv_range = {
            'white':[(0,0,140),(255,255,255)],
            'green':[(62,77,200),(70,100,255)],
            'red':[(150,25,105),(190,190,240)], #[(150,25,105),(190,190,240)]
            'red_1':[(0,20,20),(10,255,255)],
            'red_2':[(110,25,30),(190,255,255)] #加了雾
        }

    def select_HSV(self, img, HSV_Range):
        img_filtered = cv2.inRange(img, HSV_Range[0], HSV_Range[1])
        return img_filtered

    def select_red(self, img):
        temp = img.copy()
        mask_1 = cv2.inRange(img, self.hsv_range['red_1'][0], self.hsv_range['red_1'][1])
        mask_2 = cv2.inRange(temp, self.hsv_range['red_2'][0], self.hsv_range['red_2'][1])
        img_filtered = mask_1 + mask_2
        return img_filtered

    def find_max_circle():
        pass
    
    def find_circles(self,Raw_img,img_filtered,Depth_or_HSV_Flag):
        '''传入HSV红色滤波后的img，然后开运算，然后霍夫找圆（设置最大最小半径条件）取得圆心。'''
        if (Depth_or_HSV_Flag == 'Depth'):
            circles = cv2.HoughCircles(img_filtered, cv2.HOUGH_GRADIENT, 1, minDist = 50,
                            param1=30, param2=30, minRadius=15, maxRadius = 255)
        else:
            circles = cv2.HoughCircles(img_filtered, cv2.HOUGH_GRADIENT, 1, minDist = 50,
                            param1=40, param2=100, minRadius=15, maxRadius = 255)
        circles = np.array(circles)
        show_circle = Raw_img.copy()
        if circles.any():
            circles = np.uint16(np.around(circles))
            index = circles[0][:,2].argmax()
            max_circle = circles[0][index]
            for i in circles[0,:]:
                cv2.circle(show_circle, (i[0],i[1]),i[2],(255,255,255) ,2)  #画圆
                cv2.circle(show_circle, (i[0], i[1]),2, (255,255,255) ,3)   #点圆心
            return show_circle,circles,max_circle
        else:
            print('No circles found')
            max_circle = None 
            return show_circle,circles,max_circle

class ImgHandler(Filter):
    def __init__(self, Vehicle):
        super(ImgHandler, self).__init__()
        self.vehicle = Vehicle
        self.save_count = 0
        self.img_height = 480
        self.img_width = 640
        self.ctrl_attitudes_dict = {
            'task' : 0,
            'roll' : 0,
            'pitch' : 0,
            'yaw' : 0,
            'z' : 0,
            'roll_rate' : 0,
            'pitch_rate' : 0,
            'yaw_rate' : 0,
            'duration' : 0,
            'vx' : 0,
            'vy' : 0,
            'vz' : 0
        }
        self.ctrl_dict_last = {}
        self.last_horizontal_y =0
        # self.PID_z = pid_control.PID(P=0.3,I=0.024,D=0.18) #P=2.5,I=0.1,D=1.8
        # self.PID_vy = pid_control.PID(P=0.4,I=0.03,D=0.23)  #P=2,I=0.2,D=1.5
        # self.PID_landing_x = pid_control.PID(P=0.5,I=0,D=0.3)
        # self.PID_landing_y = pid_control.PID(P=0.5,I=0,D=0.3)
        self.last_landing_x = 0
        self.last_landing_y = 0
        self.FindCircleCount = 0
        self.last_detected_vy = 0
        self.last_attitude_z = -1.7
        # self.kf = KalmanFilter(transition_matrices=np.array([[1,0], [0,1]]),
        #           observation_matrices =np.array([[1,0],[0,1]]),
        #           transition_covariance= 0.2*np.eye(2))


    def kalman_calc(kf,x,y,circle_count_flag):
        global filtered_state_means0,filtered_state_covariances0,lmx,lmy,lpx,lpy
        current_measurement = np.array([np.float32(x),np.float32(y)])
        cmx, cmy = current_measurement[0], current_measurement[1]
        # print(current_measurement)
        if circle_count_flag ==1:
            filtered_state_means0=np.array([x,y])
            filtered_state_covariances0=np.eye(2)
            lmx, lmy = x, y#上次测量位置
            lpx, lpy = x, y#上次预测位置

    
        filtered_state_means, filtered_state_covariances= (kf.filter_update( filtered_state_means0,filtered_state_covariances0,current_measurement))
        cpx,cpy= filtered_state_means[0], filtered_state_means[1]
        
        filtered_state_means0, filtered_state_covariances0=filtered_state_means, filtered_state_covariances
        lpx, lpy = filtered_state_means[0], filtered_state_means[1]
        lmx, lmy =current_measurement[0], current_measurement[1]
        return cpx,cpy

    def get_img_task(self, hsv=False):
        '''This function will fetch a image and transfer to cv2 array type.'''
        rawImage = self.vehicle.client.simGetImage("0", airsim.ImageType.Scene)
        rgb_img = cv2.imdecode(airsim.string_to_uint8_array(rawImage), cv2.IMREAD_UNCHANGED)
        if hsv:
            hsv_img = cv2.cvtColor(rgb_img, cv2.COLOR_BGR2HSV)
            return hsv_img
        else:
            return rgb_img

    def get_Down_img_task(self, hsv=False):
        '''This function will fetch a image and transfer to cv2 array type.'''
        rawImage = self.vehicle.client.simGetImage(3, airsim.ImageType.Scene)
        rgb_img = cv2.imdecode(airsim.string_to_uint8_array(rawImage), cv2.IMREAD_UNCHANGED)
        if hsv:
            hsv_img = cv2.cvtColor(rgb_img, cv2.COLOR_BGR2HSV)
            return hsv_img
        else:
            return rgb_img

    def get_Depthimg_task(self,camera):
        '''This function will fetch a depth image and transfer to np.ndarray type.'''
        responses = self.vehicle.client.simGetImages([airsim.ImageRequest(camera, airsim.ImageType.DepthPerspective, True)])
        DepthImg = airsim.get_pfm_array(responses[0])

        # Some preprocessing for the depth image
        DepthImg[DepthImg>8] = 0
        DepthImg = DepthImg.astype(np.uint8)
        DepthImg = cv2.equalizeHist(DepthImg)
        print("读取成功")
        return DepthImg

    def processing_img_task(self,Raw_img,Binary_img,Depth_img):
        kernel = np.ones((5,5),np.uint8)
        opening = cv2.morphologyEx(Binary_img, cv2.MORPH_OPEN, kernel)
        Depth_or_HSV_Flag ='Depth'
        img_circles, circles, max_circle = self.find_circles(Depth_img,Depth_img,Depth_or_HSV_Flag)
        print ('circle_count = %d'%self.FindCircleCount)

        if max_circle is not None:
            # if (max_circle[2]>65):
            #     self.ctrl_attitudes_dict['task'] = 'flyFowardbyVelocity'
            #     self.ctrl_attitudes_dict['vy'] = 0
            #     self.ctrl_attitudes_dict['vz'] = 0
            #     self.ctrl_attitudes_dict['vx'] = -4
            #     self.ctrl_attitudes_dict['duration'] = 0.3
            # else:
            self.FindCircleCount += 1
            print(max_circle)
            vertical = float((220 - max_circle[1])*0.03)
            holrizontal = float(320 - max_circle[0])*0.03

            expected_vy = 320 - max_circle[0]

            if self.FindCircleCount ==1:
                detected_vy = 0
            else:
                detected_vy = max_circle[0] - self.last_horizontal_y
                if detected_vy>10:  #如果圆心位置突变，放弃速度判断。
                    detected_vy = self.last_detected_vy

            outputZ = self.PID_z.update(vertical)
            output_vy = self.PID_vy.update((expected_vy - detected_vy)*0.05)
            self.last_horizontal_y = max_circle[0]  #记录上次的y值。
            self.last_detected_vy = detected_vy
            '''Passing control commands'''
            self.ctrl_attitudes_dict['task'] = 'flyFowardbyZVelocity'
            self.ctrl_attitudes_dict['roll'] = -holrizontal
            self.ctrl_attitudes_dict['pitch'] = 0.1
            self.ctrl_attitudes_dict['yaw'] = 0
            self.ctrl_attitudes_dict['yaw_rate'] = 0
            self.ctrl_attitudes_dict['z'] = self.last_attitude_z - outputZ
            self.ctrl_attitudes_dict['duration'] = 0.1

            self.ctrl_attitudes_dict['vx'] = -0.5
            self.ctrl_attitudes_dict['vy'] = output_vy
            print('out y = %f'%output_vy)
            print('out z = %f'%self.ctrl_attitudes_dict['z'])
            print('radius = %f'%max_circle[2])
                # self.ctrl_attitudes_dict['vz'] = - vertical

        else:
            self.FindCircleCount = 0
            self.last_horizontal_y =0
            print('Go straight to find a circle')
            # self.ctrl_attitudes_dict = self.ctrl_dict_last  #保持上一次路径?或者直接让无人机朝着白色标志飞?
            self.ctrl_attitudes_dict['task'] = 'flyFowardbyVelocity'
            self.ctrl_attitudes_dict['vy'] = -0.1
            self.ctrl_attitudes_dict['vz'] = 0
            self.ctrl_attitudes_dict['vx'] = -3.5
            self.ctrl_attitudes_dict['duration'] = 0.2


        state = self.vehicle.client.getMultirotorState()
        height_z = state.kinematics_estimated.position.z_val
        self.last_attitude_z = height_z #记录上次的高度，用于PID对准高度默认值
    
        self.save_img_task(Depth_img,Raw_img,img_circles)
        self.ctrl_dict_last = self.ctrl_attitudes_dict
        return self.ctrl_attitudes_dict


    def processing_depthIMG_task_1(self,Depth_img):
        Depth_or_HSV_Flag = 'Depth'
        img_circles, circles, max_circle = self.find_circles(Depth_img,Depth_img,Depth_or_HSV_Flag)
        if max_circle is not None:
            self.FindCircleCount += 1
            print(max_circle)
            vertical = float((220 - max_circle[1])*0.03)
            holrizontal = float(320 - max_circle[0])*0.03
            expected_vy = 320 - max_circle[0]

            if self.FindCircleCount ==1:
                detected_vy = 0
            else:
                detected_vy = max_circle[0] - self.last_horizontal_y
                if detected_vy>15:  #如果圆心位置突变，放弃速度判断。
                    detected_vy = self.last_detected_vy

            outputZ = self.PID_z.update(vertical)
            output_vy = self.PID_vy.update((expected_vy - detected_vy)*0.05)
            self.last_horizontal_y = max_circle[0]  #记录上次的y值。
            self.last_detected_vy = detected_vy
            '''Passing control commands'''
            self.ctrl_attitudes_dict['task'] = 'flyFowardbyZVelocity'
            self.ctrl_attitudes_dict['z'] = self.last_attitude_z - outputZ
            self.ctrl_attitudes_dict['duration'] = 0.1

            self.ctrl_attitudes_dict['vx'] = output_vy  #先往y方向飞
            self.ctrl_attitudes_dict['vy'] = 0.8
            print('out y = %f'%output_vy)
            print('out z = %f'%self.ctrl_attitudes_dict['z'])

        else:   #没找到圆
            self.last_horizontal_y =0
            self.FindCircleCount = 0
            print('Go straight!')
            # self.ctrl_attitudes_dict = self.ctrl_dict_last  #保持上一次路径?或者直接让无人机朝着白色标志飞?
            self.ctrl_attitudes_dict['task'] = 'flyFowardbyVelocity'
            self.ctrl_attitudes_dict['vy'] = 2
            self.ctrl_attitudes_dict['vz'] = 0
            self.ctrl_attitudes_dict['vx'] = 0
            self.ctrl_attitudes_dict['duration'] = 0.3

        state = self.vehicle.client.getMultirotorState()
        height_z = state.kinematics_estimated.position.z_val
        self.last_attitude_z =height_z
        self.ctrl_dict_last = self.ctrl_attitudes_dict
        return self.ctrl_attitudes_dict

    def processing_depthIMG_ring_4(self,Depth_img):
        img_circles, circles, max_circle = self.find_circles(Depth_img,Depth_img,'Depth')
        if max_circle is not None:
            self.FindCircleCount += 1
            print(max_circle)
            z_predict,y_predict = self.kalman_calc(self.kf,max_circle[1],max_circle[0],self.FindCircleCount)

            vertical = float((220 - z_predict)*0.03)
            holrizontal = float(320 - y_predict)*0.03
            expected_vy = 320 - y_predict

            if self.FindCircleCount ==1:
                detected_vy = 0
            else:
                detected_vy = max_circle[0] - self.last_horizontal_y
                if detected_vy>15:  #如果圆心位置突变，放弃速度判断。
                    detected_vy = self.last_detected_vy

            outputZ = self.PID_z.update(vertical)
            output_vy = self.PID_vy.update((expected_vy - detected_vy)*0.05)
            self.last_horizontal_y = max_circle[0]  #记录上次的y值。
            self.last_detected_vy = detected_vy
            '''Passing control commands'''
            self.ctrl_attitudes_dict['task'] = 'flyFowardbyZVelocity'
            self.ctrl_attitudes_dict['z'] = self.last_attitude_z - outputZ
            self.ctrl_attitudes_dict['duration'] = 0.1

            self.ctrl_attitudes_dict['vx'] = -0.8
            self.ctrl_attitudes_dict['vy'] = output_vy
            print('out y = %f'%output_vy)
            print('out z = %f'%self.ctrl_attitudes_dict['z'])

        else:   #没找到圆
            self.last_horizontal_y =0
            self.FindCircleCount = 0
            print('Go straight!')
            # self.ctrl_attitudes_dict = self.ctrl_dict_last  #保持上一次路径?或者直接让无人机朝着白色标志飞?
            self.ctrl_attitudes_dict['task'] = 'flyFowardbyVelocity'
            self.ctrl_attitudes_dict['vy'] = -0.1
            self.ctrl_attitudes_dict['vz'] = 0
            self.ctrl_attitudes_dict['vx'] = -3
            self.ctrl_attitudes_dict['duration'] = 0.3

        state = self.vehicle.client.getMultirotorState()
        height_z = state.kinematics_estimated.position.z_val
        self.last_attitude_z =height_z
        self.ctrl_dict_last = self.ctrl_attitudes_dict
        return self.ctrl_attitudes_dict

    def processing_depthIMG_task_ring_3(self,Depth_img):
        Depth_or_HSV_Flag = 'Depth'
        img_circles, circles, max_circle = self.find_circles(Depth_img,Depth_img,Depth_or_HSV_Flag)
        if max_circle is not None:
            self.FindCircleCount += 1
            print(max_circle)
            vertical = float((220 - max_circle[1])*0.03)
            holrizontal = float(320 - max_circle[0])*0.03
            expected_vy = 320 - max_circle[0]

            if self.FindCircleCount ==1:
                detected_vy = 0
            else:
                detected_vy = max_circle[0] - self.last_horizontal_y
                if detected_vy>15:  #如果圆心位置突变，放弃速度判断。
                    detected_vy = self.last_detected_vy

            outputZ = self.PID_z.update(vertical)
            output_vy = self.PID_vy.update((expected_vy - detected_vy)*0.05)
            self.last_horizontal_y = max_circle[0]  #记录上次的y值。
            self.last_detected_vy = detected_vy
            '''Passing control commands'''
            self.ctrl_attitudes_dict['task'] = 'flyFowardbyZVelocity'
            self.ctrl_attitudes_dict['z'] = self.last_attitude_z - outputZ
            self.ctrl_attitudes_dict['duration'] = 0.1

            self.ctrl_attitudes_dict['vx'] = output_vy*0.4  #先往y方向飞
            self.ctrl_attitudes_dict['vy'] = output_vy*0.4
            print('out y = %f'%output_vy)
            print('out z = %f'%self.ctrl_attitudes_dict['z'])

        else:   #没找到圆
            self.last_horizontal_y =0
            self.FindCircleCount = 0
            print('Go straight!')
            # self.ctrl_attitudes_dict = self.ctrl_dict_last  #保持上一次路径?或者直接让无人机朝着白色标志飞?
            self.ctrl_attitudes_dict['task'] = 'flyFowardbyVelocity'
            self.ctrl_attitudes_dict['vy'] = 2
            self.ctrl_attitudes_dict['vz'] = 0
            self.ctrl_attitudes_dict['vx'] = -4
            self.ctrl_attitudes_dict['duration'] = 0.3

        state = self.vehicle.client.getMultirotorState()
        height_z = state.kinematics_estimated.position.z_val
        self.last_attitude_z =height_z
        self.ctrl_dict_last = self.ctrl_attitudes_dict
        return self.ctrl_attitudes_dict

    def processing_landing(self,Down_img):
        binary = cv2.inRange(Down_img, self.hsv_range['white'][0],self.hsv_range['white'][1])
        location = np.where(binary>1)
        detected_x = np.mean(location[0])
        detected_y = np.mean(location[1])
        expected_vx = 320 - detected_x
        expected_vy = 240 - detected_y

        detected_vx = detected_x - self.last_landing_x
        detected_vy = detected_y - self.last_landing_y

        output_vx = self.PID_landing_x.update((expected_vx - detected_vx)*0.0005)
        output_vy = self.PID_landing_y.update((expected_vy - detected_vy)*0.0005)
        self.last_landing_x= detected_x  #记录上次的坐标值。
        self.last_landing_y= detected_y
        '''Passing control commands'''
        self.ctrl_attitudes_dict['task'] = 'flyFowardbyVelocity'
        self.ctrl_attitudes_dict['vz'] = 0.3
        self.ctrl_attitudes_dict['duration'] = 0.2

        self.ctrl_attitudes_dict['vx'] = -output_vy
        self.ctrl_attitudes_dict['vy'] = output_vx  #注意图像的x,y和世界坐标x，y不同。
        print('out x = %f'%(-output_vy))
        print('out y = %f'%output_vx)

        print((detected_x,detected_y))
        # cv2.circle(binary, (detected_x, detected_y), 2 , (0,0,0) ,3)
        self.save_an_img_task(binary)
        return self.ctrl_attitudes_dict

    def processing_HSVImg_task_1(self,Binary_img):
        kernel = np.ones((5,5),np.uint8)
        opening = cv2.morphologyEx(Binary_img, cv2.MORPH_OPEN, kernel)
        Depth_or_HSV_Flag = 'HSV'
        img_circles, circles, max_circle = self.find_circles(opening,opening,Depth_or_HSV_Flag)

        if max_circle is not None:
            if (max_circle[2]>65):
                self.ctrl_attitudes_dict['task'] = 'flyFowardbyVelocity'
                self.ctrl_attitudes_dict['vy'] = 2
                self.ctrl_attitudes_dict['vz'] = 0
                self.ctrl_attitudes_dict['vx'] = 0
                self.ctrl_attitudes_dict['duration'] = 0.3
            else:
                self.FindCircleCount += 1
                print(max_circle)
                vertical = float((220 - max_circle[1])*0.03)
                holrizontal = float(320 - max_circle[0])*0.03

                expected_vy = 320 - max_circle[0]

                if self.FindCircleCount ==1:
                    detected_vy = 0
                else:
                    detected_vy = max_circle[0] - self.last_horizontal_y
                    if detected_vy>10:  #如果圆心位置突变，放弃速度判断。
                        detected_vy = self.last_detected_vy

                outputZ = self.PID_z.update(vertical)
                output_vy = self.PID_vy.update((expected_vy - detected_vy)*0.05)
                self.last_horizontal_y = max_circle[0]  #记录上次的y值。
                self.last_detected_vy = detected_vy
                '''Passing control commands'''
                self.ctrl_attitudes_dict['task'] = 'flyFowardbyZVelocity'
                self.ctrl_attitudes_dict['z'] = self.last_attitude_z - outputZ
                self.ctrl_attitudes_dict['duration'] = 0.1
                self.ctrl_attitudes_dict['vx'] = -0.8
                self.ctrl_attitudes_dict['vy'] = output_vy
                print('out y = %f'%output_vy)
                print('out z = %f'%self.ctrl_attitudes_dict['z'])
                print('radius = %f'%max_circle[2])
                # self.ctrl_attitudes_dict['vz'] = - vertical

        else:
            self.last_horizontal_y =0
            self.FindCircleCount = 0
            print('Go straight to find a circle')
            # self.ctrl_attitudes_dict = self.ctrl_dict_last  #保持上一次路径?或者直接让无人机朝着白色标志飞?
            self.ctrl_attitudes_dict['task'] = 'flyFowardbyVelocity'
            self.ctrl_attitudes_dict['vy'] = 2
            self.ctrl_attitudes_dict['vz'] = 0
            self.ctrl_attitudes_dict['vx'] = -2
            self.ctrl_attitudes_dict['duration'] = 0.3


        state = self.vehicle.client.getMultirotorState()
        height_z = state.kinematics_estimated.position.z_val
        self.last_attitude_z = height_z #记录上次的高度，用于PID对准高度默认值

        self.ctrl_dict_last = self.ctrl_attitudes_dict
        return self.ctrl_attitudes_dict


    def save_img_task(self, depth,Raw_img,img_circles):
        self.save_count += 1 
        current_path = os.path.dirname(__file__)
        image_folder = os.path.join(current_path, 'SavedImages')
        save_path = image_folder + '/DepthImg_{}.png'.format(str(self.save_count))
        save_path2 = image_folder + '/RawImg_{}.png'.format(str(self.save_count))
        save_path3 = image_folder + '/CircleImg_{}.png'.format(str(self.save_count))
        cv2.imwrite(save_path,depth)
        if img_circles is not None:
            cv2.imwrite(save_path2,Raw_img)
            cv2.imwrite(save_path3,img_circles)
        return

    def save_an_img_task(self, Img):
        self.save_count += 1 
        current_path = os.path.dirname(__file__)
        image_folder = os.path.join(current_path, 'SavedImages')
        save_path = image_folder + '/TestImg_{}.png'.format(str(self.save_count))

        cv2.imwrite(save_path,Img)
        return