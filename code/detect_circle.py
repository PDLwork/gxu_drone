'''检测圆心函数，（检测是否过圆）'''
import cv2
import numpy
import os

class get_ciecle():
    def __init__(self):
        self.Flag = False       #当前是否存在圆,要具有一定容错性。存在即True
        self.center_x = None
        self.center_y = None

"""检测圆心函数。检测当前向前摄像头，检测到圆心则返回圆心坐标，否则返回False"""
def circle_center(img):
    circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 100, param1=None, param2=40, minRadius=30, maxRadius=300)
    if not circles is None:
        if len(circles[0]) == 1:    #检测到一个圆
            print("当前检测到1个圆。圆心坐标为：{}，{}。".format(int(circles[0][0][0]), int(circles[0][0][1])))
            return int(circles[0][0][0]), int(circles[0][0][1])
        else:   #检测到多个圆，返回最大的圆心坐标
            center_A = int(circles[0][0][0])
            center_B = int(circles[0][0][1])
            center_C = circles[0][0][2]
            for j in circles[0]:
                if j[2] > center_C:
                    center_C = j[2]
                    center_A = int(j[0])
                    center_B = int(j[1])
            print("当前检测到{}个圆。最大圆心坐标为：{}，{}。".format(len(circles[0]), center_A, center_B))
            return center_A, center_B
    else:
        print("当前没有检测到圆。")
        return False, False


"""检测受否过圆函数,过圈返回True，没过返回False,还未达到要求。"""
def pass_judgment(img):
    #二值化只保留超过阈值的 关于精度参数还得思考
    for i in range(len(img)):
        for j in range(len(img[0])):
            if img[i][j] < 1:
                img[i][j] = 1
            else:
                img[i][j] = 0
    
    sum1 = 0
    sum2 = 0
    for i in range(len(img)/2):
        for j in range(len(img[0])):
            sum1 += img[i][j]
    for i in range(len(img)/2, len(img)):
        for j in range(len(img[0])):
            sum2 += img[i][j]
    if sum1 > 1000 and sum2 < 100:
        return 1
    if sum2 > 1000 and sum1 < 100:
        return 2


if __name__ == "__main__":
    '''测试参数，给一堆深度图，通过霍夫变换检测深度图，然后在RGB图中画圆并保存'''
    for i in range(len(os.listdir("./img/Depth"))):
        img = cv2.imread('./img/Depth/{}.jpg'.format(i), cv2.IMREAD_GRAYSCALE)
        # flaga, flagb = circle_center(img)
        img_RGB = cv2.imread('./img/RGB/{}.jpg'.format(i), cv2.IMREAD_COLOR)
        circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 100, param1=None, param2=40, minRadius=30, maxRadius=300)
        if not circles is None:
            for j in circles[0]:
                cv2.circle(img_RGB,(int(j[0]),int(j[1])),int(j[2]),(0,255,0),2) #第二参数（）内是圆心坐标，第三参数是半径，第四参数（）内是颜色，第五参数是线条粗细 画圆
                cv2.circle(img_RGB,(int(j[0]),int(j[1])),2,(0,0,255),3) #画圆心
            print("第{}张图有{}个圆。".format(i, len(circles[0])))
        else:
            print("第{}张图没有检测到圆。".format(i))
        cv2.imwrite('./img/Test/{}.jpg'.format(i), img_RGB, [int(cv2.IMWRITE_PNG_COMPRESSION), 3])



'''---------------------------------------------霍夫变换使用方法、相关参数说明-------------------------------------------------------------'''
# img = cv2.imread('picture/1.jpg', cv2.IMREAD_GRAYSCALE)

# circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1 ,300, param1=100, param2=200, minRadius=10, maxRadius=400)#霍夫圆变换
# #第3参数默认为1
# #第4参数表示圆心与圆心之间的距离（太大的话，会很多圆被认为是一个圆）
# #第5参数默认为100
# #第6参数根据圆大小设置(圆越小设置越小，检测的圆越多，但检测大圆会有噪点)
# #第7圆最小半径
# #第8圆最大半径
# circles = numpy.uint16(numpy.around(circles))
# #np.uint16数组转换为16位，0-65535
# #np.around返回四舍五入后的值
 
# P=circles[0]#去掉circles数组一层外括号
# for i in P:
#     # 画出外圆
#     cv2.circle(img,(i[0],i[1]),i[2],(0,255,0),2)#第二参数（）内是圆心坐标，第三参数是半径，第四参数（）内是颜色，第五参数是线条粗细
#     # 画出圆心
#     cv2.circle(img,(i[0],i[1]),2,(0,0,255),3)
'''---------------------------------------------------------------------------------------------------------------------------------'''