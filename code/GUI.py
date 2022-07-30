'''用户交互页面'''

import tkinter
import numpy

#GUI页面设计
class GUI_Design():
    def __init__(self, client):
        self.window = tkinter.Tk()
        self.client = client

        #定义按钮并放置
        Button_Turn_left = tkinter.Button(self.window,\
                                text='↖',\
                                font=('Arial', 12),\
                                width=10,\
                                height=1,\
                                command=self.Turn_left)
        Button_Turn_left.pack()

        Button_Turn_Right = tkinter.Button(self.window,\
                        text='↗',\
                        font=('Arial', 12),\
                        width=10,\
                        height=1,\
                        command=self.Turn_Right)
        Button_Turn_Right.pack()

        Button_Forward = tkinter.Button(self.window,\
                        text='↑',\
                        font=('Arial', 12),\
                        width=10,\
                        height=1,\
                        command=self.Forward)
        Button_Forward.pack()

        Button_Backward = tkinter.Button(self.window,\
                        text='↓',\
                        font=('Arial', 12),\
                        width=10,\
                        height=1,\
                        command=self.Backward)
        Button_Backward.pack()

        Button_Left = tkinter.Button(self.window,\
                        text='←',\
                        font=('Arial', 12),\
                        width=10,\
                        height=1,\
                        command=self.Left)
        Button_Left.pack()

        Button_Right = tkinter.Button(self.window,\
                        text='→',\
                        font=('Arial', 12),\
                        width=10,\
                        height=1,\
                        command=self.Right)
        Button_Right.pack()

        Button_Up = tkinter.Button(self.window,\
                        text='Up',\
                        font=('Arial', 12),\
                        width=10,\
                        height=1,\
                        command=self.Up)
        Button_Up.pack()

        Button_Down = tkinter.Button(self.window,\
                        text='Down',\
                        font=('Arial', 12),\
                        width=10,\
                        height=1,\
                        command=self.Down)
        Button_Down.pack()

        self.window.update()

    #按下不同按钮执行不同动作
    def Turn_left(self):
        x, y, z, roll, pitch, yaw = self.client.get_position()
        target_yaw = yaw - numpy.pi/18
        self.client.change_Yaw(0, 0, -target_yaw, 0.6, 1)
    def Turn_Right(self):
        x, y, z, roll, pitch, yaw = self.client.get_position()
        target_yaw = yaw + numpy.pi/18
        self.client.change_Yaw(0, 0, -target_yaw, 0.6, 1)
    def Forward(self):
        self.client.MoveByDroneSpeed(1, 0, 0, 5)
        # self.client.save_img("Bottom")
    def Backward(self):
        self.client.MoveByDroneSpeed(-1, 0, 0, 5)
    def Left(self):
        self.client.MoveByDroneSpeed(0, -1, 0, 3)
    def Right(self):
        self.client.MoveByDroneSpeed(0, 1, 0, 3)
    def Up(self):
        self.client.MoveByDroneSpeed(0, 0, -1, 0.5)
    def Down(self):
        self.client.MoveByDroneSpeed(0, 0, 1, 0.5)
    

    def keep(self):
        self.window.mainloop()      #循环显示窗口

if __name__ == "__main__":
    Window = GUI_Design(1)
    Window.keep()
