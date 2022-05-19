import Drone_control
import Deep_Learning
import Reinforcement_Learning
import random
import torch
import torchvision
import time
import numpy

if __name__ == "__main__":
    # if torch.cuda.is_available():
    #     device = torch.device("cuda")   #cuda:0
    #     print('系统可以使用GPU训练！\n即将采用GPU训练')
    # else:
    #     device = torch.device("cpu")
    #     print('系统不可以使用GPU训练！\n即将采用CPU训练')

    net = Deep_Learning.Mynet()     #创建深度学习网络
    net_delay = Deep_Learning.Mynet()
    net.load_state_dict(torch.load("mynet"))
    net_delay.load_state_dict(torch.load("mynet"))
    # net = net.to(device)
    # net_delay = net_delay.to(device)

    MyDrone = Drone_control.DroneControler()    #创建无人机对象

    RL_frame = Reinforcement_Learning.frame(MyDrone)   #创建强化学习框架
    loss_function = torch.nn.MSELoss()
    # loss_function = loss_function.to(device)


    store_count = 0
    store_size = 500  # buffer size
    decline = 0.8  # 衰减系数
    learn_time = 0
    update_time = 20
    gama = 0.9  # 学习因子
    batch_size = 64
    wc = 0

    store_state = numpy.zeros((store_size, 3, 32, 32))
    store_action = numpy.zeros(store_size)
    store_next_state = numpy.zeros((store_size, 3, 32, 32))
    store_reward = numpy.zeros(store_size)

    start_study = False



    transform2tensor = torchvision.transforms.Compose([
        torchvision.transforms.ToTensor(),
        torchvision.transforms.Resize((32, 32))
        ])

    for i in range(30):
        print(i)
        MyDrone.initFly()   #初始化飞行
        MyDrone.hover() #悬停

        while True:
            state = MyDrone.get_img("RGB")
            img = transform2tensor(state)     #有警告
            state = torch.reshape(img, (1, 3, 32, 32))
            # state = state.to(device)

            if random.randint(0,100) < 100*(decline**wc):   #一开始随机随着学习次数的增加慢慢的根据Q表（网络的输出）去执行
                action = random.randint(0,7) #随机
            else:
                # net.eval()
                with torch.no_grad():
                    output = net(state)
                    print(output)
                action = output.argmax(1) # 根据输入S得到输出动作

            next_state, reward, done = RL_frame.take_action(action)
            img = transform2tensor(next_state)
            next_state = torch.reshape(img, (1, 3, 32, 32))
            
            # 将值存起来
            store_state[store_count % store_size] = state
            store_action[store_count % store_size] = action
            store_next_state[store_count % store_size] = next_state
            store_reward[store_count % store_size] = reward
            store_count += 1
            print(store_count)

            # 更新状态
            state = next_state

            # 存够这么多样本了就开始学习
            if store_count > store_size:

                if learn_time % update_time == 0:
                    net_delay.load_state_dict(net.state_dict()) #初始把网络1的参数给网络2  相当于复制
                    wc += 1

                index = random.randint(0, store_size - batch_size -1)   #产生范围内的一个随机数？
                batch_state  = torch.Tensor(store_state[index:index + batch_size])
                batch_action  = torch.Tensor(store_action[index:index + batch_size])
                batch_next_state = torch.Tensor(store_next_state[index:index + batch_size])
                batch_reward  = torch.Tensor(store_reward[index:index + batch_size])
                # batch_state = batch_state.to(device)
                # batch_action = batch_action.to(device)
                # batch_next_state = batch_next_state.to(device)
                # batch_reward = batch_reward.to(device)

                # 更新Q表
                # Q_table = net(batch_state).gather(1, batch_action)  #???
                # Q_table_next = net_delay(batch_next_state).detach().max(1)[0].reshape(batch_size, 1)   #detach用于冻结梯度
                # target_Q_table = batch_reward + gama * Q_table_next
                Q_table = net(batch_state).max(1)[0].reshape(batch_size, 1) #???
                Q_table_next = net_delay(batch_next_state).detach().max(1)[0].reshape(batch_size, 1)   #detach用于冻结梯度
                target_Q_table = batch_reward + gama * Q_table_next

                # 更新网络参数
                loss = loss_function(Q_table, target_Q_table)
                net.opt.zero_grad()
                loss.backward()
                net.opt.step()

                learn_time += 1

                if not start_study:
                    print('start study')
                    start_study = True
                    break

            if done:
                MyDrone.rest()
                time.sleep(2)
                break
    torch.save(net_delay.state_dict(), "mynet")



    # MyDrone.initFly()   #初始化飞行
    # MyDrone.MoveByDroneSpeed(0, 1, 0, 1.5)
    # MyDrone.Move2position(-1, 10, -3, 2)
    # # MyDrone.change_Yaw(0, 0, -(numpy.pi/2), 0.5, 4)
    # MyDrone.change_Yaw(0, 0, (numpy.pi/2), 0.5, 2)
    # # MyDrone.MoveByDroneSpeed(0, 1, 0, 5)
    # MyDrone.hover() #悬停
    # # MyDrone.rest()
    # # MyDrone.get_img("RGB")
    # MyDrone.hover()
    # time.sleep(5)
    # MyDrone.get_position()
    # time.sleep(5)
    # MyDrone.Move2position(0, 0, -2, 2)
    # time.sleep(5)
    # MyDrone.Move2position(-1, 10, -3, 2)
    # MyDrone.rest()
    # MyDrone.landing()
    # MyDrone.end_fly()


    print("----------测试完成！----------")