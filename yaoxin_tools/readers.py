import os
import SimpleITK as sitk
import numpy as np

from PIL import Image
from torchvision.transforms.functional import pil_to_tensor

from ._base import print_cust


class usual_reader():
    '''
    ### 读取文件的类, 支持读取png, jpg, itk文件。其中图像统一输出为[B,C,H,W]格式,float32, RGB色彩通道; itk文件输出为[Image, Origin, Spacing, Direction]格式
    \n PIL读取的是RGB通道,读取的Size是 W * H, 格式uint8, 0-255, 读取的是PIL格式, 可以直接用于显示
    \n CV2读取的是BGR通道, 读取的shape是H * W * C（Numpy）,float32, , 0-255, 可以直接用于训练, 支持reshape/view函数
    \n Torch要求的是C * H * W, float32, , 0-255, 可以直接用于训练, 支持permute / swapaxes函数
    \n ITK文件读取的是Numpy格式, 输出[Image, Origin, Spacing, Direction]
    \n **注意：Matplotlib.pyplot接受ndarray的[H, W, C]格式用于显示, 如果要把BGR格式改为RGB格式, 请使用img[..., ::-1]或cv2.cvtColor(img, cv2.COLOR_BGR2RGB)**
    '''

    def __call__(self, filename:os.PathLike, arrayType=None, normalize=False, binary=False):
        '''
        Call the reader object to load an image file.
        Parameters:
        - filename (os.PathLike): The path to the image file.
        - arrayType (optional): The desired array type to convert the loaded image data to.
        - normalize (bool): Flag indicating whether to normalize the loaded image data to 0-1.
        Returns:
        - data: The loaded image data.
        Raises:
        - FileExistsError: If the specified file does not exist.
        - TypeError: If the file type is not supported by any of the available file loaders.
        '''
        dtype = os.path.splitext(filename)[-1][1:]
                 
        if not os.path.exists(filename):
            print_cust(f"File {filename} is not existed.", 'red')
            raise FileExistsError()

        file_loaders = {
            'gz': self.load_itk_image, # return numpy array
            'jpg': self.load_jpg_image_pil, # return pil array
            'png': self.load_png_image_pil # return pil array
        }
        
        # 处理文件类型
        loader = file_loaders.get(dtype)
        if loader:
            data = loader(filename, arrayType=arrayType, normalize=normalize, binary=binary)
            return data
        else:
            raise TypeError(f"Your file's mode is {dtype}, there's no Matching File Reader.")
    
    @staticmethod
    def load_itk_image(filename, **kwargs):
        itkimage = sitk.ReadImage(filename)
        numpyImage = sitk.GetArrayFromImage(itkimage)
        numpyOrigin = list(reversed(itkimage.GetOrigin()))
        numpySpacing = list(reversed(itkimage.GetSpacing()))
        numpyDirection = list(reversed(itkimage.GetDirection()))

        if kwargs.get('arrayType') is not None:
            print_cust(f"Warning: The {kwargs.get('arrayType')} is not supported for .gz files, using numpy instead.", 'red')
        
        return numpyImage, numpyOrigin, numpySpacing, numpyDirection


    @staticmethod
    def load_png_image_pil(filename, arrayType=None, **kwargs):
        img = Image.open(filename).convert('L') 
        # weight, height = img.size # 垂直方向, 水平方向
        if arrayType == 'torch':
            img = (pil_to_tensor(img)).unsqueeze(0) * 1.
        if arrayType == 'numpy':
            size = img.size
            img = np.array(img)[np.newaxis, np.newaxis, :, :].reshape([1, 1, size[1], size[0]]) * 1.
        return img / 255. if (kwargs.get('normalize') == True) else img
    
    @staticmethod
    def load_jpg_image_pil(filename, arrayType=None, **kwargs):
        if kwargs.get('binary') == True:
            img = Image.open(filename).convert("L")
        else:
            img = Image.open(filename).convert("RGB")
        if arrayType == 'torch':
            img = (pil_to_tensor(img)).unsqueeze(0) * 1.
        if arrayType == 'numpy':
            size = img.size
            img = np.array(img)[np.newaxis, np.newaxis, :, :].reshape([1, 1, size[1], size[0]]) * 1.
        return img/255. if (kwargs.get('normalize') == True) else img


if __name__ == '__main__':
    b = usual_reader()
    a = b(r'./project_results.png', arrayType='numpy')