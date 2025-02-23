from matplotlib import pyplot as plt
from yxtools.tools import usual_reader, os

import torch

def plot_2d_results(model, img_path, device='cuda:0', gt=None, out='./results.png', show_num=None, show=False, cmap='gray'):
    reader = usual_reader()
    if os.path.isfile(img_path):
        imgs = reader(img_path, 'torch').to(device).to(torch.float32)
    else:
        for idx, img in enumerate(sorted(os.listdir(img_path))):
            if idx == 0:
                imgs = reader(os.path.join(img_path + img), 'torch').to(device).to(torch.float32)
                continue
            img = reader(os.path.join(img_path + img), 'torch').to(device).to(torch.float32)
            imgs = torch.cat((imgs, img), dim=0)
    
    # cut series
    if show_num:
        imgs = imgs[:show_num]
    
    model.to(device)
    with torch.no_grad():
        outputs = model(imgs)
    
    if gt is not None:
        if os.path.isfile(gt):
            masks = reader(gt, 'torch').to(device).to(torch.float32)
        else:
            for idx, mask in enumerate(sorted(os.listdir(gt))):
                if idx == 0:
                    masks = reader(os.path.join(gt + mask), 'torch').to(device).to(torch.float32)
                    continue
                mask = reader(os.path.join(gt + mask), 'torch').to(device).to(torch.float32)
                masks = torch.cat((masks, mask), dim=0)
    
    # plt
    figure = plt.figure(figsize=(20, 20))
    b, _, _, _ = outputs[:5].shape
    dim = 3 if gt is not None else 2
    for i in range(b):
        plt.subplot(b, dim, i*dim+1)
        plt.imshow(imgs[i].cpu().numpy().transpose(1, 2, 0), cmap=cmap)
        plt.title('Input Image')
        plt.axis('off')
        
        plt.subplot(b, dim, i*dim+2)
        plt.imshow(outputs[i].cpu().numpy().transpose(1, 2, 0), cmap=cmap)
        plt.title('Output Mask')
        plt.axis('off')
        
        if gt is not None:
            plt.subplot(b, dim, i*dim+3)
            plt.imshow(masks[i].cpu().numpy().transpose(1, 2, 0), cmap=cmap)
            plt.title('GT Mask')
            plt.axis('off')
    plt.savefig(f'{out}')
    if show:
        plt.show()

if __name__ == '__main__':
    state_dict = torch.load(r'D:/Course/Signal Processing/code_task1/checkpoints/UNet_best_lr_0.02_bs_48.pth')
    model = UNet(1,1)
    model.load_state_dict(state_dict)
    plot_2d_results(model, r'E:/Datasets/FAZ/data/FAZ/Domain1/test/imgs/', 
                    gt=r'E:/Datasets/FAZ/data/FAZ/Domain1/test/mask/', 
                    out='./results.png')