from scipy.ndimage import binary_erosion, binary_dilation
from skimage.morphology import disk
from scipy.ndimage import distance_transform_edt


def calculate_edge_points(label_volume, mode=2):
    """
    计算数据边缘点
    """
    # 计算边缘点
    if mode == 1:
        edge_points = (distance_transform_edt(label_volume) < 2) >= 1
        return edge_points.astype(label_volume.dtype)
    elif mode == 2:
        eroded_label = binary_erosion(label_volume, disk(1)[np.newaxis, np.newaxis, ...])
        dilation_label = binary_dilation(label_volume)
        edge_points = dilation_label & ~eroded_label
        return edge_points


def normalize_01(img):
    """
    将图像数据归一化到 [0, 1] 区间。

    参数：
    img : ndarray
        输入的图像数据。

    返回：
    img_normalized : ndarray
        归一化后的图像数据。
    """

    # 计算最小值和最大值
    min_val = img.min()
    max_val = img.max()

    # 归一化
    img_normalized = (img - min_val) / (max_val - min_val)

    return img_normalized


if __name__ == '__main__':
    from yaoxin_tools import usual_reader
    import torch
    import numpy as np
    reader = usual_reader()
    seg = reader(r'D:\data\FAZ\Domain1\test\mask\001_D_1.png', 'numpy').astype(np.float32)
    label = reader(r'D:\data\FAZ\Domain1\test\mask\065_M_59.png', 'numpy').astype(np.float32)
    seg1 = calculate_edge_points(seg)
    label1 = calculate_edge_points(label)
    print(np.unique(label1))
    from matplotlib import pyplot as plt
    plt.figure() 
    plt.subplot(221)
    plt.imshow(label[0].reshape(256, 256, 1), cmap='gray')
    plt.subplot(222)
    plt.imshow(label1[0].reshape(256, 256, 1), cmap='gray')
    plt.show()
    print(seg1.sum(), label1.sum())