'''该文件用于双线程的时候作为另一个程序不断连续采集图片'''

import airsim
import numpy
import cv2

def save_image(responses, prefix = ""):
    response = responses[0]

    # frombuffer将data以流的形式读入转化成ndarray对象 这一步只得到一个一维数组
    buffer = numpy.frombuffer(response.image_data_uint8, dtype=numpy.uint8) 

    # reshape把1维数组对应通道数组RGB：3*h*w  depth：1*h*w
    img_rgb = buffer.reshape(response.height, response.width, -1)
    # 保存图片
    cv2.imwrite('./img/RGB/'+str(prefix)+'.jpg', img_rgb)

    # 得到灰度图
    # img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
    # cv2.imwrite('./img/Grayscale/'+str(prefix)+'.jpg', img_gray)

    #得到深度图（有BUG先不管，不要使用，保存方式不对？）
    # response = responses[1]
    # buffer = numpy.frombuffer(response.image_data_uint8, dtype=numpy.uint8) 
    # img_depth = buffer.reshape(response.height, response.width, -1)
    # cv2.imwrite('./img/Depth/'+str(prefix)+'.jpg', img_depth)

    # return img_gray

if __name__ == "__main__":
    #创建对象与无人机建立连接，用于获取图片
    client_get_picture = airsim.MultirotorClient()   # 与airsim创建链接
    client_get_picture.confirmConnection()   # 查询是否建立连接
    client_get_picture.enableApiControl(True)   # 打开API控制权
    # client_get_picture.armDisarm(True)   # 解锁

    i = 0
    while i < 100:
        responses = client_get_picture.simGetImages([
            airsim.ImageRequest("0", airsim.ImageType.Scene, False, False),
            airsim.ImageRequest("0", airsim.ImageType.DepthPerspective, True, False)
            ])
        save_image(responses, i)
        i += 1

    print("调试结束！") 