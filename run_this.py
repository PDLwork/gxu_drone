import airsim
import numpy
import cv2
import time

# import LGMD_tool

'''-------------------------初始参数设计-------------------------'''
sigma_E = 1.5
sigma_I = 5
r = 6
a = 1.2
alfa = -0.1
beta = 0.5
lamda = 0.7

# 定义一个保存图片的函数，保存rgb和灰度图
# 输入的是读取相机的数据和保存图片的索引
def save_image(responses, prefix = ""):
    response = responses[0]

    # frombuffer将data以流的形式读入转化成ndarray对象 这一步只得到一个一维数组
    buffer = numpy.frombuffer(response.image_data_uint8, dtype=numpy.uint8) 

    # reshape把1维数组改为三维数组（得到三通道的RGB图像）
    img_rgb = buffer.reshape(response.height, response.width, -1)
    # 得到灰度图
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)

    # 保存图片
    cv2.imwrite('./img/RGB/'+str(prefix)+'.jpg', img_rgb)
    cv2.imwrite('./img/Grayscale/'+str(prefix)+'.jpg', img_gray)

    return img_gray

    '''
    # plt展示图片
    matplotlib.pyplot.subplot(121)
    matplotlib.pyplot.title('RGB image')
    matplotlib.pyplot.axis('off')
    img_rgb = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)
    matplotlib.pyplot.imshow(img_rgb)
    matplotlib.pyplot.subplot(122)
    matplotlib.pyplot.title('Grayscale image')
    matplotlib.pyplot.axis('off')
    matplotlib.pyplot.imshow(img_gray, cmap='gray')
    matplotlib.pyplot.show(block = False)      # 垃圾函数  设计得一点都不好
    # matplotlib.pyplot.ion()     # 可交互
    matplotlib.pyplot.pause(0.01)   #给他反应时间？
    '''

#传输数据跑LGMD
def run_LGMD(img3, img2, img1, img0, kernel_E, kernel_I_delay1, kernel_I_delay2, prefix = ""):
    #可以修改但目前这样有助于理解
    #求差分图的绝对值
    img_diff2 = abs(img3 - img2)
    img_diff1 = abs(img2 - img1)
    img_diff0 = abs(img1 - img0)

    #卷积
    Layer_E = LGMD_tool.Convolution_same(img_diff2, kernel_E, r)
    Layer_I_delay1 = LGMD_tool.Convolution_same(img_diff1, kernel_I_delay1, r)
    Layer_I_delay2 = LGMD_tool.Convolution_same(img_diff0, kernel_I_delay2, r)
    Layer_I = Layer_I_delay1 + Layer_I_delay2

    #得到S层输出并处理
    Layer_S = Layer_E - Layer_I
    n, m = Layer_S.shape
    for i in range(n):
        for j in range(m):
            if Layer_S[i][j]<0:
                Layer_S[i][j]=0
    
    cv2.imwrite('./img/LGMD/'+str(prefix)+'.jpg', Layer_S)

if __name__ == "__main__":
    #运行代码得到卷积核
    kernel_E, kernel_I_delay1, kernel_I_delay2 = LGMD_tool.create_kernel(sigma_E, sigma_I, r, a, alfa, beta, lamda)

    #创建对象与无人机建立连接，用于获取图片
    client_get_picture = airsim.MultirotorClient()   # 与airsim创建链接
    client_get_picture.confirmConnection()   # 查询是否建立连接
    client_get_picture.enableApiControl(True)   # 打开API控制权
    client_get_picture.armDisarm(True)   # 解锁

    #先获取4张图片
    responses = client_get_picture.simGetImages([airsim.ImageRequest("0", airsim.ImageType.Scene, False, False)])   # 每一个的参数：相机名称，图像类型，是否浮点数，是否压缩图像（默认压缩）
    img0 = save_image(responses, 0)
    responses = client_get_picture.simGetImages([airsim.ImageRequest("0", airsim.ImageType.Scene, False, False)])   # 每一个的参数：相机名称，图像类型，是否浮点数，是否压缩图像（默认压缩）
    img1 = save_image(responses, 1)
    responses = client_get_picture.simGetImages([airsim.ImageRequest("0", airsim.ImageType.Scene, False, False)])   # 每一个的参数：相机名称，图像类型，是否浮点数，是否压缩图像（默认压缩）
    img2 = save_image(responses, 2)
    responses = client_get_picture.simGetImages([airsim.ImageRequest("0", airsim.ImageType.Scene, False, False)])   # 每一个的参数：相机名称，图像类型，是否浮点数，是否压缩图像（默认压缩）
    img3 = save_image(responses, 3)
    # run_LGMD(img3, img2, img1, img0, kernel_E, kernel_I_delay1, kernel_I_delay2, 3)

    i = 4
    while True:
        responses = client_get_picture.simGetImages([airsim.ImageRequest("0", airsim.ImageType.Scene, False, False)])   # 每一个的参数：相机名称，图像类型，是否浮点数，是否压缩图像（默认压缩）
        img0 = img1
        img1 = img2
        img2 = img3
        img3= save_image(responses, i)
        # run_LGMD(img3, img2, img1, img0, kernel_E, kernel_I_delay1, kernel_I_delay2, i)
        i += 1