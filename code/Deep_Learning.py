import torch

class Mynet(torch.nn.Module):
    def __init__(self):
        super().__init__()
        #实际上就是一个组合
        self.Mymodule = torch.nn.Sequential(
            torch.nn.Conv2d(in_channels=3, out_channels=32, kernel_size=5, padding=2),
            torch.nn.MaxPool2d(2),
            torch.nn.Sigmoid(),
            torch.nn.Conv2d(in_channels=32, out_channels=32, kernel_size=5, padding=2),
            torch.nn.MaxPool2d(2),
            torch.nn.Sigmoid(),
            torch.nn.Conv2d(in_channels=32, out_channels=64, kernel_size=5, padding=2),
            torch.nn.MaxPool2d(2),
            torch.nn.Sigmoid(),
            torch.nn.Flatten(),
            torch.nn.Linear(64*4*4, 64),
            torch.nn.Linear(64, 8)
        )
        self.mls = torch.nn.MSELoss()
        self.opt = torch.optim.Adam(self.parameters(), lr = 0.001)

    def forward(self, input):
        output = self.Mymodule(input)
        return output

# 一般在这里验证网络的正确性
if __name__ == "__main__":
    Test = Mynet()
    input = torch.ones((1, 3, 32, 32))  #创建一个tensor
    print(input.shape)
    output = Test(input)
    print(output.shape)