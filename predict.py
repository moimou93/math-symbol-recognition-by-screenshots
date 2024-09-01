from utils.models import select_model
from torchvision import io
import torch
from torchvision import transforms

def imageTransform(img, img_size):
    trans1 = transforms.Resize(img_size)
    trans2 = transforms.Grayscale(num_output_channels=1)
    trans = transforms.Compose([trans1,trans2])
    img = trans(img)

    img = img.float()  # 确保图像是 float 类型
    img = img.unsqueeze(0)
    return img

def getIdxDict():
    return torch.load('idx2class',weights_only=True)

def predictByImage(net, path, img_size):
    net.eval()
    image = io.read_image(path)
    image = imageTransform(image, img_size)  # 应用图像转换
    predict = torch.argmax(net(image), dim=1)
    return int(predict)

def judge(path):
    in_channels = 1  # 输入通道数
    num_classes = 113  # 预测类别
    model_in_use = 'resNet18'  # 模型选用，可选项有：leNet, alexNet，NiN, GoogLeNet, resNet18, denseNet
    model_kargs = {'in_channels': in_channels, "num_classes": num_classes}  # 模型参数
    # 定义 img_size 根据模型选择
    if model_in_use == 'leNet':
        img_size = (28, 28)
    elif model_in_use in ['alexNet', 'vgg11']:
        img_size = (224, 224)
    else:
        img_size = (45,45)

    idxDict = getIdxDict()
    net = select_model(model_in_use, model_kargs)

    if path == "":
        print("路径不能为空")
    else:
        predict = predictByImage(net, path, img_size)
        print([idxDict[predict]])

    return idxDict[predict]
