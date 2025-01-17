from torchvision.datasets import ImageFolder
from torchvision import transforms
from random import randint
import torch
from torchvision import io
from torch.utils.data import DataLoader
from torch.utils.data import Dataset


def idxPrepare(path):
    # 有关类别编号的预处理
    dataset = ImageFolder(path, transform=transforms.Compose([transforms.Resize((45,45)),transforms.ToTensor()]))
    class2idx = dataset.class_to_idx
    idx2class = {key: value for value, key in class2idx.items()}
    torch.save(class2idx, './class2idx')  # 保存字典——{类别:索引}
    torch.save(idx2class, './idx2class')  # 保存字典——{索引:类别}
    # 返回元组(图片地址, 类别)组成的列表
    return dataset.imgs


def image2txt(path_idx, r=1):
    # 划分训练数据和测试数据并将图片路径和类别标签放到txt文件中
    train = open('./train.txt', 'w')
    test = open('./test.txt', 'w')
    for path, idx in path_idx:
        file = path + " " + str(idx) + '\n'
        if randint(0, 10) >= r:
            train.write(file)
        else:
            test.write(file)

    train.close()
    test.close()


def MyLoader(path):
    # 加载图片
    return io.read_image(path)


class MyData(Dataset):
    # 数据加载器
    def __init__(self, txt, transform=None, target_transform=None, loader=MyLoader):
        imgs = []
        with open(txt) as f:
            for line in f.readlines():
                line = line.strip('\n')  # 移除字符串首尾的换行符
                line = line.rstrip()  # 删除末尾空
                words = line.split(' ')  # 以空格为分隔符 将字符串分成
                if line.count(' ')==1:
                    imgs.append((words[0], int(words[1])))  # imgs中包含有图像路径和标签
                elif line.count(' ')==2:
                    x1 = words[0]+' '+words[1]
                    x2 = words[2]
                    imgs.append((words[0]+' '+words[1],int(words[2])))
        self.imgs = imgs
        self.transform = transform
        self.target_transform = target_transform
        self.loader = loader

    def __getitem__(self, index):
        fn, label = self.imgs[index]
        img = self.loader(fn)
        if self.transform is not None:
            img = self.transform(img)

        if self.target_transform is not None:
            label = self.target_transform(label)
        return img.type(torch.float32), label

    def __len__(self):
        return len(self.imgs)


def LoadDataset(data_path, batch_size, img_size):
    # 加载数据
    path_idx = idxPrepare(data_path)
    # 生成txt文件，分割训练集和测试集
    image2txt(path_idx, 1)

    train_set = MyData('train.txt', transform=transforms.Resize(img_size))
    train_iter = DataLoader(train_set, batch_size=batch_size, shuffle=True)
    test_set = MyData('test.txt', transform=transforms.Resize(img_size))
    test_iter = DataLoader(test_set, batch_size=batch_size)

    return train_iter, test_iter
