'''检测圆心函数'''
import cv2
import numpy
import os

def circle_center():
    pass

for i in range(len(os.listdir("./img/Depth"))):
    img = cv2.imread('./img/Depth/{}.jpg'.format(i), cv2.IMREAD_GRAYSCALE)
    img_RGB = cv2.imread('./img/RGB/{}.jpg'.format(i), cv2.IMREAD_COLOR)
    circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, minDist = 30, param1=30, param2=30, minRadius=15, maxRadius = 255)
    if not circles is None:
        for j in circles[0]:
            cv2.circle(img_RGB,(int(j[0]),int(j[1])),int(j[2]),(0,255,0),2)#第二参数（）内是圆心坐标，第三参数是半径，第四参数（）内是颜色，第五参数是线条粗细
            cv2.circle(img_RGB,(int(j[0]),int(j[1])),2,(0,0,255),3)
        print("第{}张图有{}个圆。".format(i, len(circles[0])))
    cv2.imwrite('./img/Test/{}.jpg'.format(i), img_RGB, [int(cv2.IMWRITE_PNG_COMPRESSION), 3])



'''---------------------------------------------------------------------------------------------------------------------------------'''
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

# print("圆的个数是：")
# print(len(P))

# for i in P:
#     r=int(i[2])
#     x=int(i[0])
#     y=int(i[1])
#     print("圆心坐标为：",(x,y))
#     print("圆的半径是：",r)

# cv2.imshow('test', img)

# cv2.waitKey(0)
# cv2.destroyAllWindows()
'''---------------------------------------------------------------------------------------------------------------------------------'''