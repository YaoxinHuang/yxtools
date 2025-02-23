import torch, argparse
import multiprocessing as mp
from torch.utils.data import DataLoader as DataLoader
from ._base import *
from .readers import *
from .writers import *


'''
Functions
'''

def get_config():
    parser = argparse.ArgumentParser()
    parser.add_argument('--batch_size', default=16, type=int, help='batch size of each gpu')
    parser.add_argument('--epochs', default=25, type=int)
    parser.add_argument('--cuda', default=0, type=int, help='GPU id')

    return parser.parse_args()


def normalize(tensor, mean, std):
    '''
    Normalize the tensor with mean and std.
    Only support 1D, 2D, 3D, 4D tensor / ndarray, list is not acceptable.
    '''
    if len(mean) != len(std):
        raise ValueError(f"The length of mean and std should be the same, but got {len(mean)} and {len(std)}")

    if tensor.dim() == 4:  # [b, c, h, w] format
        for i in range(len(mean)):
            tensor[:, i, :, :] = (tensor[:, i, :, :] - mean[i]) / std[i]
    elif tensor.dim() == 3:  # [c, h, w] format
        for i in range(len(mean)):
            tensor[i, :, :] = (tensor[i, :, :] - mean[i]) / std[i]
    elif tensor.dim() == 2:  # 2D array
        for i in range(len(mean)):
            tensor[:, i] = (tensor[:, i] - mean[i]) / std[i]
    elif tensor.dim() == 1:  # 1D array
        for i in range(len(mean)):
            tensor[i] = (tensor[i] - mean[i]) / std[i]
    else:
        raise ValueError("Unsupported tensor shape")

    return tensor


def model_init(model, init_type:str='kaiming', init_gain=0.02):
    '''
    ### Types = ['normal', 'xavier', 'kaiming', 'orthogonal']
    Initialize the model with the given initialization type.
    ''' 

    def weights_init_normal(m):
        classname = m.__class__.__name__
        if classname.find('Conv') != -1:
            torch.nn.init.normal_(m.weight.data, 0.0, init_gain)
        elif classname.find('Linear') != -1:
            torch.nn.init.normal_(m.weight.data, 0.0, init_gain)
        elif classname.find('BatchNorm2d') != -1:
            torch.nn.init.normal_(m.weight.data, 1.0, init_gain)
            torch.nn.init.constant_(m.bias.data, 0.0)
    
    def weights_init_xavier(m):
        classname = m.__class__.__name__
        if classname.find('Conv') != -1:
            torch.nn.init.xavier_normal_(m.weight.data, gain=init_gain)
        elif classname.find('Linear') != -1:
            torch.nn.init.xavier_normal_(m.weight.data, gain=init_gain)
        elif classname.find('BatchNorm2d') != -1:
            torch.nn.init.normal_(m.weight.data, 1.0, init_gain)
            torch.nn.init.constant_(m.bias.data, 0.0)
    
    def weights_init_kaiming(m):
        classname = m.__class__.__name__
        if classname.find('Conv') != -1:
            torch.nn.init.kaiming_normal_(m.weight.data, a=0, mode='fan_in')
        elif classname.find('Linear') != -1:
            torch.nn.init.kaiming_normal_(m.weight.data, a=0, mode='fan_in')
        elif classname.find('BatchNorm2d') != -1:
            torch.nn.init.normal_(m.weight.data, 1.0, init_gain)
            torch.nn.init.constant_(m.bias.data, 0.0)

    def weights_init_orthogonal(m):
        classname = m.__class__.__name__
        if classname.find('Conv') != -1:
            torch.nn.init.orthogonal_(m.weight.data, gain=init_gain)
        elif classname.find('Linear') != -1:
            torch.nn.init.orthogonal_(m.weight.data, gain=init_gain)
        elif classname.find('BatchNorm2d') != -1:
            torch.nn.init.normal_(m.weight.data, 1.0, init_gain)
            torch.nn.init.constant_(m.bias.data, 0.0)

            
    if init_type == 'normal':
        model.apply(weights_init_normal)
    elif init_type == 'xavier':
        model.apply(weights_init_xavier)
    elif init_type == 'kaiming':
        model.apply(weights_init_kaiming)
    elif init_type == 'orthogonal':
        model.apply(weights_init_orthogonal)
    else:
        raise NotImplementedError(f'Initialization method [{init_type}] is not implemented')


#parametersChoice
import multiprocessing as mp
import time
def check_bestNumWorkers(train_loader, num):
    best = 1e9
    total_num_workers =  mp.cpu_count()
    step = total_num_workers // num
    print(f"num of CPU: {mp.cpu_count()}")
    for num_workers in range(1, total_num_workers+1, step):
        start = time.time()
        for epoch in range(1, 3):
            for i, data in enumerate(train_loader, 0):
                pass
        end = time.time()
        print("Finish with:{} second, num_workers={}".format(end - start, num_workers))
        if end < best:
            best = end
            best_num_workers = num_workers
    return best_num_workers


def mapping(arr, left_b=0, right_b=255):
    return (arr - min(arr)) * (right_b - left_b) / (max(arr) - min(arr)) + left_b

if __name__ == '__main__':
    pass