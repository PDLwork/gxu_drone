import tkinter

#GUI页面设计
class GUI_Design():
    def __init__(self, Drone):
        self.window = tkinter.Tk()
        self.UAV = Drone

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
        self.UAV.take_action("yaw_left")
    def Turn_Right(self):
        self.UAV.take_action("yaw_Right")
    def Forward(self):
        self.UAV.take_action("forward")
    def Backward(self):
        self.UAV.take_action("backward")
    def Left(self):
        self.UAV.take_action("left")
    def Right(self):
        self.UAV.take_action("right")
    def Up(self):
        self.UAV.take_action("up")
    def Down(self):
        self.UAV.take_action("down")
    

    def keep(self):
        self.window.mainloop()      #循环显示窗口

if __name__ == "__main__":
    Window = GUI_Design(1)
    Window.keep()
