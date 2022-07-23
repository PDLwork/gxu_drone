'''该代码用于测试深度强化学习训练后效果'''

import sys
sys.path.append(sys.argv[0].rstrip('ethod1_DQN/verify.py').rstrip('/m'))  #这一系列的操作是为了能导入上一级的包
import Deep_Learning
import torch
import Drone_control
import Reinforcement_Learning
import torchvision

transform2tensor = torchvision.transforms.Compose([
        torchvision.transforms.ToTensor(),
        torchvision.transforms.Resize((32, 32))
        ])

if __name__ == "__main__":
    net = Deep_Learning.Mynet()     # 创建深度学习网络
    net.load_state_dict(torch.load('mynet.pth'))
    MyDrone = Drone_control.DroneControler()    #创建无人机对象

    RL_frame = Reinforcement_Learning.frame(MyDrone)   #创建强化学习框架
    loss_function = torch.nn.MSELoss()

    done = False
    MyDrone.initFly()
    MyDrone.Move2position(-0.5, 3, -2.5, 2)     #第一个圈起点
    # MyDrone.Move2position(1.3, 10, -0.5, 2)     #第2个圈起点

    while not done:
        state = MyDrone.get_img("RGB")
        img = transform2tensor(state)     #有警告
        state = torch.reshape(img, (1, 3, 32, 32))

        with torch.no_grad():
            output = net(state)
            print(output)
        action = output.argmax(1) # 根据输入S得到输出动作

        next_state, reward, done = RL_frame.take_action(action)